from integratedEnergySystemPrototypes import (
    LiBrRefrigeration, # are you sure there's no need to consume electricity here?
    CitySupply,
    Load,
    # PhotoVoltaic,
    # GridNet,
    # no storage?
    # WaterEnergyStorage,
)
from demo_utils import LoadGet, ResourceGet
from config import num_hour, day_node

# num_hour *=3
debug=False
from docplex.mp.model import Model

simulation_name = "micro_refrigeration"

load = LoadGet()
# let's augment the load.
import math
import numpy as np

cool_load = load.get_cool_load(num_hour)
coldWaterLoad = Load("cold_water", cool_load)

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
    num_hour, model,device_count_max=10000 * 10000, device_price=1000, efficiency=0.9,input_type='hot_water',
    debug=debug,
)
hotWaterLiBr.constraints_register()


# power_highTemperatureHotWater_sum = model.continuous_var_list(
#     [i for i in range(0, num_hour)], name="power_highTemperatureHotWater_sum"
# )

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
    device_count_max=10000,
    device_price=3000,
    running_price=municipalHotWater_price0,
    efficiency=0.9,
    output_type = 'hot_water',
    debug=debug,
)
municipalHotWater.constraints_register()

# model.add_constraints(
#     power_highTemperatureHotWater_sum[h] == 
#     # platePhotothermal.power_photoVoltaic[h]+ 
#     municipalHotWater.heat_citySupplied[h]
#     for h in range(num_hour)
# )

# model.add_constraints(
#     hotWaterLiBr.heat_LiBr_from[h] <= power_highTemperatureHotWater_sum[h]
#     for h in range(num_hour)
# )

# # consumption and production
# model.add_constraints(
#     cool_load[h] == hotWaterLiBr.cool_LiBr[h] for h in range(num_hour)
# )


###### SYSTEM OVERVIEW ######
#
# |e\dv | LB | MH | CL |
# |-----|----|----|----|
# | cw  |  s |    |  r |
# | hw  |  r |  s |    |
# 
###### SYSTEM TOPOLOGY ######
# 
# MH -> [NODE1] -> LB -> [NODE2] -> CL
# 


from integratedEnergySystemPrototypes import EnergyFlowNode


cold_water_type = "cold_water"
hot_water_type = "hot_water"

Node1 = EnergyFlowNode(model, num_hour, node_type="greater_equal", debug=debug,energy_type=hot_water_type)
Node2 = EnergyFlowNode(model, num_hour, node_type="greater_equal", debug=debug,energy_type=cold_water_type)

Node1.add_input(municipalHotWater)
Node1.add_output(hotWaterLiBr)

Node2.add_input(hotWaterLiBr)
Node2.add_output(coldWaterLoad)

Node1.build_relations()
Node2.build_relations()

systems = [hotWaterLiBr,municipalHotWater]
# systems = [platePhotothermal,hotWaterLiBr,municipalHotWater]

from mini_data_log_utils import solve_and_log

solve_and_log(systems, model, simulation_name)
# without platephotothermal: 19327715.402514137
# with platephotothermal: 13374199.775218224
# obviously cheaper.