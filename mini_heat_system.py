from integratedEnergySystemPrototypes import (
    PhotoVoltaic,
    # CombinedHeatAndPower,
    # GroundSourceSteamGenerator,
    WaterHeatPump,
    CitySupply,
    Linearization,
    WaterEnergyStorage,
    # GasBoiler,
    GridNet
)
from demo_utils import LoadGet, ResourceGet
from config import num_hour, day_node

# num_hour *=3
from docplex.mp.model import Model

simulation_name = "micro_heat_system"

load = LoadGet()
# let's augment the load.
import math
import numpy as np

heat_load = load.get_heat_load(num_hour)
delta = 0.3
heat_load = (
    np.array([(1 - delta) + math.cos(i * 0.2) * delta for i in range(len(heat_load))])
    * heat_load
)*0.4
model = Model(name=simulation_name)

resource = ResourceGet()
# gas_price0 = resource.get_gas_price(num_hour)
municipalSteam_price0 = resource.get_municipalSteam_price(num_hour)
electricity_price0 = resource.get_electricity_price(num_hour)
intensityOfIllumination0 = (
    resource.get_radiation(path="jinan_changqing-hour.dat", num_hour=num_hour) * 100
)

# 光伏
photoVoltaic = PhotoVoltaic(
    num_hour,
    model,
    device_count_max=5000,  # how about let's alter this?
    device_price=4500,
    intensityOfIllumination=intensityOfIllumination0,
    efficiency=0.8,
    device_name="PhotoVoltaic",
)
photoVoltaic.constraints_register()



# 电网
gridNet = GridNet(
    num_hour,
    model,
    device_count_max=200000,
    device_price=0,
    electricity_price=electricity_price0,
    electricity_price_upload=0.35,
)
gridNet.constraints_register(powerPeak_predicted=2000)



# 水源热泵
waterSourceHeatPumps = (
    WaterHeatPump(  # you are not using the electricity of photothermal power?
        num_hour,
        model,
        device_count_max=2000,
        device_price=3000,
        electricity_price=electricity_price0*0, # with gridnet.
        case_ratio=np.ones(4),
        device_name="waterSourceHeatPumps",
    )
)
waterSourceHeatPumps.constraints_register(model)


# power constrains:

model.add_constraints(waterSourceHeatPumps.electricity_waterSourceHeatPumps[h] == photoVoltaic.power_photoVoltaic[h] + gridNet.total_power[h] for h in range(num_hour))

# 水储能罐
waterStorageTank = WaterEnergyStorage(
    num_hour,
    model,
    waterStorageTank_Volume_max=10000,
    volume_price=300, # make it cheap
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
    model, register_period_constraints=1, day_node=day_node
)

# 市政热水
municipalSteam = CitySupply(
    num_hour,
    model,
    citySupplied_device_max=5000*10000,
    device_price=3000,
    run_price=0.3 * np.ones(num_hour),
    efficiency=0.9,
)
municipalSteam.constraints_register(model)

power_heat_sum = model.continuous_var_list(
    [i for i in range(0, num_hour)], name="power_heat_sum"
)

power_heatStorage = model.continuous_var_list(
    [i for i in range(0, num_hour)], name="power_heatStorage"
)

model.add_constraints(
    power_heat_sum[h]
    == municipalSteam.heat_citySupplied[h]
    + waterSourceHeatPumps.power_waterSourceHeatPumps_heat[h]
    + power_heatStorage[h]
    for h in range(0, num_hour)
)

# 高温热水去处
model.add_constraints(
    power_heat_sum[h] >= heat_load[h] for h in range(0, num_hour)
)  # 每小时热水消耗 >= 每小时热水负荷消耗量

model.add_constraints(
    waterSourceHeatPumps.power_waterSourceHeatPumps_heatStorage[h]
    + waterStorageTank.power_waterStorageTank_heat[h]
    == power_heatStorage[h]
    for h in range(0, num_hour)
)
linearization = Linearization()

linearization.max_zeros(
    # TODO: invert x/y position
    num_hour,
    model,
    y=power_heatStorage,
    x=waterStorageTank.power_waterStorageTank_heat,
)


systems = [
    photoVoltaic,
    gridNet,
    waterSourceHeatPumps,
    waterStorageTank,
    municipalSteam,
]
# systems = [platePhotothermal,hotWaterLiBr,municipalHotWater]

from mini_data_log_utils import solve_and_log

solve_and_log(systems, model, simulation_name)
