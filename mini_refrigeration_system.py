
from integratedEnergySystemPrototypes import LiBrRefrigeration, CitySupply, WaterEnergyStorage
from demo_utils import LoadGet, ResourceGet
from config import num_hour0, day_node
# num_hour0 *=3
from docplex.mp.model import Model

simulation_name = "micro_refrigeration"

load = LoadGet()
cool_load = load.get_cool_load(num_hour0)

model1 = Model(name=simulation_name)

resource = ResourceGet()
municipalHotWater_price0 = resource.get_municipalHotWater_price(num_hour0)


# consumption and production
model1.add_constraint(cool_load[h] == power_cooletStorage[h] for h in range(num_hour0))