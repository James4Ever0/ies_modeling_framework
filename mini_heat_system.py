from integratedEnergySystemPrototypes import (
    TroughPhotoThermal,
    CombinedHeatAndPower,
    GroundSourceSteamGenerator,
    CitySupply,
    GasBoiler,
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

steam_load = load.get_steam_load(num_hour0)
delta = 0.3
steam_load = (
    np.array([(1 - delta) + math.cos(i * 0.2) * delta for i in range(len(steam_load))])
    * steam_load
)
model1 = Model(name=simulation_name)

resource = ResourceGet()
gas_price0 = resource.get_gas_price(num_hour0)
municipalSteam_price0 = resource.get_municipalSteam_price(num_hour0)
electricity_price0 = resource.get_electricity_price(num_hour0)
intensityOfIllumination0 = resource.get_radiation(path="jinan_changqing-hour.dat", num_hour=num_hour0) 

# 槽式光热设备
troughPhotoThermal = TroughPhotoThermal(
    num_hour0,
    model1,
    troughPhotoThermal_device_max=5000,
    troughPhotoThermal_price=2000,
    troughPhotoThermalSolidHeatStorage_price=1000,
    intensityOfIllumination0=intensityOfIllumination0,
    efficiency=0.8,
)
troughPhotoThermal.constraints_register(model1)


# 市政蒸汽
municipalSteam = CitySupply(
    num_hour0,
    model1,
    citySupplied_device_max=5000,
    device_price=3000,
    run_price=0.3 * np.ones(num_hour0),
    efficiency=0.9,
)
municipalSteam.constraints_register(model1)

power_steam_sum = model1.continuous_var_list(
    [i for i in range(0, num_hour0)], name="power_steam_sum"
)
model1.add_constraints(
    power_steam_sum[h]
    == municipalSteam.heat_citySupplied[h]
    + combinedHeatAndPower.wasteGasAndHeat_steam_device.heat_exchange[h]
    + troughPhotoThermal.power_troughPhotoThermal_steam[h]
    for h in range(0, num_hour0)
)
# 高温蒸汽去处
model1.add_constraints(
    power_steam_sum[h] >= steam_load[h] + power_steam_used_heatcool[h]
    for h in range(0, num_hour0)
)  # 每小时蒸汽消耗 >= 每小时蒸汽负荷消耗量+每小时蒸汽用于制冷或者热交换的使用量

# 汽水热交换器
steamAndWater_exchanger = Exchanger(
    num_hour0, model1, device_max=20000, device_price=400, k=50
)
steamAndWater_exchanger.constraints_register(model1)  # qs - 泉水？ steamAndWater热交换器？

# 蒸汽溴化锂
steamPowered_LiBr = LiBrRefrigeration(  # 蒸汽？
    num_hour0, model1, LiBr_device_max=10000, device_price=1000, efficiency=0.9
)
steamPowered_LiBr.constraints_register(model1)

model1.add_constraints(
    power_steam_used_heatcool[h]  # （每小时）蒸汽被使用于制冷或者热交换的量
    >= steamAndWater_exchanger.heat_exchange[h]  # 汽水热交换器得到的热量
    + steamPowered_LiBr.heat_LiBr_from[h]  # 蒸汽溴化锂得到的热量
    for h in range(0, num_hour0)
)
