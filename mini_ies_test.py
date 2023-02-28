# all 12.8 versions of cplex installers:
# http://www.mysmu.edu/faculty/hclau/is421.html

# we need different architecture, via miniconda -> rosetta, x86-64, python==3.7
# https://www.jianshu.com/p/0b95b3d48b99
# using enviorment: `conda activate rosetta`

import os

os.environ["PATH"] = (
    "/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx:" + os.environ["PATH"]
)  # not working?

# print(os.environ['PATH'])

from integratedEnergySystemPrototypes import GridNet, EnergyStorageSystem, PhotoVoltaic
from demo_utils import LoadGet, ResourceGet
from config import num_hour, day_node, epsilon

# num_hour *=3
from docplex.mp.model import Model

simulation_name = "microgrid"

load = LoadGet()
power_load = load.get_power_load(num_hour)

model = Model(name=simulation_name)

resource = ResourceGet()
electricity_price = resource.get_electricity_price(num_hour)
intensityOfIllumination = (
    resource.get_radiation(path="jinan_changqing-hour.dat", num_hour=num_hour) * 100
)

# 光伏
photoVoltaic = PhotoVoltaic(
    num_hour,
    model,
    photoVoltaic_device_max=5000,  # how about let's alter this?
    device_price=4500,
    intensityOfIllumination=intensityOfIllumination,
    efficiency=0.8,
    device_name="PhotoVoltaic",
)
photoVoltaic.constraints_register(model)

# 电网
gridNet = GridNet(
    num_hour,
    model,
    gridNet_device_max=200000,
    device_price=0,
    electricity_price_from=electricity_price,
    electricity_price_to=0.35,
)
gridNet.constraints_register(model, powerPeak_predicted=2000)


# 电池储能
batteryEnergyStorageSystem = EnergyStorageSystem(
    num_hour,
    model,
    energyStorageSystem_device_max=20000,
    energyStorageSystem_price=1800 / 20,  # this won't save anything.
    powerConversionSystem_price=250 / 10,
    conversion_rate_max=2,
    efficiency=0.9,
    energyStorageSystem_init=0.5,  # this value will somehow affect system for sure. epsilon? fully charged? what is the size of the battery? let's set it to zero? (no do not do this or the system will not run. let's set it slightly greater than zero.) this parameter is not used when `register_period_constraints=1` (original) because the battery status will always stay at the same level both at the end and the start.
    stateOfCharge_min=0,  # state of charge
    stateOfCharge_max=1,
)
# original: battery
batteryEnergyStorageSystem.constraints_register(  # using mode 1?
    model, register_period_constraints=0, day_node=day_node
)  # why it is not working under mode 0?

# define energy balance restrictions


from integratedEnergySystemPrototypes import EnergyFlowNode

# util = EnengySystemUtils(model, num_hour)
#
# | r\dv | PV | BESS | GRID | LOAD |
# |------|----|------|------|------|
# | recv |    |  x   |   x  |  x   |
# | send | x  |  x   |   x  |      |
#

############## HOW WE CONNECT THIS ##############
#
# PV - [NODE1] -> BESS -> - [NODE2] - LOAD
#              \_ GRID _/
#
# TOTAL: 2 Nodes

Node1 = EnergyFlowNode(model,num_hour,"greater_equal")
Node2 = EnergyFlowNode(model,num_hour,"greater_equal")

Node1.add_input()

# model.add_constraints(
#     power_load[h]
#     - batteryEnergyStorageSystem.power_energyStorageSystem[h]
#     - photoVoltaic.power_photoVoltaic[h]
#     == gridNet.total_power[h]
#     for h in range(num_hour)
# )

systems = [photoVoltaic, batteryEnergyStorageSystem, gridNet]

from mini_data_log_utils import solve_and_log

solve_and_log(systems, model, simulation_name)
