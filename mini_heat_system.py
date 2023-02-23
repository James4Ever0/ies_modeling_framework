from integratedEnergySystemPrototypes import TroughPhotoThermal,GroundSourceSteamGenerator, CitySupply, GasBoiler
from demo_utils import LoadGet, ResourceGet
from config import num_hour0, day_node
# num_hour0 *=3
from docplex.mp.model import Model

simulation_name = "micro_refrigeration"

load = LoadGet()
# let's augment the load.
import math
import numpy as np

steam_load=load.get_steam_load(num_hour0)
delta = 0.3
steam_load = np.array([(1-delta) + math.cos(i*0.1)*delta for i in range(len(steam_load))])*steam_load
model1 = Model(name=simulation_name)

resource = ResourceGet()
gas_price0 = resource.get_gas_price(num_hour0)
municipalSteam_price0 = resource.get_municipalSteam_price(num_hour0)
electricity_price0 = resource.get_electricity_price(num_hour0)
intensityOfIllumination0 = resource.get_radiation(
    path="jinan_changqing-hour.dat", num_hour=num_hour0
)*100

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

# 地热蒸汽发生器
groundSourceSteamGenerator = GroundSourceSteamGenerator(
    num_hour0,
    model1,
    groundSourceSteamGenerator_device_max=20000,
    groundSourceSteamGenerator_price=200,
    groundSourceSteamGeneratorSolidHeatStorage_price=200,  # gtxr? SolidHeatStorage？
    electricity_price=electricity_price0,
    efficiency=0.9,
)
groundSourceSteamGenerator.constraints_register(model1)

# 热电联产机组
combinedHeatAndPower = CombinedHeatAndPower(
    num_hour0,
    model1,
    combinedHeatAndPower_num_max=5,
    combinedHeatAndPower_price=2000,
    gas_price=gas_price0,
    combinedHeatAndPower_single_device=2000,
    power_to_heat_ratio=1.2,  # dr? 电热?
)
combinedHeatAndPower.constraints_register(model1)

# 燃气锅炉
gasBoiler = GasBoiler(
    num_hour0,
    model1,
    gasBoiler_device_max=5000,
    gasBoiler_price=200,
    gas_price=gas_price0,
    efficiency=0.9,
)
gasBoiler.constraints_register(model1)

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