from integratedEnergySystemPrototypes import (
    TroughPhotoThermal,
    # CombinedHeatAndPower,
    # GroundSourceSteamGenerator,
    WaterHeatPump,
    CitySupply,
    Linearization,
    WaterEnergyStorage,
    # GasBoiler,
)
from demo_utils import LoadGet, ResourceGet
from config import num_hour0, day_node

# num_hour0 *=3
from docplex.mp.model import Model

simulation_name = "micro_refrigeration"

load = LoadGet()
# let's augment the load.
import math
import numpy as np

heat_load = load.get_heat_load(num_hour0)
delta = 0.3
heat_load = (
    np.array([(1 - delta) + math.cos(i * 0.2) * delta for i in range(len(heat_load))])
    * heat_load
)
model1 = Model(name=simulation_name)

resource = ResourceGet()
gas_price0 = resource.get_gas_price(num_hour0)
municipalSteam_price0 = resource.get_municipalSteam_price(num_hour0)
electricity_price0 = resource.get_electricity_price(num_hour0)
# free_electricity_price = 


# 水源热泵
waterSourceHeatPumps = WaterHeatPump( # you are not using the electricity of photothermal power?
    num_hour0,
    model1,
    device_max=2000,
    device_price=3000,
    electricity_price=electricity_price0*0,
    case_ratio=np.ones(4),
    device_name="waterSourceHeatPumps",
)
waterSourceHeatPumps.constraints_register(model1)

# 水储能罐
waterStorageTank = WaterEnergyStorage(
    num_hour0,
    model1,
    waterStorageTank_Volume_max=10000,
    volume_price=300,
    powerConversionSystem_price=1,
    conversion_rate_max=0.5,
    efficiency=0.9,
    energyStorageSystem_init=1,
    stateOfCharge_min=0,
    stateOfCharge_max=1,
    ratio_cool=10,
    ratio_heat=10,
    ratio_gheat=20,
    device_name="waterStorageTank",
)
waterStorageTank.constraints_register(
    model1, register_period_constraints=1, day_node=day_node
)

# 市政热水
municipalSteam = CitySupply(
    num_hour0,
    model1,
    citySupplied_device_max=5000,
    device_price=3000,
    run_price=0.3 * np.ones(num_hour0),
    efficiency=0.9,
)
municipalSteam.constraints_register(model1)

power_heat_sum = model1.continuous_var_list(
    [i for i in range(0, num_hour0)], name="power_heat_sum"
)

power_heatStorage = model1.continuous_var_list(
    [i for i in range(0, num_hour0)], name="power_heat_sum"
)
model1.add_constraints(
    power_heat_sum[h]
    == municipalSteam.heat_citySupplied[h]
    + waterSourceHeatPumps.power_waterSourceHeatPumps_heat[h]
    + power_heatStorage[h]
    for h in range(0, num_hour0)
)

# 高温热水去处
model1.add_constraints(
    power_heat_sum[h] >= heat_load[h] for h in range(0, num_hour0)
)  # 每小时热水消耗 >= 每小时热水负荷消耗量

model1.add_constraints(
    waterSourceHeatPumps.power_waterSourceHeatPumps_heatStorage[h]
    + waterStorageTank.power_energyStorageSystem[h]
    == power_heatStorage[h] 
    for h in range(0, num_hour0)
)
linearization = Linearization()

#
linearization.max_zeros(
    # TODO: invert x/y position
    num_hour0,
    model1,
    y=power_heatStorage,
    x=waterStorageTank.power_energyStorageSystem,
)
