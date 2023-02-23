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
