import json
from topo_check import *
import rich

###############
# build from code.
###############

# FIXED: 加法器没有"output"

def print_with_banner(data, banner: str):
    print()
    print("=" * 40 + f"[{banner}]")
    rich.print(data)
    print()


# you may need pydantic here. verify then import to compute graph.
from ies_optim import (
    柴油信息,
    电负荷信息,
    光伏发电信息,
    风力发电信息,
    柴油发电信息,
    锂电池信息,
    变压器信息,
    变流器信息,
    双向变流器信息,
    传输线信息,
)
from ies_optim import 计算参数

import numpy as np

a = abs(np.random.random((8760,))).tolist()

# algoParam = 计算参数(计算步长="小时", 典型日=False, 计算类型="仿真模拟", 风速=a, 光照=a, 气温=a, 年利率=0.1).dict()
algoParam = 计算参数(计算步长="小时", 典型日=False, 计算类型="设计规划", 风速=a, 光照=a, 气温=a, 年利率=0.1).dict()
# topo = 拓扑图()  # with structure?
topo = 拓扑图(**algoParam)  # with structure?

devParam = dict(生产厂商="Any", 设备型号="Any")

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
DSS = 柴油(topo, param=柴油信息(Price=10, Unit="L/元").dict())
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
        循环边界条件 = '日间连接',
        RatedCapacity=20,
        CostPerCapacity=100,
        TotalCapacity = 20000,
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
print_with_banner(mdict, "图序列化")
with open("template_input.json", "w+") as f:
    f.write(json.dumps(mdict, ensure_ascii=False, indent=4))

###############
# load from dict
###############

topo_load = topo.from_json(mdict)  # static method
print_with_banner(topo_load, "图对象")
# how to check error now?
# all connected?

topo_load.check_consistency()  # may still be good.
## COMPUTE THIS GRAPH ##
# use devs, adders

graph_data = topo.get_graph_data()
print_with_banner(graph_data, "图元数据")
# objective is contained in the graph data.
# so all we need to pass to the compute function are: devs, adders, graph_data
import sys

if sys.argv[-1] in ["-f", "--full"]:
    # 测试全年8760,没有典型日
    from pyomo.environ import *
    from ies_optim import compute, ModelWrapperContext

    with ModelWrapperContext() as mw:
        obj_expr, devInstDict, PD = compute(devs, adders, graph_data, topo.G, mw)

        OBJ = mw.Objective(expr=obj_expr, sense=minimize)

        solver = SolverFactory("cplex")
        try:
            print(">>>SOLVING<<<")
            # results = solver.solve(mw.model, tee=True, keepfiles= True)
            results = solver.solve(mw.model, tee=True)
        except:
            import traceback
            traceback.print_exc()
            print(">>>SOLVER ERROR<<<")
            exprs = [str(mw.model.__dict__[x].expr) for x in dir(mw.model) if x.startswith('CON')]
            output_path = "dump.json"
            print("DUMPING COND TO:" , output_path)
            with open(output_path, 'w+') as f:
                import json
                content = json.dumps(exprs, indent=4, ensure_ascii=False)
                f.write(content)
            # breakpoint()

        print("OBJECTIVE?")
        OBJ.display()
        breakpoint()
        
        print("END")
