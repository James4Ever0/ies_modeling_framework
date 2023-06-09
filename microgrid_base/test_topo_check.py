import json
from topo_check import *
import rich

####################
# build from code. #
####################

# FIXED: 加法器没有"output"


def print_with_banner(data, banner: str):
    print()
    print("=" * 40 + f"[{banner}]")
    rich.print(data)
    print()


# you may need pydantic here. verify then import to compute graph.
from ies_optim import *
from export_format_validate import *

import numpy as np

a = abs(np.random.random((8760,))).tolist()

# algoParam = 计算参数(计算步长="小时", 典型日=False, 计算类型="仿真模拟", 风速=a, 光照=a, 气温=a, 年利率=0.1).dict()
algoParam = 计算参数(计算步长="小时", 典型日=False, 计算类型="设计规划", 风速=a, 光照=a, 气温=a, 年利率=0.1).dict()
# topo = 拓扑图()  # with structure?
topo = 拓扑图(**algoParam)  # with structure?

devParam = dict(生产厂商="Any", 设备型号="Any", 设备名称="Any")


P1 = 光伏发电信息(
    **devParam,
    Area=10,
    PowerConversionEfficiency=0.9,
    MaxPower=20,
    PowerDeltaLimit=1,
    CostPerKilowatt=100,
    CostPerYearPerKilowatt=100,
    VariationalCostPerWork=100,
    Life=20,
    BuildCostPerKilowatt=10,
    BuildBaseCost=10,
    MaxInstallArea=200,
    MinInstallArea=100,
    DeviceCount=100,
).dict()
PV1 = 光伏发电(topo, param=P1)  # 这种是增加新的光伏发电
PV2 = 光伏发电(topo, param=P1)
DSS = 柴油(
    topo,
    param=柴油信息(设备名称="Any", Price=(10, "L/元"), 热值=(10, "MJ/L"), CO2=(10, "kg/L")).dict(),
)
DS = 柴油发电(
    topo,
    param=柴油发电信息(
        **devParam,
        RatedPower=20,
        PowerDeltaLimit=1,
        PowerStartupLimit=1,
        CostPerMachine=100,
        CostPerYearPerMachine=100,
        VariationalCostPerWork=100,
        Life=20,
        BuildCostPerMachine=10,
        BuildBaseCost=10,
        DieselToPower_Load=[[2, 10], [3, 50], [1, 100]],
        DeviceCount=100000000,
        MaxDeviceCount=2000000,
        MinDeviceCount=100,
    ).dict(),
)

DEL1 = 变流器(
    topo,
    param=变流器信息(
        **devParam,
        RatedPower=20,
        CostPerKilowatt=100,
        CostPerYearPerKilowatt=100,
        VariationalCostPerWork=100,
        Life=20,
        Efficiency=0.9,
        BuildCostPerKilowatt=10,
        BuildBaseCost=10,
        DeviceCount=1000000,
        MaxDeviceCount=200,
        MinDeviceCount=100,
    ).dict(),
)
DEL2 = 变压器(
    topo,
    param=变压器信息(
        **devParam,
        PowerParameter=0.9,
        LoadRedundancyParameter=1.2,
        RatedPower=20,
        CostPerKilowatt=100,
        CostPerYearPerKilowatt=100,
        VariationalCostPerWork=100,
        Life=20,
        Efficiency=0.9,
        BuildCostPerKilowatt=10,
        BuildBaseCost=10,
        DeviceCount=1000000,
        MaxDeviceCount=200,
        MinDeviceCount=100,
    ).dict(),
)
LOAD = 电负荷(
    topo, param=电负荷信息(**devParam, EnergyConsumption=a, MaxEnergyConsumption=100).dict()
)

BAT = 锂电池(
    topo,
    param=锂电池信息(
        **devParam,
        循环边界条件="日间连接",
        RatedCapacity=20,
        CostPerCapacity=100,
        TotalCapacity=20000,
        CostPerYearPerCapacity=100,
        VariationalCostPerWork=100,
        Life=20,
        BatteryDeltaLimit=2,
        ChargeEfficiency=0.9,
        DischargeEfficiency=0.9,
        BuildCostPerCapacity=10,
        BuildBaseCost=10,
        InitSOC=0.5,
        BatteryStorageDecay=10,
        BatteryLife=9,
        TotalDischargeCapacity=1000,
        MaxSOC=1,
        MinSOC=0,
        MaxTotalCapacity=200,
        MinTotalCapacity=100,
    ).dict(),
)

A1 = 母线(topo, "可连接供电端母线")
A2 = 母线(topo, "可连接供电端母线")
A3 = 母线(topo, "可连接电母线")

BC = 双向变流器(
    topo,
    param=双向变流器信息(
        **devParam,
        RatedPower=10,
        Efficiency=0.9,
        CostPerKilowatt=100,
        CostPerYearPerKilowatt=100,
        VariationalCostPerWork=100,
        Life=100,
        BuildCostPerKilowatt=100,
        BuildBaseCost=100,
        MaxDeviceCount=200,
        MinDeviceCount=100,
        DeviceCount=1000000,
    ).dict(),
)

连接线(topo, "不可连接电储能端母线", BC.储能端, BAT.电接口)
连接线(topo, "不可连接柴油母线", DS.燃料接口, DSS.燃料接口)
连接线(topo, "不可连接电母线输入输出", BC.线路端, A3.id)

连接线(topo, "不可连接电母线输入", DEL1.电输出, A3.id)
连接线(topo, "不可连接电母线输出", A3.id, DEL2.电输入)

连接线(topo, "不可连接负荷电母线", DEL2.电输出, LOAD.电接口)

连接线(topo, "不可连接供电端母线输入", A1.id, PV1.电接口)
连接线(topo, "不可连接供电端母线输入", A2.id, PV2.电接口)
连接线(topo, "不可连接供电端母线输入", A2.id, DS.电接口)
连接线(topo, "不可连接供电端母线输出", A2.id, DEL1.电输入)

合并线(topo, "可合并供电端母线", A1.id, A2.id)

# L1 = 母线(graph)

# # walk over all connections.

# conn = 连接线(graph, PV.ports["电接口"], LOAD.ports["电接口"])

# conn_merge = 合并线(L0, L1)  # what do you do?
topo.check_consistency()
# shall raise error.

# methods for computing.

devs = topo.get_all_devices()
print_with_banner(devs, "设备")
# {
#     'type': '设备',
#     'subtype': '双向变流器',
#     'ports': {
#         '线路端': {'subtype': '双向变流器线路端输入输出', 'id': 18},
#         '储能端': {'subtype': '双向变流器储能端输入输出', 'id': 19}
#     }
# }

# device, ports, device_data

adders = topo.get_all_adders()
print_with_banner(adders, "加法器")
# input, output, io
# {
#     16: {'input': [6], 'output': [9], 'IO': [18]},
#     14: {'input': [1, 3], 'output': [5], 'IO': []},
#     -1: {'input': [], 'output': [], 'IO': [19, 13]},
#     -2: {'input': [8], 'output': [11], 'IO': []}
# }

###############
# dump to dict
###############

mdict = topo.to_json()
mdictList = [mdict]  # 传入API的计算参数

print_with_banner(mdict, "图序列化")
with open("template_input.json", "w+") as f:
    f.write(json.dumps(mdictList, ensure_ascii=False, indent=4))

###############
# load from dict
###############
import sys


calcParamList = []

for md in mdictList:
    topo_load = topo.from_json(md)  # static method
    print_with_banner(topo_load, "图对象")
    # how to check error now?
    # all connected?

    topo_load.check_consistency()  # may still be good.
    ## COMPUTE THIS GRAPH ##
    # use devs, adders

    graph_data = topo_load.get_graph_data()
    print_with_banner(graph_data, "图元数据")
    # objective is contained in the graph data.
    # so all we need to pass to the compute function are: devs, adders, graph_data
    devs = topo_load.get_all_devices()
    adders = topo_load.get_all_adders()
    calcParam = (devs, adders, graph_data, topo_load.G)
    calcParamList.append(calcParam)
    
if sys.argv[-1] in ["-f", "--full"]:
    assert len(calcParamList)>=1
    firstParam_graphparam = calcParamList[0][2]
    典型日 = firstParam_graphparam['典型日']
    计算步长 = firstParam_graphparam['计算步长']
    计算类型 = firstParam_graphparam['计算类型']
    计算目标 = firstParam_graphparam['计算目标']
    
    if 典型日:
        assert len(calcParamList)>1
    else:
        assert len(calcParamList) == 1
    # 测试全年8760,没有典型日
    DEBUG = False  # poly degree based verification.
    from pyomo.environ import *
    from ies_optim import compute, ModelWrapperContext

    with ModelWrapperContext() as mw:
        # obj_expr = 0
        calcTargetLUT = {
                "经济": 0,
                "环保": 0,
            }
        
        for calc_id, (devs, adders, graph_data, topo_G) in enumerate(calcParamList):
            典型日ID = calc_id
            
            if 典型日:
                graph_data['典型日ID'] = 典型日ID
                timeParam = 24 * len(graph_data['典型日代表的日期'])
            else:
                timeParam = 8760 if 计算步长 == '小时' else 2 # how many hours?
        
            obj_exprs, devInstDict, PD = compute(
                devs, adders, graph_data, topo.G, mw
            )  # single instance.
            (financial_obj_expr, financial_dyn_obj_expr, environment_obj_expr) = obj_exprs
            
            obj_time_param = (1 if not 典型日 else len(graph_data['典型日代表的日期']))
            calcTargetLUT["环保"]+= environment_obj_expr * obj_time_param
            calcTargetLUT["经济"]+= (financial_obj_expr if else financial_dyn_obj_expr) * obj_time_param
            
            expr_base = calcTargetLUT[计算目标]
            if 典型日:
                if 计算步长 == "小时":
                    obj_expr += 
                else:
                    raise Exception(f'不合理的计算步长: {计算步长}')
            else:
                
            

        OBJ = mw.Objective(expr=obj_expr, sense=minimize)

        devClassMapping = {
            f"DI_{k}": c.__class__.__name__.strip("模型") for k, c in devInstDict.items()
        }

        def dumpCond():
            exprs = [
                str(mw.model.__dict__[x].expr)
                for x in dir(mw.model)
                if x.startswith("CON")
            ]
            import re

            def process_expr(expr):
                b = re.findall(r"\[\d+\]", expr)
                for e in b:
                    expr = expr.replace(e, "[]")
                for k, cn in devClassMapping.items():
                    expr = expr.replace(k, cn)
                return expr

            new_exprs = set([process_expr(e) for e in exprs])

            exprs = list(new_exprs)

            output_path = "dump.json"
            print("DUMPING COND TO:", output_path)
            with open(output_path, "w+") as f:
                import json

                content = json.dumps(exprs, indent=4, ensure_ascii=False)
                f.write(content)

        if DEBUG:
            dumpCond()
        solver = SolverFactory("cplex")
        try:
            print(">>>SOLVING<<<")
            # results = solver.solve(mw.model, tee=True, keepfiles= True)
            results = solver.solve(mw.model, tee=True)
        except:
            import traceback

            traceback.print_exc()
            print(">>>SOLVER ERROR<<<")
            # breakpoint()

        # print("OBJECTIVE?")
        # OBJ.display()
        try:
            print("OBJ:", value(OBJ))
            # export value.
            # import json
            sol = True
        except:
            sol = False
            print("NO SOLUTION.")
        if sol:
            try:
                with open("export_format.json", "r") as f:
                    dt = json.load(f)
                    columns = dt["仿真结果"]["ALL"]
                    columns = [e if type(e) == str else e[0] for e in columns]
                import pandas as pd

                仿真结果表 = []
                出力曲线字典 = {} # 设备ID: 设备出力曲线
                from export_format_validate import *

                for devId, devInst in devInstDict.items():
                    devClassName = devInst.__class__.__name__.strip("模型")
                    结果类 = globals()[f"{devClassName}仿真结果"]  # 一定有的
                    出力曲线类 = globals().get(f"{devClassName}出力曲线", None)
                    结果 = 结果类.export(devInst, timeParam)
                    仿真结果表.append(结果.dict())

                    if 出力曲线类:
                        出力曲线 = 出力曲线类.export(devInst, timeParam)
                        出力曲线字典.update({devId: 出力曲线.dict()})
                仿真结果表 = pd.DataFrame(仿真结果表, columns=columns)
                print()
                rich.print(出力曲线字典)
                print()
                仿真结果表.head()
                # export_table = 仿真结果表.to_html()
                # may you change the format.
                sim_table_obj = 仿真结果表.to_json(force_ascii=False, orient='records')
            except:
                import traceback

                traceback.print_exc()
                breakpoint()
        breakpoint()

        print("END")

## assume we have multiobjective here.

min_finance, fin_env = 0, 3
env_finance, min_env = 1, 1

import numpy as np

a, b = min_finance, env_finance
if a == b:
    raise Exception("Unable to perform multiobjective search.")
elif a > b:
    a, b = b, a

fin_points = np.linspace(a, b, num=11)
for fin_start, fin_end in zip(fin_points[:-1].tolist(), fin_points[1:].tolist()):
    print("{} <= FIN <= {}".format(fin_start, fin_end))  # fin constraint
    # min env under this condition. recalculate.
