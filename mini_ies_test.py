# all 12.8 versions of cplex installers:
# http://www.mysmu.edu/faculty/hclau/is421.html

# we need different architecture, via miniconda -> rosetta, x86-64, python==3.7
# https://www.jianshu.com/p/0b95b3d48b99
# using enviorment: `conda activate rosetta`

import os

os.environ['PATH']='/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx:'+os.environ['PATH'] # not working?

# print(os.environ['PATH'])

from integratedEnergySystemPrototypes import GridNet, EnergyStorageSystem, PhotoVoltaic
from demo_utils import LoadGet, ResourceGet
from config import num_hour0, day_node, epsilon
# num_hour0 *=3
from docplex.mp.model import Model

simulation_name = "microgrid"

load = LoadGet()
power_load = load.get_power_load(num_hour0)

model1 = Model(name=simulation_name)

resource = ResourceGet()
electricity_price0 = resource.get_electricity_price(num_hour0)
intensityOfIllumination0 = resource.get_radiation(
    path="jinan_changqing-hour.dat", num_hour=num_hour0
)*100

# 光伏
photoVoltaic = PhotoVoltaic(
    num_hour0,
    model1,
    photoVoltaic_device_max=5000, # how about let's alter this?
    device_price=4500,
    intensityOfIllumination0=intensityOfIllumination0,
    efficiency=0.8,
    device_name="PhotoVoltaic",
)
photoVoltaic.constraints_register(model1)

# 电网
gridNet = GridNet(
    num_hour0,
    model1,
    gridNet_device_max=200000,
    device_price=0,
    electricity_price_from=electricity_price0,
    electricity_price_to=0.35,
)
gridNet.constraints_register(model1, powerPeak_pre=2000)


# 电池储能
batteryEnergyStorageSystem = EnergyStorageSystem(
    num_hour0,
    model1,
    energyStorageSystem_device_max=20000,
    energyStorageSystem_price=1800/20,  #this won't save anything.
    powerConversionSystem_price=250/10,
    conversion_rate_max=2,
    efficiency=0.9,
    energyStorageSystem_init=0.5, # this value will somehow affect system for sure. epsilon? fully charged? what is the size of the battery? let's set it to zero? (no do not do this or the system will not run. let's set it slightly greater than zero.) this parameter is not used when `register_period_constraints=1` (original) because the battery status will always stay at the same level both at the end and the start.
    stateOfCharge_min=0,  # state of charge
    stateOfCharge_max=1,
)
# original: battery
batteryEnergyStorageSystem.constraints_register( # using mode 1?
    model1, register_period_constraints=0, day_node=day_node
) # why it is not working under mode 0?

# define energy balance restrictions

model1.add_constraints(
    power_load[h]
    - batteryEnergyStorageSystem.power_energyStorageSystem[h]
    - photoVoltaic.power_photoVoltaic[h]
    == gridNet.total_power[h]
    for h in range(num_hour0)
)

systems = [photoVoltaic, batteryEnergyStorageSystem, gridNet]

systems_annualized = [system.annualized for system in systems]

import functools

objective = functools.reduce(lambda a, b: a + b, systems_annualized)

model1.minimize(objective)

# 1000秒以内解出 否则放弃
model1.set_time_limit(time_limit=1000)

from typing import Union
from docplex.mp.solution import SolveSolution

# 模型求解返回值 可为空
solution_run1: Union[None, SolveSolution] = model1.solve(
    log_output=True
)  # output some solution.

from data_visualize_utils import (
    printDecisionVariablesFromSolution,
    printIntegratedEnergySystemDeviceCounts,
    plotSingle,
)

if solution_run1 == None:
    print("UNABLE TO SOLVE")
else:
    printDecisionVariablesFromSolution(model1)
    printIntegratedEnergySystemDeviceCounts(systems)

    # collect all types of lists.

    for system in systems:
        system_name = system.device_name
        system_data_name_list = dir(system)
        for system_data_name in system_data_name_list:
            system_data = system.__dict__.get(system_data_name, None)
            if type(system_data) == list:
                # then we plot this!
                plotSingle(
                    system_data,
                    title_content=f"{system_name}_{system_data_name}",
                    save_directory=f"{simulation_name}_figures",
                )
    print("TOTAL ANNUAL:", objective.solution_value)
    # breakpoint()
    # 1007399999.999996 if charge[0] == discharge[0] == 0
    # 992227727.2532595 if no init constrains on charge/discharge
