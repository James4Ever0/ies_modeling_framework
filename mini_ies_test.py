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
    Load,
)
from demo_utils import LoadGet, ResourceGet
from config import num_hour, day_node, epsilon

# num_hour *=3
from docplex.mp.model import Model

simulation_name = "microgrid"

load = LoadGet()
power_load = load.get_power_load(num_hour)

electricityLoad = Load('electricity',power_load)

model = Model(name=simulation_name)

# debug = True # we step through conflicts.
# debug = "EXCEPTION" # we step through conflicts.
# debug = "STEP_EXCEPTION"
debug = False

resource = ResourceGet()
electricity_price = resource.get_electricity_price(num_hour)
intensityOfIllumination = resource.get_radiation(
    path="jinan_changqing-hour.dat", num_hour=num_hour
)

# 光伏
photoVoltaic = PhotoVoltaic(
    num_hour,
    model,
    device_count_max=50000,  # how about let's alter this?
    device_price=4500,
    intensityOfIllumination=intensityOfIllumination,
    efficiency=0.8,
    device_name="PhotoVoltaic",
    # device_count_min=5000,
    debug=debug,
)
photoVoltaic.constraints_register()

# 电网
gridNet = GridNet(
    num_hour,
    model,
    device_count_max=10000,
    device_price=0,
    electricity_price=electricity_price,
    electricity_price_upload=0.35,
    debug=debug
    # device_count_min=5000,
)
gridNet.constraints_register(powerPeak_predicted=2000)


# 电池储能
batteryEnergyStorageSystem = EnergyStorageSystem(
    num_hour,
    model,
    device_count_max=200000,
    device_price=1800,  # this won't save anything.
    device_price_powerConversionSystem=250,
    conversion_rate_max=2,
    efficiency=0.9,
    energy_init=1,  # this value will somehow affect system for sure. epsilon? fully charged? what is the size of the battery? let's set it to zero? (no do not do this or the system will not run. let's set it slightly greater than zero.) this parameter is not used when `register_period_constraints=1` (original) because the battery status will always stay at the same level both at the end and the start.
    stateOfCharge_min=0,  # state of charge
    stateOfCharge_max=1,
    input_type="electricity",
    output_type="electricity",
    device_count_min=1,  # just buy it? what is the problem?
    debug=debug,
)
# original: battery
batteryEnergyStorageSystem.constraints_register(  # using mode 1?
    register_period_constraints=0, day_node=day_node
)  # why it is not working under mode 0?

# define energy balance restrictions


from integratedEnergySystemPrototypes import EnergyFlowNodeFactory

# util = EnengySystemUtils(model, num_hour)
#
# | r\dv | PV | BESS | GRID | LOAD |
# |------|----|------|------|------|
# | recv |    |  x   |   x  |  x   |
# | send | x  |  x   |   x  |      |
#

############## HOW WE CONNECT THIS ##############
#
# are you sure we can connect to the same node?
#
#     _ BESS _   
#    /        \ 
# PV - [NODE1] - LOAD       
#    \_ GRID _/           
#                                   
#
# TOTAL: 1 Node

# no checking!
electricity_type = 'electricity'

NodeFactory = EnergyFlowNodeFactory(model, num_hour,debug=debug)

Node1 = NodeFactory.create_node(electricity_type)
# Node2 = NodeFactory.create_node(electricity_type)

# channels here are not bidirectional, however any connection between nodes is bidirectional, and any attempt of connection between 3 and more nodes will result into interlaced connections. (fully connected)
# from integratedEnergySystemPrototypes import NodeUtils

# Channel1 = model.continuous_var_list(
#     [i for i in range(num_hour)], lb=0, name="channel_1"
# )

# Channel2 = model.continuous_var_list(
#     [i for i in range(num_hour)], lb=0, name="channel_2"
# )

Node1.add_input(photoVoltaic)
# Node1.add_input(Channel2)

Node1.add_input_and_output(gridNet)
# Node1.add_input(gridNet)
# Node1.add_output(gridNet)
# Node1.add_output(Channel1)

Node1.add_input_and_output(batteryEnergyStorageSystem)
# Node1.add_input(batteryEnergyStorageSystem)
# Node1.add_output(batteryEnergyStorageSystem)

# Node2.add_input(Channel1)
Node1.add_output(electricityLoad)
# Node2.add_output(Channel2)

# nodeUtils = NodeUtils(model, num_hour)
# nodeUtils.fully_connected(Node1,Node2)

systems = [photoVoltaic, batteryEnergyStorageSystem, gridNet, electricityLoad]
NodeFactory.build_relations(systems)



from system_topology_utils import visualizeSystemTopology
visualizeSystemTopology(NodeFactory)

# Node1.build_relations()
# Node2.build_relations()

# model.add_constraints(
#     power_load[h]
#     - batteryEnergyStorageSystem.power_energyStorageSystem[h]
#     - photoVoltaic.power_photoVoltaic[h]
#     == gridNet.total_power[h]
#     for h in range(num_hour)
# )

assert NodeFactory.built

from mini_data_log_utils import check_solve_and_log
check_solve_and_log(systems, model, simulation_name)
