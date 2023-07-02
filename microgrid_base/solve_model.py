import json
from typing import List, Dict, Any, Union

try:
    from typing import Literal
except:
    from typing_extensions import Literal
from ies_optim import ModelWrapper
from export_format_validate import *
from pyomo.environ import *
from pyomo.util.infeasible import log_infeasible_constraints

from pydantic import BaseModel
import rich
import io
import logging

mstream = io.StringIO()
# shall you 
logging.basicConfig(stream=mstream, level=logging.INFO)

with open("export_format.json", "r") as f:
    dt = json.load(f)
    columns = dt["仿真结果"]["ALL"]
    columns = [e if type(e) == str else e[0] for e in columns]

with open("frontend_sim_param_translation.json", "r") as f:
    FSPT = json.load(f)

from pandas import DataFrame
from topo_check import 拓扑图


def mDictListToCalcParamList(mdictList: List):
    calcParamList = []

    for md in mdictList:
        topo_load = 拓扑图.from_json(md)  # static method
        # print_with_banner(topo_load, "图对象")
        # how to check error now?
        # all connected?

        topo_load.check_consistency()  # may still be good.
        ## COMPUTE THIS GRAPH ##
        # use devs, adders

        graph_data = topo_load.get_graph_data()
        # print_with_banner(graph_data, "图元数据")
        # objective is contained in the graph data.
        # so all we need to pass to the compute function are: devs, adders, graph_data
        devs = topo_load.get_all_devices()
        adders = topo_load.get_all_adders()
        calcParam = (devs, adders, graph_data, topo_load.G)
        calcParamList.append(calcParam)
    return calcParamList


def translateSimParamTableHeaders(df: DataFrame):
    df_dict = df.to_dict()
    df_dict_translated = {FSPT[k]: v for k, v in df_dict.items()}
    ret = DataFrame(df_dict_translated)
    return ret


# if sys.argv[-1] in ["-f", "--full"]:
def solveModelFromCalcParamList(
    calcParamList: List,
    DEBUG: bool = False,  # replaced by poly degree based verification.
) -> List:
    assert len(calcParamList) >= 1
    # breakpoint()
    firstParam_graphparam = calcParamList[0][2]
    典型日 = firstParam_graphparam["典型日"]
    计算步长 = firstParam_graphparam["计算步长"]
    计算类型 = firstParam_graphparam["计算类型"]
    计算目标 = firstParam_graphparam["计算目标"]

    if 典型日:
        assert len(calcParamList) > 1
    else:
        assert len(calcParamList) == 1
    # 测试全年8760,没有典型日
    from ies_optim import compute, ModelWrapperContext

    # obj_expr = 0
    from copy import deepcopy

    def solve_model(mw: ModelWrapper, obj_expr, sense=minimize):
        OBJ = mw.Objective(expr=obj_expr, sense=sense)

        # devClassMapping = {
        #     f"DI_{k}": c.__class__.__name__.strip("模型") for k, c in devInstDict.items()
        # }

        # def dumpCond():
        #     exprs = [
        #         str(mw.model.__dict__[x].expr)
        #         for x in dir(mw.model)
        #         if x.startswith("CON")
        #     ]
        #     import re

        #     def process_expr(expr):
        #         b = re.findall(r"\[\d+\]", expr)
        #         for e in b:
        #             expr = expr.replace(e, "[]")
        #         for k, cn in devClassMapping.items():
        #             expr = expr.replace(k, cn)
        #         return expr

        #     new_exprs = set([process_expr(e) for e in exprs])

        #     exprs = list(new_exprs)

        #     output_path = "dump.json"
        #     print("DUMPING COND TO:", output_path)
        #     with open(output_path, "w+") as f:
        #         import json

        #         content = json.dumps(exprs, indent=4, ensure_ascii=False)
        #         f.write(content)

        # if DEBUG:
        #     dumpCond()

        solved = False
        with SolverFactory("cplex") as solver:
            # try:
            solver.options["timelimit"] = 60 * 24  # solver timeout: 24 minutes.
            print(">>>SOLVING<<<")
            # results = solver.solve(mw.model, tee=True, keepfiles= True)
            # results = solver.solve(mw.model, tee=True, options = dict(mipgap=0.01, emphasis_numerical='y'))
            results = solver.solve(mw.model, tee=True)
            print("SOLVER RESULTS?")
            rich.print(results)

            # breakpoint() # TODO: check diesel engine issues.

            # except:
            #     import traceback
            #     traceback.print_exc()
            # print(">>>SOLVER ERROR<<<")
            # breakpoint()
            # "Solver (cplex) did not exit normally"
            # return False  # you can never get value here.
            # breakpoint()
            # print("OBJECTIVE?")
            # OBJ.display()
            # try:

            assert results, "no solver result."
            TC = results.solver.termination_condition
            SS = results.solver.status
            normalSSs = [SolverStatus.ok, SolverStatus.warning]
            normalTCs = [
                TerminationCondition.globallyOptimal,
                TerminationCondition.locallyOptimal,
                TerminationCondition.feasible,
                TerminationCondition.optimal,
            ]
            error_msg = []
            mstream.truncate(0)
            # strip away other logging data.
            log_infeasible_constraints(
                mw.model, log_expression=True, log_variables=True
            )

            mstream.seek(0)
            infeasible_constraint_log = mstream.getvalue()
            mstream.truncate(0)
            if infeasible_constraint_log:
                error_msg.append("")
                error_msg.append(infeasible_constraint_log)
                error_msg.append("")
                error_msg.append("_" * 20)
                error_msg.append("")
            if TC not in normalTCs:
                error_msg.append(f"abnormal termination condition: {TC}")
            if SS not in normalSSs:
                error_msg.append(f"abnormal solver status: {TC}")
            if error_msg:
                raise Exception("\n".join(error_msg))

            print("OBJ:", value(OBJ))
            # export value.
            # import json
            solved = True
            # except:
            # print("NO SOLUTION.")
        return solved

    class CalcStruct(BaseModel):
        calcTargetLUT: Dict
        devInstDictList: List[Dict]
        PDList: List[Dict]
        timeParamList: List[int]
        graph_data_list: List

    def getCalcStruct(mw: ModelWrapper, mCalcParamList: list):
        calcParamList = deepcopy(mCalcParamList)
        calcTargetLUT = {
            "经济": 0,
            "环保": 0,
        }

        devInstDictList = []
        PDList = []
        timeParamList = []
        graph_data_list = []

        for calc_id, (devs, adders, graph_data, topo_G) in enumerate(calcParamList):
            典型日ID = calc_id

            if 典型日:
                graph_data["典型日ID"] = 典型日ID
                timeParam = 24 * len(graph_data["典型日代表的日期"])
            else:
                timeParam = 8760 if 计算步长 == "小时" else 2  # how many hours?
            timeParamList.append(timeParam)
            obj_exprs, devInstDict, PD = compute(
                devs, adders, graph_data, topo_G, mw
            )  # single instance.
            (
                financial_obj_expr,
                financial_dyn_obj_expr,
                environment_obj_expr,
            ) = obj_exprs

            obj_time_param = 1 if not 典型日 else len(graph_data["典型日代表的日期"])
            calcTargetLUT["环保"] += environment_obj_expr * obj_time_param
            calcTargetLUT["经济"] += (
                financial_obj_expr if 计算类型 == "设计规划" else financial_dyn_obj_expr
            ) * obj_time_param

            devInstDictList.append(devInstDict)
            PDList.append(PD)
            graph_data_list.append(graph_data)

        ret = CalcStruct(
            calcTargetLUT=calcTargetLUT,
            devInstDictList=devInstDictList,
            PDList=PDList,
            timeParamList=timeParamList,
            graph_data_list=graph_data_list,
        )
        return ret

    def fetchResult(solved: bool, ret: CalcStruct):
        if solved:
            # try:
            import pandas as pd

            仿真结果表 = {}
            出力曲线字典 = {}  # 设备ID: 设备出力曲线

            创建出力曲线模版 = lambda: [
                0 for _ in range(8760)
            ]  # 1d array, placed when running under typical day mode.

            def 填充出力曲线(出力曲线模版: List[float], 典型日出力曲线: List[float], 典型日代表的日期: List[int]):
                assert len(出力曲线模版) == 8760
                assert len(典型日出力曲线) == 24
                for day_index in 典型日代表的日期:
                    出力曲线模版[day_index * 24 : (day_index + 1) * 24] = 典型日出力曲线
                return 出力曲线模版

            for index, devInstDict in enumerate(ret.devInstDictList):
                graph_data = ret.graph_data_list[index]
                典型日代表的日期 = graph_data["典型日代表的日期"]
                timeParam = 24 * len(典型日代表的日期) if 典型日 else (8760 if 计算步长 == "小时" else 2)
                for devId, devInst in devInstDict.items():
                    devClassName = devInst.__class__.__name__.strip("模型")
                    # where you convert the units.
                    # devName = devInst.设备信息.设备名称
                    结果类 = globals()[f"{devClassName}仿真结果"]  # 一定有的
                    出力曲线类 = globals().get(f"{devClassName}出力曲线", None)
                    结果 = 结果类.export(devInst, timeParam)
                    # 仿真结果表.append(结果.dict())
                    之前结果 = deepcopy(仿真结果表.get(devInst, None))
                    if 之前结果 == None:
                        仿真结果表[devInst] = 结果.dict()
                    else:
                        仿真结果表[devInst] = {k: v + 之前结果[k] for k, v in 结果.dict().items()}

                    if 出力曲线类:
                        出力曲线 = 出力曲线类.export(devInst, timeParam)
                        if 典型日:
                            if 出力曲线字典.get(devId, None) is None:
                                出力曲线字典[devId] = {
                                    k: 创建出力曲线模版() for k in 出力曲线.dict().keys()
                                }
                            mdict = deepcopy(出力曲线字典[devId])
                            出力曲线字典.update(
                                {
                                    devId: {
                                        k: 填充出力曲线(mdict[k], v, 典型日代表的日期)
                                        for k, v in 出力曲线.dict().items()
                                    }
                                }
                            )
                        else:
                            出力曲线字典.update({devId: 出力曲线.dict()})
            仿真结果表_导出 = pd.DataFrame([v for _, v in 仿真结果表.items()], columns=columns)
            仿真结果表_导出 = translateSimParamTableHeaders(仿真结果表_导出)
            print()
            rich.print(出力曲线字典)
            print()
            仿真结果表_导出.head()
            # export_table = 仿真结果表.to_html()
            # may you change the format.
            仿真结果表_格式化 = 仿真结果表_导出.to_dict(orient="records")
            # return 出力曲线字典, 仿真结果表_格式化
            出力曲线列表 = []
            for devId, content_dict in 出力曲线字典.items():
                deviceName = ret.devInstDictList[0][devId].设备信息.设备名称
                deviceType = ret.devInstDictList[0][devId].__class__.__name__.strip(
                    "模型"
                )
                elem = {"name": deviceName, "plot_list": []}
                for abbr, val in content_dict.items():
                    if abbr in ["元件名称", "时间"]:
                        continue
                    plotName = f"{deviceType}{abbr}出力曲线"
                    xData = content_dict["时间"]
                    yData = val
                    subElem = {
                        "name": plotName,
                        "abbr": abbr,
                        "data": {"x": xData, "y": yData},
                    }
                    elem["plot_list"].append(subElem)
                出力曲线列表.append(elem)
            return dict(performanceDataList=出力曲线列表, simulationResultTable=仿真结果表_格式化)
            # except:
            #     import traceback

            #     traceback.print_exc()
        return None

    ## assume we have multiobjective here.

    class DualObjectiveRange(BaseModel):
        min_finance: float
        fin_env: float
        env_finance: float
        min_env: float

    def prepareConstraintRangesFromDualObjectiveRange(
        DOR: DualObjectiveRange, target: Union[Literal["fin"], Literal["env"]]
    ):
        # min_finance, fin_env = 0, 3
        # env_finance, min_env = 1, 1

        # DOR.min_finance, DOR.fin_env = 0, 3
        # DOR.env_finance, DOR.min_env = 1, 1

        import numpy as np

        if target == "fin":
            a, b = DOR.min_finance, DOR.env_finance
        elif target == "env":
            a, b = DOR.min_env, DOR.fin_env
        else:
            raise Exception("Unsupported target:", target)
        if a == b:
            raise Exception("Unable to perform multiobjective search.")
        elif a > b:
            a, b = b, a

        fin_points = np.linspace(a, b, num=11)
        constraint_ranges = list(zip(fin_points[:-1].tolist(), fin_points[1:].tolist()))
        for fin_start, fin_end in constraint_ranges:
            print("{} <= FIN <= {}".format(fin_start, fin_end))  # fin constraint
            # min env under this condition. recalculate.
        return constraint_ranges

    def solve_model_and_fetch_result(
        calcParamList: List,
        calcTarget: str,
        rangeDict: Union[None, Dict] = None,
        needResult: bool = True,
        additional_constraints: Dict = {},
    ):
        targetNameMappings = dict(
            abbr=dict(经济="fin", 环保="env"), full=dict(经济="finance", 环保="env")
        )
        with ModelWrapperContext() as mw:
            ret = getCalcStruct(mw, calcParamList)
            for expr_name, constraints in additional_constraints.items():
                expr = ret.calcTargetLUT[expr_name]
                min_const = constraints.get("min", None)
                max_const = constraints.get("max", None)
                if min_const:
                    mw.Constraint(expr >= min_const)
                if max_const:
                    mw.Constraint(expr <= max_const)

            obj_expr = ret.calcTargetLUT[calcTarget]
            solved = solve_model(mw, obj_expr)
            result = None
            if solved:
                if rangeDict is not None:
                    rangeDict[f"min_{targetNameMappings['full'][calcTarget]}"] = value(
                        ret.calcTargetLUT[calcTarget]
                    )
                    for key in targetNameMappings["full"].keys():
                        if key != calcTarget:
                            rangeDict[
                                f"{targetNameMappings['abbr'][calcTarget]}_{targetNameMappings['full'][key]}"
                            ] = value(ret.calcTargetLUT[key])
                if needResult:
                    result = fetchResult(solved, ret)  # use 'ret' to prepare result.
            return solved, result, rangeDict

    resultList = []
    # try:
    if 计算目标 in ["经济", "环保"]:
        solved, result, _ = solve_model_and_fetch_result(calcParamList, 计算目标, {})
        if result:
            resultList.append(result)
    else:
        # breakpoint()
        rangeDict = {}
        solved, fin_result, rangeDict = solve_model_and_fetch_result(
            calcParamList, "经济", rangeDict
        )
        # breakpoint()
        if rangeDict != {} and solved:
            solved, env_result, rangeDict = solve_model_and_fetch_result(
                calcParamList, "环保", rangeDict
            )
            # breakpoint()
            if solved:
                # breakpoint()
                DOR = DualObjectiveRange.parse_obj(rangeDict)

                ### 检验经济环保是否互相影响 ###
                if DOR.fin_env == DOR.min_env:
                    # 环境不影响经济 返回最小经济结果
                    return [fin_result]
                elif DOR.env_finance == DOR.min_finance:
                    # 经济不影响环境 返回最小环保结果
                    return [env_result]

                constraint_ranges = prepareConstraintRangesFromDualObjectiveRange(
                    DOR, target="env"  # add some more paremeters.
                )
                for env_start, env_end in constraint_ranges:
                    # for fin_start, fin_end in constraint_ranges:
                    additional_constraints = {
                        #     "经济": {"min": fin_start, "max": fin_end}
                        "环保": {"min": env_start, "max": env_end}
                    }
                    solved, result, _ = solve_model_and_fetch_result(
                        calcParamList,
                        "经济",
                        None,
                        additional_constraints=additional_constraints
                        # calcParamList, "环保", None, additional_constraints = additional_constraints
                    )
                    if solved:
                        if result:
                            resultList.append(result)
        #### LOOP OF PREPARING SOLUTION ####
    # except:
    #     import traceback

    #     traceback.print_exc()
    #     #         breakpoint()  # you need to turn off these breakpoints in release.
    #     # breakpoint()
    print("SOLVER WORKER END.")
    return resultList
