from integratedEnergySystemPrototypes import GridNet, EnergyStorageSystem, PhotoVoltaic
from demo_utils import LoadGet, ResourceGet
from config import num_hour0, day_node

from docplex.mp.model import Model

simulation_name = "microgrid"

load = LoadGet()
power_load = load.get_power_load(num_hour0)

model1 = Model(name=simulation_name)

resource = ResourceGet()
electricity_price0 = resource.get_electricity_price(num_hour0)
intensityOfIllumination0 = resource.get_radiation(
    path="jinan_changqing-hour.dat", num_hour0=num_hour0
)

# 光伏
photoVoltaic = PhotoVoltaic(
    num_hour0,
    model1,
    photoVoltaic_device_max=5000,
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
    energyStorageSystem_price=1800,
    powerConversionSystem_price=250,
    conversion_rate_max=2,
    efficiency=0.9,
    energyStorageSystem_init=1,
    stateOfCharge_min=0,  # state of charge
    stateOfCharge_max=1,
)
# original: battery
batteryEnergyStorageSystem.constraints_register(
    model1, register_period_constraints=1, day_node=day_node
)

systems = [photoVoltaic, batteryEnergyStorageSystem, gridNet]

systems_annualized = [system.annualized for system in systems]

import functools

objective = functools.reduce(lambda a, b: a + b, systems_annualized)

model1.minimize(objective)

from data_visualize_utils import (
    printDecisionVariablesFromSolution,
    printIntegratedEnergySystemDeviceCounts,
    plotSingle,
)

printDecisionVariablesFromSolution(model1)
printIntegratedEnergySystemDeviceCounts(systems)

# collect all types of lists.


for system in systems:
    system_name = system.__name__
    system_data_name_list = dir(system)
    for system_data_name in system_data_name_list:
        system_data = system.__dict__[system_data_name]
        if type(system_data) == list:
            # then we plot this!
            plotSingle(
                system_data,
                title_content=f"{system_name}_{system_data_name}",
                save_directory=f"{simulation_name}_figures",
            )
