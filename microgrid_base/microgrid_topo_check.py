import os

os.environ["SKIP_ARGENV"] = "True"
os.environ["DOTENV"] = ".test_microgrid_topo_env"
# os.environ["DOTENV"] = ".test_topo_env"

data_fpath = "./heatpump_code_reference/windspeed_and_illumination_8760.dat"

windspeed = []  # m/s
illumination = []  # W/m2 -> kW/m2

# NO_BATTERY = True
NO_BATTERY = False
# NO_ELEC_LOAD=True
NO_ELEC_LOAD = False
# NO_RENEWABLE=True
NO_RENEWABLE = False
# DEBUG = True
DEBUG = False

with open(data_fpath, "r") as f:
    for line in f.readlines():
        line = line.strip()
        if line.startswith("#"):
            continue
        dat = line.split()
        if len(dat) == 4:
            num_dat = [float(e) for e in dat]
            windspeed.append(num_dat[3] + 4)
            illumination.append(num_dat[1] / 1000)

from log_utils import logger_print


from config import *

# ies_env.VAR_INIT_AS_ZERO = "1"
# os.environ[
#     "PERCENT_WARNING_THRESHOLD"
# ] = "1"  # percent value less or equal than this value shal be warned
import json
from topo_check import *

# import rich

if DEBUG:
    datalen = 24
else:
    datalen = 8760
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
if DEBUG:
    extraParams = dict(
        典型日代表的日期=[1],
        典型日=True,
    )
else:
    extraParams = dict(
        典型日=False,
    )
algoParam = 计算参数(
    计算目标="经济",
    # 计算目标="经济_环保",
    # 计算目标="环保",
    计算步长="小时",
    # 典型日代表的日期=[1, 2],
    计算类型="设计规划",
    # 风速=windspeed,
    # 光照=illumination,
    风速=windspeed[:datalen],
    光照=illumination[:datalen],
    气温=a,
    贴现率=9,
    # 贴现率=0.1,
    # 年利率=0.1,
    **extraParams,
).dict()
# topo = 拓扑图()  # with structure?
topo = 拓扑图(**algoParam)  # with structure?

devParam = dict(生产厂商="Any", 设备型号="Any")
# devParam = dict(生产厂商="Any", 设备型号="Any", 设备名称="Any")


P1 = 光伏发电信息(
    **devParam,
    设备名称="光伏1",
    Area=2.59,
    RenewableEnergyConsumptionConstraint=新能源消纳约束.限制消纳率,
    RenewableEnergyConsumptionRate=95,
    # too low for percentage
    PowerConversionEfficiency=90,
    # PowerConversionEfficiency=0.9,
    MaxPower=0.6,
    PowerDeltaLimit=10,
    CostPerKilowatt=0.14,
    CostPerYearPerKilowatt=0.002,
    VariationalCostPerWork=0,
    Life=25,
    BuildCostPerKilowatt=0.14,
    BuildBaseCost=0,
    MaxInstallArea=4300,
    MinInstallArea=4300,
    DeviceCount=4300,
).dict()

光伏发电1 = 光伏发电(topo, param=P1)  # 这种是增加新的光伏发电

WT_P1 = 风力发电信息(
    **devParam,
    设备名称="风力1",
    RenewableEnergyConsumptionConstraint=新能源消纳约束.限制消纳率,
    RenewableEnergyConsumptionRate=95,
    CutoutPower=2350,
    RatedPower=2500,
    RatedWindSpeed=9,
    MinWindSpeed=3,
    MaxWindSpeed=20,
    PowerDeltaLimit=10,
    CostPerKilowatt=0.4,
    CostPerYearPerKilowatt=0.005,
    VariationalCostPerWork=0,
    Life=25,
    BuildCostPerKilowatt=0.2,
    BuildBaseCost=0,
    MaxDeviceCount=12,
    MinDeviceCount=12,
    DeviceCount=12,
).dict()


风力发电1 = 风力发电(topo, param=WT_P1)

柴油1 = 柴油(
    topo,
    param=柴油信息(
        设备名称="Any",
        Price=(9.2, "元/L"),
        热值=(9.1667, "kWh/L"),
        CO2=(2.583, "kg/L"),
        NOX=(0.01, "kg/L"),
        SO2=(0.01, "kg/L"),
    ).dict(),
    # param=柴油信息(设备名称="Any", Price=(10, "L/元"), 热值=(10, "MJ/L"), CO2=(10, "kg/L")).dict(),
)

p1 = 柴油发电信息(
    **devParam,
    设备名称="柴油发电1",
    RatedPower=1e4,
    PowerDeltaLimit=0.3,
    PowerStartupLimit=0.0001,
    CostPerMachine=6,
    CostPerYearPerMachine=0.1,
    VariationalCostPerWork=0.1,
    Life=15,
    BuildCostPerMachine=0.2,
    BuildBaseCost=0,
    DieselToPower_Load=[
        (
            0.13,
            29,
        ),
        (
            0.145,
            36,
        ),
        (
            0.164,
            43,
        ),
        (
            0.18,
            50,
        ),
        (
            0.19,
            57,
        ),
        (
            0.21,
            64,
        ),
        (
            0.224,
            71,
        ),
        (
            0.238,
            79,
        ),
        (
            0.26,
            86,
        ),
        (
            0.294,
            93,
        ),
        (
            0.365,
            100,
        ),
    ],
    DeviceCount=20,
    MaxDeviceCount=20,
    MinDeviceCount=20,
).dict()
# breakpoint()

柴油发电1 = 柴油发电(
    topo,
    param=p1,
)


# breakpoint()
def 变流器工厂(index, dc: int, rp: float):
    ret = 变流器(
        topo,
        param=变流器信息(
            **devParam,
            设备名称=f"变流器{index}",
            RatedPower=rp,
            CostPerKilowatt=0.023,
            CostPerYearPerKilowatt=0.00023,
            VariationalCostPerWork=0,
            Life=20,
            Efficiency=99,
            BuildCostPerKilowatt=0,
            BuildBaseCost=0,
            DeviceCount=dc,
            MaxDeviceCount=dc,
            MinDeviceCount=dc,
        ).dict(),
    )
    return ret


变流器1 = 变流器工厂(1, 35, 1000)  # 风机
变流器2 = 变流器工厂(2, 12, 1000)  # 光伏
变流器3 = 变流器工厂(3, 7, 5000)
变流器4 = 变流器工厂(4, 3, 5000)

# import random

LOAD_H = 氢负荷(
    topo,
    param=氢负荷信息(
        **devParam,
        设备名称="氢负荷1",
        # LoadType=负荷类型.Normal,
        LoadType=负荷类型.Flexible,
        Pmin=0,
        # Pmin=100,
        Pmax=1500,
        EnergyConsumption=[1500] * len(a),
        PriceModel=常数氢价(Price=18),
    ).dict(),
)

if not NO_ELEC_LOAD:
    LOAD_E = 电负荷(
        topo,
        param=电负荷信息(
            **devParam,
            设备名称="电负荷1",
            LoadType=负荷类型.Flexible,
            Pmin=100,
            Pmax=500,
            EnergyConsumption=[400] * len(a),  # TODO: fix data retrieval bug
            PriceModel=常数电价(Price=1),
        ).dict(),
    )

if not NO_BATTERY:
    锂电池1 = 锂电池(
        topo,
        param=锂电池信息(
            **devParam,
            设备名称="锂电池1",
            循环边界条件="日间连接",
            RatedCapacity=1000,
            CostPerCapacity=0.06,
            CostPerYearPerCapacity=0,
            VariationalCostPerWork=0.05,
            Life=15,
            BatteryDeltaLimit=0.5,
            ChargeEfficiency=92,
            DischargeEfficiency=92,
            BuildCostPerCapacity=0.03,
            BuildBaseCost=0,
            InitSOC=50,
            BatteryStorageDecay=0,
            # BatteryStorageDecay=0.5,
            BatteryLife=10,
            LifetimeCycleCount=6000,
            # TotalDischargeCapacity=1000,
            MaxSOC=100,
            MinSOC=15,
            TotalCapacity=20000,
            MaxTotalCapacity=20000,
            MinTotalCapacity=1000,
        ).dict(),
    )

    双向变流器1 = 双向变流器(
        topo,
        param=双向变流器信息(
            **devParam,
            设备名称="双向变流器1",
            RatedPower=1250,
            Efficiency=100,
            CostPerKilowatt=0,
            # CostPerKilowatt=0.014,
            CostPerYearPerKilowatt=0,
            VariationalCostPerWork=0,
            Life=20,
            BuildCostPerKilowatt=0,
            BuildBaseCost=0,
            MaxDeviceCount=40,
            MinDeviceCount=10,
            DeviceCount=40,
        ).dict(),
    )


电解槽1 = 电解槽(
    topo,
    param=电解槽信息(
        **devParam,
        设备名称=f"电解槽1",
        RatedInputPower=1e5,
        HydrogenGenerationStartupRate=0.001,
        HydrogenGenerationEfficiency=100,
        DeltaLimit=3.4,
        HeatRecycleEfficiency=100,
        CostPerMachine=900,
        CostPerYearPerMachine=5,
        VariationalCostPerWork=0.01,
        Life=15,
        BuildCostPerMachine=20,
        BuildBaseCost=0,
        MaxDeviceCount=6,
        MinDeviceCount=6,
        DeviceCount=6,
    ).dict(),
)

# 电解槽2 = 电解槽(
#     topo,
#     param=电解槽信息(
#         **devParam,
#         设备名称=f"电解槽2",
#         RatedInputPower=1000,
#         HydrogenGenerationStartupRate=5,
#         HydrogenGenerationEfficiency=60,
#         DeltaLimit=50,
#         HeatRecycleEfficiency=70,
#         CostPerMachine=800,
#         CostPerYearPerMachine=5,
#         VariationalCostPerWork=0.01,
#         Life=15,
#         BuildCostPerMachine=20,
#         BuildBaseCost=0,
#         MaxDeviceCount=6,
#         MinDeviceCount=1,
#         DeviceCount=6,
#     ).dict(),
# )
传输线1 = 传输线(
    topo,
    param=传输线信息(
        **devParam,
        设备名称="传输线1",
        Optimize=True,
        U=10000,
        Rho=2.94e-8,
        GivenAveragePower=10000,
        GivenMaxPower=10000,
        Pwire_Asec_Pr=[
            (7200, 95, 3.3),
            (7800, 120, 3.7),
            (9000, 150, 4.2),
            (10500, 185, 4.7),
            (11200, 210, 5.1),
            (12200, 240, 5.5),
            (13100, 300, 6.2),
            (16000, 400, 7.4),
            (26000, 600, 12.4),
            (39000, 900, 19.2),
            (109000, 900, 19.2),
        ],
        PowerTransferDecay=0,
        CostPerKilometer=0,
        CostPerYearPerKilometer=0,
        Life=20,
        BuildCostPerKilometer=0,
        BuildBaseCost=0,
        Length=20,
    ).dict(),
)

if not NO_RENEWABLE:
    母线1 = 母线(topo, "可连接母线")
    母线2 = 母线(topo, "可连接母线")

母线3 = 母线(topo, "可连接母线")
# 母线4 = 母线(topo, "可连接母线")
# 母线5 = 母线(topo, "可连接母线")


def 创建连接线(left, right):
    连接线(topo, "不可连接母线", left, right)


if not NO_RENEWABLE:
    创建连接线(风力发电1.电接口, 变流器1.电输入)
    创建连接线(光伏发电1.电接口, 变流器2.电输入)

    创建连接线(变流器1.电输出, 母线1.id)
    创建连接线(变流器2.电输出, 母线2.id)

    创建连接线(母线1.id, 变流器3.电输入)
    创建连接线(母线2.id, 变流器4.电输入)

创建连接线(柴油1.燃料接口, 柴油发电1.燃料接口)
创建连接线(柴油发电1.电接口, 母线3.id)
# 创建连接线(变流器3.电输出, 母线3.id)
# 创建连接线(变流器4.电输出, 母线3.id)
创建连接线(母线3.id, 电解槽1.电接口)

if not NO_BATTERY:
    # 创建连接线(锂电池1.电接口, 母线3.id)
    创建连接线(锂电池1.电接口, 双向变流器1.储能端)
    创建连接线(传输线1.电输入, 母线3.id)
    创建连接线(传输线1.电输出, 双向变流器1.线路端)
    # 创建连接线(双向变流器1.线路端, 母线3.id)

# 创建连接线(母线3.id, 传输线1.电输入)
# 创建连接线(传输线1.电输出, 母线4.id)


# if not NO_BATTERY:
#     创建连接线(锂电池1.电接口, 双向变流器1.储能端)
#     创建连接线(双向变流器1.线路端, 母线4.id)

# 创建连接线(传输线1.电输出, 电解槽1.电接口)
# # 创建连接线(母线4.id, 电解槽1.电接口)
# # 创建连接线(母线4.id, 电解槽2.电接口)

# if not NO_ELEC_LOAD:
#     创建连接线(母线4.id, LOAD_E.电接口)

创建连接线(电解槽1.制氢接口, LOAD_H.氢气接口)
# 创建连接线(电解槽2.制氢接口, 母线5.id)

# 创建连接线(母线5.id, LOAD_H.氢气接口)
# 创建连接线(母线5.id, LOAD_H.氢气接口)

# L1 = 母线(graph)

# # walk over all connections.

# conn = 连接线(graph, PV.ports["电接口"], LOAD.ports["电接口"])

# conn_merge = 合并线(L0, L1)  # what do you do?
try:
    topo.check_consistency()
except Exception as e:
    # raise e
    pass
# shall raise error.

# methods for computing.
from fastapi_celery_functions import calculate_energyflow_graph_base

# TODO: add test of celery app
from fastapi_datamodel_template import EnergyFlowGraph

import os

mdict = topo.to_json()
import json

mdictList = [mdict]

# breakpoint()  # error while reloading params
EFG = EnergyFlowGraph(mDictList=mdictList, residualEquipmentLife=2)  # override default.

json_dump_params = dict(ensure_ascii=False, indent=4)
with open("microgrid_topo_check_test_input.json", "w+") as f:
    json.dump(EFG.dict(), f, **json_dump_params)
ret = calculate_energyflow_graph_base(EFG.dict())
logger_print(ret)

if ret:
    with open(saved_path := "microgrid_test_output_full.json", "w+") as f:
        f.write(json.dumps(ret, **json_dump_params))
    logger_print(f"dumped to: {saved_path}")
