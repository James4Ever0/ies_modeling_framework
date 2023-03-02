from integratedEnergySystemPrototypes import (
    PhotoVoltaic,
    # CombinedHeatAndPower,
    # GroundSourceSteamGenerator,
    WaterHeatPump,
    CitySupply,
    Linearization,
    WaterEnergyStorage,
    # GasBoiler,
    Exchanger,
    Load,
    GridNet,
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
) * 0.4
heatLoad = Load("warm_water", data=heat_load)

model = Model(name=simulation_name)
debug = False

resource = ResourceGet()
# gas_price0 = resource.get_gas_price(num_hour)
municipalHotWater_price0 = resource.get_municipalHotWater_price(num_hour)
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
    debug=debug,
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
    debug=debug,
)
gridNet.constraints_register(powerPeak_predicted=2000)


# 水源热泵
waterSourceHeatPumps = (
    WaterHeatPump(  # you are not using the electricity of photothermal power?
        num_hour,
        model,
        device_count_max=2000,
        device_price=3000,
        electricity_price=electricity_price0
        * 0,  # with gridnet, optional electricity input?
        case_ratio=np.ones(4),
        device_name="waterSourceHeatPumps",
        debug=debug,
    )
)
waterSourceHeatPumps.constraints_register()


# power constrains:

# model.add_constraints(waterSourceHeatPumps.electricity_waterSourceHeatPumps[h] == photoVoltaic.power_photoVoltaic[h] + gridNet.total_power[h] for h in range(num_hour))

# 水储能罐
waterStorageTank = WaterEnergyStorage(
    num_hour,
    model,
    volume_max=10000,
    volume_price=300,  # make it cheap
    device_price_powerConversionSystem=1,
    conversion_rate_max=0.5,
    efficiency=0.9,
    energy_init=1,
    stateOfCharge_min=0,
    stateOfCharge_max=1,
    ratio_cold_water=10,
    ratio_warm_water=10,
    ratio_hot_water=20,
    device_name="waterStorageTank",
    debug=debug,
)
waterStorageTank.constraints_register(register_period_constraints=1, day_node=day_node)


hotWaterExchanger = Exchanger(
    num_hour,
    model,
    device_count_max=20000,
    device_price=400,
    k=50,
    device_name="hotWaterExchanger",
    input_type='hot_water',
    output_type='warm_water'
)
hotWaterExchanger.constraints_register()

# 市政热水
municipalHotWater = CitySupply(
    num_hour,
    model,
    device_count_max=5000 * 10000,
    device_price=3000,
    running_price=0.3 * np.ones(num_hour),  # run_price -> running_price
    efficiency=0.9,
    output_type="hot_water",  # add output_type
    debug=debug,
)
municipalHotWater.constraints_register()  # remove "model"

# power_heat_sum = model.continuous_var_list(
#     [i for i in range(0, num_hour)], name="power_heat_sum"
# )

# power_heatStorage = model.continuous_var_list(
#     [i for i in range(0, num_hour)], name="power_heatStorage"
# )

# model.add_constraints(
#     power_heat_sum[h]
#     == municipalHotWater.heat_citySupplied[h]
#     + waterSourceHeatPumps.power_waterSourceHeatPumps_heat[h]
#     + power_heatStorage[h]
#     for h in range(0, num_hour)
# )

# # 高温热水去处
# model.add_constraints(
#     power_heat_sum[h] >= heat_load[h] for h in range(0, num_hour)
# )  # 每小时热水消耗 >= 每小时热水负荷消耗量

# model.add_constraints(
#     waterSourceHeatPumps.power_waterSourceHeatPumps_heatStorage[h]
#     + waterStorageTank.power_waterStorageTank_heat[h]
#     == power_heatStorage[h]
#     for h in range(0, num_hour)
# )
# linearization = Linearization()

# linearization.max_zeros(
#     # TODO: invert x/y position
#     num_hour,
#     model,
#     y=power_heatStorage,
#     x=waterStorageTank.power_waterStorageTank_heat,
# )

systems = [
    photoVoltaic,
    gridNet,
    waterSourceHeatPumps,
    waterStorageTank,
    municipalHotWater,
    hotWaterExchanger,
]

# systems = [platePhotothermal,hotWaterLiBr,municipalHotWater]

###### SYSTEM OVERVIEW ######
#
# |e\dv | PV | GN | HP | WT | MH | WL | EX |
# |-----|----|----|----|----|----|----|----|
# | ele | s  |r\s | r  |    |    |    |    |
# | ww  |    |    | s  | r  |    | r  | s  |
# | ww_s|    |    | s  | s  |    |    |    |
# | hw  |    |    |    |    | s  |    | r  |
#
###### SYSTEM TOPOLOGY ######
#                                                   [NODE3] - WT
#                                                  /          |
#    PV - [NODE1{FC0}] -> GRID -> [NODE2{FC0}] ->  HP         |
#                                                   \         |
#                                                    |        |
#                                                    |       /
#                         MH - [NODE5] ->  EX -> [NODE4] ----
#                                                   |
#                                                   WL

from integratedEnergySystemPrototypes import EnergyFlowNodeFactory, NodeUtils


electricity_type = "electricity"
warm_water_type = "warm_water"
hot_water_type = "hot_water"
warm_water_storage_type = "warm_water_storage"
NodeFactory = EnergyFlowNodeFactory(model, num_hour, debug=debug)


Node1 = NodeFactory.create_node(node_type="greater_equal", energy_type=electricity_type)
Node2 = NodeFactory.create_node(node_type="greater_equal", energy_type=electricity_type)

Node3 = NodeFactory.create_node(
    node_type="greater_equal", energy_type=warm_water_storage_type
)

Node4 = NodeFactory.create_node(node_type="greater_equal", energy_type=warm_water_type)

Node5 = NodeFactory.create_node(node_type="greater_equal", energy_type=hot_water_type)


# in the end, we make some class called the "load class", to ensure the integrity.

Node1.add_input(photoVoltaic)
Node1.add_output(gridNet)

Node2.add_input(gridNet)
Node2.add_output(waterSourceHeatPumps)

nodeUtil = NodeUtils(model, num_hour)
nodeUtil.fully_connected(Node1, Node2)  # ensure the energy types will match.

Node3.add_input(waterSourceHeatPumps)
Node3.add_output(waterStorageTank)

Node4.add_input(waterSourceHeatPumps)
Node4.add_input(waterStorageTank)
Node4.add_input(hotWaterExchanger)
Node4.add_output(heatLoad)

Node5.add_input(municipalHotWater)
Node5.add_output(hotWaterExchanger)

NodeFactory.build_relations()
# Node1.build_relations()
# Node2.build_relations()
# Node3.build_relations()
# Node4.build_relations()

from mini_data_log_utils import check_solve_and_log

check_solve_and_log(systems, model, simulation_name)
