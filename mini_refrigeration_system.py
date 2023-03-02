from integratedEnergySystemPrototypes import (
    LiBrRefrigeration,
    CitySupply,
    PhotoVoltaic,
    # no storage?
    # WaterEnergyStorage,
)
from demo_utils import LoadGet, ResourceGet
from config import num_hour, day_node

# num_hour *=3
from docplex.mp.model import Model

simulation_name = "micro_refrigeration"

load = LoadGet()
# let's augment the load.
import math
import numpy as np

cool_load = load.get_cool_load(num_hour)
delta = 0.3
cool_load = (
    np.array([(1 - delta) + math.cos(i * 0.1) * delta for i in range(len(cool_load))])
    * cool_load
)

model = Model(name=simulation_name)

resource = ResourceGet()
municipalHotWater_price0 = resource.get_municipalHotWater_price(num_hour)
# intensityOfIllumination0 = (
#     resource.get_radiation(path="jinan_changqing-hour.dat", num_hour=num_hour) * 100
# )

# let's add illumination data.

hotWaterLiBr = LiBrRefrigeration(
    num_hour, model, LiBr_device_max=10000 * 10000, device_price=1000, efficiency=0.9
)

hotWaterLiBr.constraints_register()


power_highTemperatureHotWater_sum = model.continuous_var_list(
    [i for i in range(0, num_hour)], name="power_highTemperatureHotWater_sum"
)


# # 平板光热
# platePhotothermal = PhotoVoltaic(
#     num_hour,
#     model,
#     photoVoltaic_device_max=10000,
#     device_price=500,
#     intensityOfIllumination0=intensityOfIllumination0,
#     efficiency=0.8,
#     device_name="platePhotothermal",
# )  # platePhotothermal
# platePhotothermal.constraints_register(model)

# 市政热水
municipalHotWater = CitySupply(
    num_hour,
    model,
    citySupplied_device_max=10000,
    device_price=3000,
    run_price=municipalHotWater_price0,
    efficiency=0.9,
)
municipalHotWater.constraints_register(model)

model.add_constraints(
    power_highTemperatureHotWater_sum[h] == 
    # platePhotothermal.power_photoVoltaic[h]+ 
    municipalHotWater.heat_citySupplied[h]
    for h in range(num_hour)
)

model.add_constraints(
    hotWaterLiBr.heat_LiBr_from[h] <= power_highTemperatureHotWater_sum[h]
    for h in range(num_hour)
)

# consumption and production
model.add_constraints(
    cool_load[h] == hotWaterLiBr.cool_LiBr[h] for h in range(num_hour)
)

systems = [hotWaterLiBr,municipalHotWater]
# systems = [platePhotothermal,hotWaterLiBr,municipalHotWater]

from mini_data_log_utils import solve_and_log

solve_and_log(systems, model, simulation_name)
# without platephotothermal: 19327715.402514137
# with platephotothermal: 13374199.775218224
# obviously cheaper.