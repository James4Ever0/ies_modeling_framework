from log_utils import logger_print

MAKEFILE = dict(inputs=["topo_check.py"], outputs=["check_topo"], args=[])
import os
os.environ["VAR_INIT_AS_ZERO"] = "1"
from config import *
# ies_env.VAR_INIT_AS_ZERO = "1"
# os.environ["UNIT_WARNING_AS_ERROR"] = "1"
# os.environ[
#     "PERCENT_WARNING_THRESHOLD"
# ] = "1"  # percent value less or equal than this value shal be warned
import json
from topo_check import *
# import rich


datalen = 24
# datalen = 8760
####################
# build from code. #
####################

# FIXED: 加法器没有"output"


def print_with_banner(data, banner: str):
    logger_print()
    logger_print("=" * 40 + f"[{banner}]")
    logger_print(data)
    logger_print()


# you may need pydantic here. verify then import to compute graph.
from ies_optim import *
from export_format_validate import *

# import numpy as np

# a = abs(np.random.random((24,))).tolist()
a = [100] * datalen  # this is not random.
# a = abs(np.random.random((datalen,))).tolist()

# algoParam = 计算参数(计算步长="小时", 典型日=False, 计算类型="仿真模拟", 风速=a, 光照=a, 气温=a, 年利率=0.1).dict()
algoParam = 计算参数(
    计算目标="经济",
    # 计算目标="经济_环保",
    # 计算目标="环保",
    计算步长="小时",
    典型日代表的日期=[1],
    # 典型日代表的日期=[1, 2],
    典型日=True,
    # 典型日=False,
    计算类型="设计规划",
    风速=a,
    光照=a,
    气温=a,
    贴现率=0.1,
    # 年利率=0.1,
).dict()
# topo = 拓扑图()  # with structure?
topo = 拓扑图(**algoParam)  # with structure?

devParam = dict(生产厂商="Any", 设备型号="Any", 设备名称="Any")


P1 = 光伏发电信息(
    **devParam,
    Area=10,
    # too low for percentage
    PowerConversionEfficiency=90,
    # PowerConversionEfficiency=0.9,
    MaxPower=9,
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
    param=柴油信息(
        设备名称="Any",
        Price=(10, "元/L"),
        热值=(10, "MJ/L"),
        CO2=(gasEmission := (10, "kg/L")),
        NOX=gasEmission,
        SO2=gasEmission,
    ).dict(),
    # param=柴油信息(设备名称="Any", Price=(10, "L/元"), 热值=(10, "MJ/L"), CO2=(10, "kg/L")).dict(),
)
DS = 柴油发电(
    topo,
    param=柴油发电信息(
        **devParam,
        RatedPower=2000,
        PowerDeltaLimit=100,
        PowerStartupLimit=1,
        CostPerMachine=1,
        CostPerYearPerMachine=1,
        VariationalCostPerWork=1,
        Life=20,
        BuildCostPerMachine=10,
        BuildBaseCost=10,
        DieselToPower_Load=[[2, 10], [3, 50], [1, 100]],
        DeviceCount=100,
        MaxDeviceCount=200,
        MinDeviceCount=100,
    ).dict(),
)

DEL1 = 变流器(
    topo,
    param=变流器信息(
        **devParam,
        RatedPower=20000,
        CostPerKilowatt=100,
        CostPerYearPerKilowatt=100,
        VariationalCostPerWork=100,
        Life=20,
        Efficiency=0.9,
        BuildCostPerKilowatt=10,
        BuildBaseCost=10,
        DeviceCount=1000,
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
        RatedPower=20000,
        CostPerKilowatt=100,
        CostPerYearPerKilowatt=100,
        VariationalCostPerWork=100,
        Life=20,
        Efficiency=0.9,
        BuildCostPerKilowatt=10,
        BuildBaseCost=10,
        DeviceCount=1000,
        MaxDeviceCount=200,
        MinDeviceCount=100,
    ).dict(),
)
LOAD = 电负荷(
    topo,
    param=电负荷信息(
        **devParam,
        EnergyConsumption=[1] * len(a),
        MaxEnergyConsumption=10,
        PriceModel=常数电价(Price=1),
    ).dict(),
)

BAT = 锂电池(
    topo,
    param=锂电池信息(
        **devParam,
        循环边界条件="日间连接",
        RatedCapacity=200,
        CostPerCapacity=100,
        TotalCapacity=2000,
        CostPerYearPerCapacity=100,
        VariationalCostPerWork=100,
        Life=200000,
        BatteryDeltaLimit=0.1,
        ChargeEfficiency=0.9,
        DischargeEfficiency=0.9,
        BuildCostPerCapacity=10,
        BuildBaseCost=10,
        InitSOC=1.5,
        BatteryStorageDecay=10,
        BatteryLife=9000,
        LifetimeCycleCount=100000000,
        # TotalDischargeCapacity=1000,
        MaxSOC=99,
        MinSOC=1,
        MaxTotalCapacity=2000,
        MinTotalCapacity=1000,
    ).dict(),
)

A1 = 母线(topo, "可连接供电端母线")
A2 = 母线(topo, "可连接供电端母线")
A3 = 母线(topo, "可连接电母线")

BC = 双向变流器(
    topo,
    param=双向变流器信息(
        **devParam,
        RatedPower=10000,
        Efficiency=0.9,
        CostPerKilowatt=100,
        CostPerYearPerKilowatt=100,
        VariationalCostPerWork=100,
        Life=100,
        BuildCostPerKilowatt=100,
        BuildBaseCost=100,
        MaxDeviceCount=2000,
        MinDeviceCount=1000,
        DeviceCount=10000,
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

flag = sys.argv[-1]

from fastapi_celery_functions import calculate_energyflow_graph_base

# TODO: add test of celery app
from fastapi_datamodel_template import EnergyFlowGraph

### TEST PARSING ###
# from filediff.diff import file_diff_compare
from copy import deepcopy
import os

EFG = EnergyFlowGraph(
    mDictList=deepcopy(mdictList), residualEquipmentLife=2
)  # override default.

if flag in ["-f", "--full"]:  # been replaced by celery full test.
    ret = calculate_energyflow_graph_base(EFG.dict())
    logger_print(ret)
    if ret:
        with open(saved_path := "test_output_full.json", "w+") as f:
            f.write(json.dumps(ret, ensure_ascii=False, indent=4))
        logger_print(f"dumped to: {saved_path}")
# if True: # override to debug.
elif flag in ["-p", "--partial"]:
    from solve_model import solveModelFromCalcParamList, mDictListToCalcParamList

    mdictList2 = EFG.dict()["mDictList"]
    # text1 = json.dumps(mdictList[0]['nodes'], indent=4, ensure_ascii=False)
    # text2 = json.dumps(mdictList2[0]['nodes'], indent=4, ensure_ascii=False)

    # with open("input_1.json", 'w+') as f:
    #     f.write(text1)

    # with open("input_2.json", 'w+') as f:
    #     f.write(text2)
    # # file_diff_compare(f1, f2, "diff_result.html")
    # # exit()
    # import difflib
    # max_width=150
    # diff_out = "diff_result.html"
    # numlines=0
    # show_all=False

    # logger_print("WRITE DIFF TO:",diff_out)
    # d = difflib.HtmlDiff(wrapcolumn=max_width)
    # with open(diff_out, 'w', encoding="u8") as f:
    #     f.write(d.make_file(text1, text2, context=not show_all, numlines=numlines))
    # exit()

    ### YOU MAY WANT TO DIFF IT ###

    calcParamList = mDictListToCalcParamList(mdictList2)
    resultList = solveModelFromCalcParamList(calcParamList)
    logger_print(resultList)
    logger_print("RESULT:", resultList)
    if resultList:
        with open(saved_path := "test_output_partial.json", "w+") as f:
            f.write(
                json.dumps(resultList, ensure_ascii=False, indent=4).replace(
                    "NaN", "nan"
                )
            )
        logger_print(f"dumped to: {saved_path}")

elif os.path.basename(flag) != os.path.basename(__file__):
    raise Exception(f"Invalid command line arguments: {sys.argv}")

# may you get infeasible constraints on some row.
# Row 'c_e_x1988826_' infeasible, all entries at implied bounds.
# but this row has been transformed by pyomo, which is hard to retrieve.
