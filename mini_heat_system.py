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
