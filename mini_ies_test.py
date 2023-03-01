# all 12.8 versions of cplex installers:
# http://www.mysmu.edu/faculty/hclau/is421.html

# we need different architecture, via miniconda -> rosetta, x86-64, python==3.7
# https://www.jianshu.com/p/0b95b3d48b99
# using enviorment: `conda activate rosetta`

import os

# add this or not?
import sys


def get_platform():
    platforms = {
        "linux1": "Linux",
        "linux2": "Linux",
        "darwin": "OS X",
        "win32": "Windows",
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


platform = get_platform()
if platform == "darwin":  # not my computer!
    os.environ["PATH"] = (
        "/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx:" + os.environ["PATH"]
    )  # not working?

# print(os.environ['PATH'])

from integratedEnergySystemPrototypes import (
    GridNet,
    EnergyStorageSystem,
    PhotoVoltaic,
    symbols,
)
from demo_utils import LoadGet, ResourceGet
from config import num_hour, day_node, epsilon

# num_hour *=3
from docplex.mp.model import Model

simulation_name = "microgrid"

load = LoadGet()
power_load = load.get_power_load(num_hour)*0.01

model = Model(name=simulation_name)

resource = ResourceGet()
electricity_price = resource.get_electricity_price(num_hour)
intensityOfIllumination = (
    resource.get_radiation(path="jinan_changqing-hour.dat", num_hour=num_hour) * 1000
)

# 光伏
photoVoltaic = PhotoVoltaic(
    num_hour,
    model,
    device_count_max=5000,  # how about let's alter this?
    device_price=4500 * 0,
    intensityOfIllumination=intensityOfIllumination,
    efficiency=0.8,
    device_name="PhotoVoltaic",
    device_count_min=5000,
)
photoVoltaic.constraints_register()

# 电网
gridNet = GridNet(
    num_hour,
    model,
    device_count_max=1000,
    device_price=0,
    electricity_price=electricity_price * 10,
    electricity_price_upload=0.35 * 100,
    # device_count_min=5000,
)
gridNet.constraints_register(powerPeak_predicted=2000)


# 电池储能
batteryEnergyStorageSystem = EnergyStorageSystem(
    num_hour,
    model,
    device_count_max=2000,
    device_price=1800 * 0,  # this won't save anything.
    device_price_powerConversionSystem=250 * 0,
    conversion_rate_max=2,
    efficiency=0.9,
    energy_init=1,  # this value will somehow affect system for sure. epsilon? fully charged? what is the size of the battery? let's set it to zero? (no do not do this or the system will not run. let's set it slightly greater than zero.) this parameter is not used when `register_period_constraints=1` (original) because the battery status will always stay at the same level both at the end and the start.
    stateOfCharge_min=0,  # state of charge
    stateOfCharge_max=1,
    input_type="electricity",
    output_type="electricity",
    device_count_min=1 # just buy it? what is the problem?
)
# original: battery
batteryEnergyStorageSystem.constraints_register(  # using mode 1?
    register_period_constraints=0, day_node=day_node
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
#              _<CHANNEL1>_
#             /            \
# PV - [NODE1] -> BESS -> - [NODE2] - LOAD
#     |        |        |           |
#     |        \_ GRID _/           |
#     |                             |
#      \________<CHANNEL2>_________/
#
# TOTAL: 2 Nodes

# no checking!

Node1 = EnergyFlowNode(model, num_hour, symbols.greater_equal)
Node2 = EnergyFlowNode(model, num_hour, symbols.greater_equal)

Channel1 = model.continuous_var_list(
    [i for i in range(num_hour)], lb=0, name="channel_1"
)

Channel2 = model.continuous_var_list(
    [i for i in range(num_hour)], lb=0, name="channel_2"
)

Node1.add_input(photoVoltaic.power_of_outputs["electricity"])
Node1.add_input(Channel2)
Node1.add_output(batteryEnergyStorageSystem.power_of_inputs["electricity"])
Node1.add_output(gridNet.power_of_inputs["electricity"])
Node1.add_output(Channel1)

Node2.add_input(Channel1)
Node2.add_input(gridNet.power_of_outputs["electricity"])
Node2.add_input(batteryEnergyStorageSystem.power_of_outputs["electricity"])
Node2.add_output(power_load)
Node2.add_output(Channel2)


Node1.build_relations()
Node2.build_relations()

# model.add_constraints(
#     power_load[h]
#     - batteryEnergyStorageSystem.power_energyStorageSystem[h]
#     - photoVoltaic.power_photoVoltaic[h]
#     == gridNet.total_power[h]
#     for h in range(num_hour)
# )

systems = [photoVoltaic, batteryEnergyStorageSystem, gridNet]

from mini_data_log_utils import solve_and_log, check_conflict

# before all the fuzz...
check_conflict(model)

breakpoint()

solve_and_log(systems, model, simulation_name)
