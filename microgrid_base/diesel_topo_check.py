from log_utils import logger_print

import os

os.environ["SKIP_ARGENV"] = "True"
os.environ["DOTENV"] = ".test_microgrid_topo_env"
from config import *

# import json
from topo_check import *

from ies_optim import *
from export_format_validate import *

# DEBUG = False
DEBUG = True
data_fpath = "./heatpump_code_reference/windspeed_and_illumination_8760.dat"

windspeed = []  # m/s
illumination = []  # W/m2 -> kW/m2

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
if DEBUG:
    extraParams = dict(
        典型日代表的日期=[1],
        典型日=True,
    )
    datalen = 24

else:
    extraParams = dict(
        典型日=False,
    )
    datalen = 8760

a = [100] * datalen  # this is not random.

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
    RatedPower=100,
    unitPlanningAlgorithmSelection=油耗规划算法.最佳,
    PowerDeltaLimit=0.3,
    PowerStartupLimit=10,
    CostPerMachine=6,
    CostPerYearPerMachine=0.1,
    VariationalCostPerWork=0.1,
    Life=15,
    BuildCostPerMachine=0.2,
    BuildBaseCost=0,
    DieselToPower_Load=[
        ( 0.13, 29,),
        ( 0.145, 36,),
        ( 0.164, 43,),
        ( 0.18, 50,),
        ( 0.19, 57,),
        ( 0.21, 64,),
        ( 0.224, 71,),
        ( 0.238, 79,),
        ( 0.26, 86,),
        ( 0.294, 93,),
        (0.365, 100,),
    ],
    DeviceCount=(c:=3),
    # DeviceCount=10,
    MaxDeviceCount=c,
    MinDeviceCount=c,
).dict()
# breakpoint()

柴油发电1 = 柴油发电(
    topo,
    param=p1,
)


LOAD_E = 电负荷(
    topo,
    param=电负荷信息(
        **devParam,
        设备名称="电负荷1",
        LoadType=负荷类型.Normal,
        # LoadType=负荷类型.Flexible,
        # Pmin=100,
        # Pmax=500,
        EnergyConsumption=[(100*math.sin(i)+300)*0.3 for i in range(len(a))],
        # EnergyConsumption=[400] * len(a),  # TODO: fix data retrieval bug
        PriceModel=常数电价(Price=1),
    ).dict(),
)


def 创建连接线(left, right):
    连接线(topo, "不可连接母线", left, right)


创建连接线(柴油1.燃料接口, 柴油发电1.燃料接口)
创建连接线(柴油发电1.电接口, LOAD_E.电接口)

try:
    topo.check_consistency()
except Exception as e:
    pass

from fastapi_celery_functions import calculate_energyflow_graph_base


import os

mdict = topo.to_json()
import json

mdictList = [mdict]

# breakpoint()  # error while reloading params
EFG = EnergyFlowGraph(mDictList=mdictList, residualEquipmentLife=2)  # override default.

with open("diesel_topo_check_test_input.json", "w+") as f:
    json.dump(EFG.dict(), f)
ret = calculate_energyflow_graph_base(EFG.dict())
logger_print(ret)

if ret:
    with open(saved_path := "diesel_test_output_full.json", "w+") as f:
        f.write(json.dumps(ret, ensure_ascii=False, indent=4))
    logger_print(f"dumped to: {saved_path}")
