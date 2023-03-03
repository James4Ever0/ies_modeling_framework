# coding: utf-8
# 整理完所有缩写的全称之后,绘制拓扑图
# 可以把代码转化成图

"""
- 模块简介:
    - 建立综合能源系统的各种设备机组，包括产能、储能、负荷、能量交换设备等，根据输入信息，创建约束关系，求解规划方案。默认所有的能源产出都对应到目标负荷或储能装置上。
- 输入信息:
    - 机组参数:
        - 机组最大装机量
        - 设备单价
        - 运行价格
        - 效率参数
        - 设备名称
        - PCS价格
        - 最大充放能速率
        - 初始储能量
        - 最大充能量
        - 最小充能量
    - 环境参数:
        - 一天小时数
        - 光照强度
        - 分时用电价格
        - 分时用气价格
        - 市政热水价格
        - 市政蒸汽价格
        - 上传电价
    - 负荷参数:
        - 冷负荷
        - 热负荷
        - 电负荷
        - 蒸汽负荷
- 目标函数:
    - 综合能源系统设备所有设备的年化运维成本综合最小值,即min(sum(各设备的年化运维成本))
- 约束条件: 
    1. 各能源系统中各自的约束条件
    2. 能源获取及负荷需求获取约束
    2. 绝对值线性约束及线性约束条件
    3. 高温蒸汽约束、高温热水约束
    4. 冷 热 冰 供给储存消耗平衡约束
    5. 电供销平衡约束
- 输出信息：
    - 机组设备购买量，设备产能储能每小时工作状况，能量每小时供消情况
"""

# chinese display issue
import matplotlib

# import os

# os.system("chcp 65001") # not working?

# ensure we can display chinese characters
# matplotlib.rc(group="font", family="YouYuan")

# Glyph 8722 (\N{MINUS SIGN}) missing from current font.

from docplex.mp.solution import SolveSolution

# import docplex  # modeling with ibm cplex
from docplex.mp.model import Model
from typing import Union

# import pandas as pd
# import numpy as np

# import time
# import os.path
# import math

# from typing import Iterable

# from docplex.mp.conflict_refiner import ConflictRefiner
# import matplotlib.pyplot as plt

# from matplotlib import style
from result_processlib import Value  # ?

# from docplex.mp.dvar import Var
# from typing import List

# from docplex.mp.vartype import (
#     VarType,
#     BinaryVarType,
#     IntegerVarType,
#     ContinuousVarType,
#     # SemiContinuousVarType,
#     # SemiIntegerVarType,
# )

# we prefer not to plot this.
# from plot_arr import IGESPlot as IntegratedEnergySystemPlot

# create main model
# not specifying model type? really?

from config import (
    # localtime1,
    # run,
    # year,
    # node,
    day_node,
    # debug,
    num_hour,
    # simulationTime,
    # bigNumber,
    # intensityOfIllumination,
)

### BEGIN COMPONENTS DEFINITION ###


### END COMPONENTS DEFINITION ###

# 获取能源负荷信息 都是生成的常数数据
##########################################
from demo_utils import (
    getPowerCoolHeatSteamLoads,
    getResourceData,
    electricSystemRegistration,
    steamSourcesRegistration,
    hotWaterSourcesRegistration,
)

# TODO: 拟合实际情况 根据历史数据 求待定系数 反馈机制

power_load, cool_load, heat_load, steam_load = getPowerCoolHeatSteamLoads(num_hour)

# heat_load is for warm_water.

##########################################

# is this a test on `Linear_absolute`?

# absolute1 = Linear_absolute(model, [-5, 6], [0, 1])
# absolute1.absolute_add_constraints(model)

from integratedEnergySystemPrototypes import (
    IntegratedEnergySystem,  # needed!
    # PhotoVoltaic,
    LiBrRefrigeration,
    # DieselEngine,
    # EnergyStorageSystem,
    # EnergyStorageSystemVariable,
    # TroughPhotoThermal,
    # CombinedHeatAndPower,
    # GasBoiler,
    # ElectricBoiler,
    Exchanger,
    # AirHeatPump,
    # WaterHeatPump,
    # WaterCoolingSpiral,
    # DoubleWorkingConditionUnit,
    # TripleWorkingConditionUnit,
    # GeothermalHeatPump,
    # WaterEnergyStorage,
    # ElectricSteamGenerator,
    # Linear_absolute,
    # CitySupply,
    GridNet,
    Linearization,
    NodeUtils,  # shall we disable in-node connections
    EnergyFlowNodeFactory,
    Load,
)

electricityLoad = Load("electricity", power_load)
warmWaterLoad = Load("warm_water", heat_load)
coldWaterLoad = Load("cold_water", cool_load)
steamLoad = Load("steam", steam_load)

from mini_data_log_utils import check_solve_and_log

debug = False

if __name__ == "__main__":
    model = Model(name="buses")

    # 获取光照、能源价格
    ##########################################
    (
        intensityOfIllumination,
        electricity_price0,
        gas_price0,
        municipalHotWater_price0,
        municipalSteam_price0,
    ) = getResourceData(num_hour)
    ##########################################

    # 发电及电储能装置
    ##########################################
    dieselEngine, photoVoltaic, batteryEnergyStorageSystem = electricSystemRegistration(
        model,
        num_hour,
        intensityOfIllumination,
        day_node,
        debug=debug,
    )
    ##########################################

    # 蒸汽发生装置及参数配置
    ##########################################

    (
        troughPhotoThermal,
        electricSteamGenerator,
        combinedHeatAndPower,
        gasBoiler,
        municipalSteam,
    ) = steamSourcesRegistration(
        model,
        num_hour,
        intensityOfIllumination,
        # day_node,
        electricity_price0,
        gas_price0,
        debug=debug,
    )

    # 以上为蒸汽发生装置
    ##########################################

    # 汽水热交换器
    steamAndWater_exchanger = Exchanger(
        num_hour,
        model,
        device_count_max=20000,
        device_price=400,
        k=50,
        device_name="steamAndWater_exchanger",
        debug=debug,
        input_type="steam",
        output_type="hot_water",
    )
    steamAndWater_exchanger.constraints_register()  # qs - 泉水？ steamAndWater热交换器？

    # 蒸汽溴化锂
    # TODO: 添加设备最少购买数量
    steamPowered_LiBr = LiBrRefrigeration(  # 蒸汽？
        num_hour,
        model,
        device_count_max=10000,
        device_price=1000,
        efficiency=0.9,
        device_name="steamPowered_LiBr",
        debug=debug,
    )
    steamPowered_LiBr.constraints_register()

    (
        platePhotothermal,
        waterStorageTank,
        municipalHotWater,
        gasBoiler_hotWater,  # TODO: 待定是否只能烧高温热水
        phaseChangeHotWaterStorage,
        hotWaterElectricBoiler,
    ) = hotWaterSourcesRegistration(
        model,
        num_hour,
        intensityOfIllumination,
        day_node,
        electricity_price0,
        municipalHotWater_price0,
        gas_price0,
        debug=debug,
    )

    # 热水溴化锂，制冷
    hotWaterLiBr = LiBrRefrigeration(
        num_hour,
        model,
        device_count_max=10000,
        device_price=1000,
        efficiency=0.9,
        device_name="hotWaterLiBr",
        debug=debug,
    )
    hotWaterLiBr.constraints_register()

    # 热水交换器，吸收热量
    hotWaterExchanger = Exchanger(
        num_hour,
        model,
        device_count_max=20000,
        device_price=400,
        k=50,
        device_name="hotWaterExchanger",
        debug=debug,
        input_type="hot_water",
        output_type="warm_water",
    )
    hotWaterExchanger.constraints_register()

    from demo_utils import cooletIceHeatDevicesRegistration

    (
        heatPump,
        waterSourceHeatPumps,
        waterCoolingSpiralMachine,
        tripleWorkingConditionUnit,
        doubleWorkingConditionUnit,
        groundSourceHeatPump,
        iceStorage,
        phaseChangeColdWaterStorage,
        phaseChangeWarmWaterStorage,
    ) = cooletIceHeatDevicesRegistration(
        model,
        num_hour,
        electricity_price0,
        debug=debug,
    )

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

    # 高温蒸汽去向
    ##########################################
    # power_steam_used_product = model.continuous_var_list(
    #     [i for i in range(0, num_hour)], name="power_steam_used_product"
    # )  # shall this be never used?
    # power_steam_used_heatcool = model.continuous_var_list(
    #     [i for i in range(0, num_hour)], name="power_steam_used_heatcool"
    # )
    # power_steam_sum = model.continuous_var_list(
    #     [i for i in range(0, num_hour)], name="power_steam_sum"
    # )
    NodeFactory = EnergyFlowNodeFactory(model=model, num_hour=num_hour, debug=debug)
    SteamNode1 = NodeFactory.create_node(
        "steam"
    )  # shall we automatically determine the equation type?

    for device in [
        municipalSteam,
        combinedHeatAndPower,
        troughPhotoThermal,
        electricSteamGenerator,
        gasBoiler,
    ]:
        SteamNode1.add_input(device)

    for device in [steamLoad, steamAndWater_exchanger, steamPowered_LiBr]:
        SteamNode1.add_output(device)

    # model.add_constraints( # node input
    #     power_steam_sum[h]
    #     == municipalSteam.heat_citySupplied[h]
    #     + combinedHeatAndPower.wasteGasAndHeat_steam_device.heat_exchange[h]
    #     + troughPhotoThermal.power_troughPhotoThermal_steam[h]
    #     + electricSteamGenerator.power_electricSteamGenerator_steam[h]
    #     + gasBoiler.heat_gasBoiler[
    #         h
    #     ]  # （每小时）所有产生蒸汽量的总和 = 市政热量 + CHP余气余热蒸汽 + 槽式光热产蒸汽 + 燃气锅炉产生热量
    #     for h in range(0, num_hour)
    # )
    # # 高温蒸汽去处
    # model.add_constraints( # steam_load <- node output?
    #     power_steam_sum[h] >= steam_load[h] + power_steam_used_heatcool[h]
    #     for h in range(0, num_hour)
    # )  # 每小时蒸汽的总和 >= 每小时蒸汽负荷消耗量+每小时蒸汽用于制冷或者热交换的使用量

    # model.add_constraints( # node output
    #     power_steam_used_heatcool[h]  # （每小时）蒸汽被使用于制冷或者热交换的量
    #     >= steamAndWater_exchanger.heat_exchange[h]  # 汽水热交换器得到的热量
    #     + steamPowered_LiBr.heat_LiBr_from[h]  # 蒸汽溴化锂得到的热量
    #     for h in range(0, num_hour)
    # )
    ##########################################

    # 高温热水发生装置及水储能装置
    ##########################################
    # highTemperatureHotWater
    # 1) combinedHeatAndPower gasTurbineSystem?
    # 2) combinedHeatAndPower wasteGasAndHeat__to_water?
    # 3

    ##########################################

    hotWaterNode1 = NodeFactory.create_node("hot_water")

    # 高温热水合计
    power_highTemperatureHotWater_sum = model.continuous_var_list(
        [i for i in range(0, num_hour)], name="power_highTemperatureHotWater_sum"
    )

    for device in [
        combinedHeatAndPower,
        platePhotothermal,
        phaseChangeHotWaterStorage,
        municipalHotWater,
        gasBoiler_hotWater,
        hotWaterElectricBoiler,
    ]:
        hotWaterNode1.add_input(device)

    hotWaterNode1.add_input_and_output(waterStorageTank)

    for device in [hotWaterLiBr, hotWaterExchanger]:
        hotWaterNode1.add_output(device)

    # TODO: 这些设备能不能输出高温热水 待定
    # model.add_constraints(  # inputs
    #     power_highTemperatureHotWater_sum[h]
    #     == combinedHeatAndPower.gasTurbineSystem_device.heat_exchange[h]
    #     + combinedHeatAndPower.wasteGasAndHeat_water_device.heat_exchange[
    #         h
    #     ]  # wasteGasAndHeat_？
    #     + platePhotothermal.power_photoVoltaic[h]
    #     + phaseChangeHotWaterStorage.power_energyStorageSystem[h]
    #     + municipalHotWater.heat_citySupplied[h]
    #     + gasBoiler_hotWater.heat_gasBoiler[h]
    #     + hotWaterElectricBoiler.heat_electricBoiler[h]
    #     + waterStorageTank.power_waterStorageTank_gheat[h]  # 水储能设备发出的热量？ bidirectional! input and output.
    #     for h in range(
    #         0, num_hour
    #     )  # 高温热水 = CHP燃气轮机热交换量 + CHP供暖热水热交换量+ 平板光热发热功率 + 相变储热装置的充放能功率 + 市政热水实际消耗 + 燃气锅炉热功率 + 电锅炉热功率 + 水蓄能设备（高温？）水储能功率
    # )

    # 高温热水去向
    # model.add_constraints( # output
    #     power_highTemperatureHotWater_sum[h]
    #     >= hotWaterLiBr.heat_LiBr_from[h] + hotWaterExchanger.heat_exchange[h]
    #     for h in range(0, num_hour)  # （每小时）高温热水总热量 >= 热水溴化锂消耗热量 + 热交换器消耗热量
    # )
    # model.add_constraints( # precluded.
    #     power_highTemperatureHotWater_sum[h] >= 0 for h in range(0, num_hour)
    # )  # （每小时）高温热水总热量>=0

    # power_heatPump[h]*heatPump_flag[h]+power_waterStorageTank[h]*waterStorageTank_flag[h]+power_waterCoolingSpiralMachine[h]*waterSourceHeatPumps_flag[h]+power_LiBr[h]+power_waterCoolingSpiralMachine[h]+power_iceStorage[h]==cool_load[h]%冷量需求
    # power_heatPump[h]*(1-heatPump_flag[h])+power_waterStorageTank[h]*(1-waterStorageTank_flag[h])+power_waterSourceHeatPumps[h]*(1-waterSourceHeatPumps_flag[h])+power_gas[h]+power_groundSourceHeatPump[h]==heat_load[h]%热量需求
    # 采用线性化技巧,处理为下面的约束.基于每种设备要么制热,要么制冷。
    # 供冷:风冷heatPump groundSourceHeatPump 蓄能水罐 hotWaterLiBr机组 蒸汽LiBr机组 phaseChangeColdWaterStorage
    # 供热:风冷heatPump groundSourceHeatPump 蓄能水罐 地热 水水Exchanger传热
    # heatPump = AirHeatPump(num_hour, model, device_max=10000, device_price=1000, electricity_price=electricity_price0)
    # heatPump.constraints_register(model)

    # 冷 热 冰 供给储存消耗平衡
    ##########################################

    # 产能储能机组平衡输出功率
    ###########
    #
    #
    #
    #
    warmWaterStorageNode1 = NodeFactory.create_node("warm_water_storage")
    warmWaterNode1 = NodeFactory.create_node("warm_water")

    coldWaterStorageNode1 = NodeFactory.create_node("cold_water_storage")
    coldWaterNode1 = NodeFactory.create_node("cold_water")

    iceNode1 = NodeFactory.create_node("ice")

    # power_cooletStorage = model.continuous_var_list(
    #     [i for i in range(0, num_hour)], name="power_cooletStorage"
    # )
    # power_heatStorage = model.continuous_var_list(
    #     [i for i in range(0, num_hour)], name="power_heatStorage"
    # )
    # power_iceStorage = model.continuous_var_list(
    #     [i for i in range(0, num_hour)], name="power_iceStorage"
    # )

    ###########
    for device in [
        heatPump,
        waterStorageTank,
        phaseChangeColdWaterStorage,
        #     + power_cooletStorage[h] # this thing is indirect. it is actually the sum of the cold water storage outputs.
        waterSourceHeatPumps,
        steamPowered_LiBr,
        hotWaterLiBr,
        waterCoolingSpiralMachine,
        iceStorage,
        tripleWorkingConditionUnit,
        doubleWorkingConditionUnit,
    ]:
        coldWaterNode1.add_input(device)

    # power_heatPump_cool[h]+power_cooletStorage[h]+power_waterSourceHeatPumps_cool[h]+power_zqLiBr[h]+power_hotWaterLiBr[h]+power_waterCoolingSpiralMachine_cool[h]+power_ice[h]+power_tripleWorkingConditionUnit_cool[h]+power_doubleWorkingConditionUnit_cool[h]==cool_load[h]%冷量需求

    # what is "_x"?
    # model.add_constraints( # cold_water input -> output
    #     heatPump.power_waterSourceHeatPumps_cool[h]
    #     + power_cooletStorage[h] # this thing is indirect. it is actually the sum of the cold water storage outputs.
    #     + waterSourceHeatPumps.power_waterSourceHeatPumps_cool[h]
    #     + steamPowered_LiBr.cool_LiBr[h]
    #     + hotWaterLiBr.cool_LiBr[h]
    #     + waterCoolingSpiralMachine.power_waterCoolingSpiralMachine_cool[h]
    #     + power_iceStorage[h] # output of iceStorage.
    #     + tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_cool[h]
    #     + doubleWorkingConditionUnit.power_doubleWorkingConditionUnit_cool[h]
    #     == cool_load[
    #         h
    #     ]  # 冷量需求 == (热泵制冷功率 + 水源热泵制冷功率 + 蒸汽溴化锂机组制冷量 + 热水溴化锂机组制冷量 + 水冷螺旋机的制冷功率 + 三工况机组的制冷功率 + 双工况机组的制冷功率) + (蓄冰机组平衡输出 + 蓄冷机组平衡输出)
    #     for h in range(0, num_hour)
    # )
    # power_heatPump_heat[h]+power_heatStorage[h]+power_waterSourceHeatPumps_heat[h]+power_gas_heat[h]+power_ss_heat[h]+power_groundSourceHeatPump[h]+power_tripleWorkingConditionUnit_heat[h]==heat_load[h]%热量需求
    model.add_constraints(  # warm_water input -> output
        heatPump.power_waterSourceHeatPumps_heat[h]
        + power_heatStorage[h]  # actually sum of warm_water storage outputs.
        + waterSourceHeatPumps.power_waterSourceHeatPumps_heat[h]
        + steamAndWater_exchanger.heat_exchange[h]  # both warm water output.
        + hotWaterExchanger.heat_exchange[h]  # both warm water output.
        + tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_heat[h]
        + groundSourceHeatPump.power_groundSourceHeatPump[h]
        == heat_load[
            h
        ]  # 热量需求 = 热泵制热功率 + 蓄热机组平衡输出 + 水源热泵制热功率 + 汽水热交换量 + 热水热交换量 + 三工况机组的制热功率 + 地源热泵输出功率
        for h in range(0, num_hour)
    )
    # 冰蓄冷逻辑组合
    model.add_constraints(
        tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_ice[h]
        + doubleWorkingConditionUnit.power_doubleWorkingConditionUnit_ice[h]
        + iceStorage.power_energyStorageSystem[
            h
        ]  # where you are going to use this power?
        == power_iceStorage[h]  # 蓄冰机组平衡输出 == (三工况机组的制冰功率 + 双工况机组的制冰功率) + 冰蓄能充放能功率
        for h in range(0, num_hour)
    )
    linearization = Linearization()
    # it is right in the topology.
    linearization.max_zeros(
        # TODO: invert x/y position
        # 修改之前： 要么冰蓄冷功率为0，冰蓄能装置不充不放; 要么冰蓄冷功率等于蓄冷装置充放功率（此时冰蓄能释放能量）
        # 修改之后： 要么蓄冰机组平衡输出为0，冰蓄能装置充能（负数），制冰机组输出（正数）全部被冰蓄能装置吸收；要么制冰机组用于蓄冰的功率为0，冰蓄能装置放能（正数），蓄冰机组平衡输出（正数）全部由冰蓄能装置提供
        num_hour,
        model,
        y=power_iceStorage,
        x=iceStorage.power_energyStorageSystem,
    )

    # 蓄冷逻辑组合
    for device in [heatPump, waterSourceHeatPumps, waterCoolingSpiralMachine]:
        coldWaterStorageNode1.add_input(device)
    for device in [
        waterStorageTank,
        phaseChangeColdWaterStorage,
    ]:
        coldWaterStorageNode1.add_output(device)
    model.add_constraints(
        heatPump.power_waterSourceHeatPumps_cooletStorage[h]
        + waterSourceHeatPumps.power_waterSourceHeatPumps_cooletStorage[h]
        + waterCoolingSpiralMachine.power_waterCoolingSpiralMachine_cooletStorage[h]
        + waterStorageTank.power_waterStorageTank_cool[h]
        + phaseChangeColdWaterStorage.power_energyStorageSystem[h]
        == power_cooletStorage[
            h
        ]  # 蓄冷系统平衡功率 == (热泵蓄冷功率 + 水源热泵蓄冷功率 + 水冷螺旋机的蓄冷功率) + (水蓄能设备蓄冷充放功率 + 相变蓄冷设备充放功率)
        for h in range(0, num_hour)
    )
    linearization.max_zeros(
        num_hour,
        model,
        # TODO: invert x/y position
        # 修改之前：要么蓄冷设备不充不放，系统不产生冷量；要么消耗冷，冷量全部由蓄冷设备提供
        # 修改之后： 要么蓄冷机组平衡输出为0，蓄冷装置充能（负数），制冷机组输出（正数）全部被蓄冷装置吸收；要么制冷机组用于蓄冷的功率为0，蓄冷装置放能（正数），蓄冷机组平衡输出（正数）全部由蓄冷装置提供
        y=power_cooletStorage,
        x=linearization.add(  # （每小时）总蓄冷功率 = 水蓄冷功率 + 相变蓄冷功率
            num_hour,
            model,
            waterStorageTank.power_waterStorageTank_cool,
            phaseChangeColdWaterStorage.power_energyStorageSystem,
        ),
    )
    # 蓄热逻辑组合
    model.add_constraints(
        heatPump.power_waterSourceHeatPumps_heatStorage[h]
        + waterSourceHeatPumps.power_waterSourceHeatPumps_heatStorage[h]
        + waterStorageTank.power_waterStorageTank_heat[h]
        + phaseChangeWarmWaterStorage.power_energyStorageSystem[h]
        == power_heatStorage[
            h
        ]  # 蓄热系统功率 == (热泵蓄热功率 + 水源热泵蓄热功率) + (水蓄能设备储能功率 + 储热设备充放功率)
        for h in range(0, num_hour)
    )
    linearization.max_zeros(
        num_hour,
        model,
        # TODO: invert x/y position
        # 修改之前：要么蓄热设备不充不放，系统不产生热量；要么消耗热，热量全部由蓄热设备提供
        # 修改之后： 要么蓄热机组平衡输出为0，蓄热装置充能（负数），制热机组输出（正数）全部被蓄热装置吸收；要么制热用于蓄热的功率为0，蓄热装置放能（正数），蓄热机组平衡输出（正数）全部由蓄热装置提供
        y=power_heatStorage,
        x=linearization.add(
            num_hour,
            model,
            waterStorageTank.power_waterStorageTank_heat,
            phaseChangeWarmWaterStorage.power_energyStorageSystem,
        ),
    )
    ##########################################

    # 电量平衡
    # electricity_groundSourceHeatPump[h] + electricity_waterCoolingSpiralMachine[h] + electricity_heatPump[h] - power_batteryEnergyStorageSystem[h] - power_photoVoltaic[h] + electricity_waterSourceHeatPumps[h] + power_load[h] - power_combinedHeatAndPower[h] - power_chargeaifa[h] + \
    # power_electricSteamGenerator[h] + power_electricBoiler[h] + electricity_tripleWorkingConditionUnit[h] + electricity_doubleWorkingConditionUnit[h] == total_power[h]
    # 市政电力电流是双向的,其余市政是单向的。

    # what is "chargeaifa" ??

    # 电 供销平衡
    ##########################################

    model.add_constraints(
        groundSourceHeatPump.electricity_groundSourceHeatPump[h]
        + waterCoolingSpiralMachine.electricity_waterCoolingSpiralMachine[h]
        + heatPump.electricity_waterSourceHeatPumps[h]
        + waterSourceHeatPumps.electricity_waterSourceHeatPumps[h]
        + power_load[h]
        + electricSteamGenerator.power_electricSteamGenerator[h]
        + hotWaterElectricBoiler.electricity_electricBoiler[h]
        + tripleWorkingConditionUnit.electricity_tripleWorkingConditionUnit[h]
        + doubleWorkingConditionUnit.electricity_doubleWorkingConditionUnit[h]
        - batteryEnergyStorageSystem.power_energyStorageSystem[h]
        - photoVoltaic.power_photoVoltaic[h]
        - combinedHeatAndPower.power_combinedHeatAndPower[h]
        - dieselEngine.power_dieselEngine[h]
        == gridNet.total_power[h]  # 总的耗电量 == 用电量 - 放能量
        # 用电量 == 地源热泵每小时耗电量 + 水冷螺旋机的用电量 + 每个时刻热泵用电量 + 每个时刻水源热泵用电量 + 用电需求 + 电蒸汽发生器总功率 + 电锅炉在每个时段的电消耗量 + 三工况机组的用电量 + 双工况机组的用电量
        # 放能量 == 每小时储能装置的充放能功率 + 每个小时内光伏机组发电量 + 热电联产在每个时段的发电量 + 每个小时内柴油发电机机组发电量
        for h in range(0, num_hour)
    )
    ##########################################

    # 综合能源系统 所有设备集合
    systems = [  # all constrains in IES/IntegratedEnergySystem system
        dieselEngine,
        photoVoltaic,
        batteryEnergyStorageSystem,
        troughPhotoThermal,
        electricSteamGenerator,
        combinedHeatAndPower,  # for CHP outputs, electricity and hot_water are mandatory. steam is optional.
        gasBoiler,
        steamAndWater_exchanger,  # qs? 气水？
        steamPowered_LiBr,  # zq? 制取？
        platePhotothermal,
        phaseChangeHotWaterStorage,
        municipalHotWater,
        hotWaterElectricBoiler,
        gasBoiler_hotWater,
        waterStorageTank,
        municipalSteam,
        hotWaterLiBr,
        hotWaterExchanger,
        heatPump,
        waterSourceHeatPumps,
        waterCoolingSpiralMachine,
        tripleWorkingConditionUnit,
        doubleWorkingConditionUnit,
        groundSourceHeatPump,
        iceStorage,  # bx?
        phaseChangeColdWaterStorage,
        phaseChangeWarmWaterStorage,
        gridNet,
    ]

    check_solve_and_log(
        systems, model, simulation_name="fig"
    )  # <- assume our objective is to minimize the total annual fee.

    # # 目标值 = 所有混合能源机组年运行成本总和
    # objective = systems[0].annualized
    # for ii in range(1, len(systems)):
    #     objective += systems[ii].annualized

    # # 使得目标值最小
    # model.minimize(objective)

    # model.print_information()

    # do we have anything in conflict?
    ####
    # refiner = ConflictRefiner()  # 先实例化ConflictRefiner类
    # res = refiner.refine_conflict(model)  # 将模型导入该类,调用方法
    # res.display()  # 显示冲突约束

    # print("start calculation:")

    # # 1000秒以内解出 否则放弃
    # model.set_time_limit(time_limit=1000)

    # # 模型求解返回值 可为空
    # solution_run1: Union[None, SolveSolution] = model.solve(
    #     log_output=True
    # )  # output some solution.
    # # docplex.mp.solution.SolveSolution or None

    # if solution_run1 is None:  # 没有解出来
    #     # from docplex.mp.sdetails import SolveDetails

    #     print("NO SOLUTION.")
    # else:  # 解出来了
    #     print("objective: annual", solution_run1.get_value(objective))  # 所有设备年运行成本总和
    #     print()

    #     from data_visualize_utils import (
    #         printDecisionVariablesFromSolution,
    #         printIntegratedEnergySystemDeviceCounts,
    #         plotSingle,
    #     )

    #     printIntegratedEnergySystemDeviceCounts(systems)
    #     printDecisionVariablesFromSolution(model)

    #     value = Value(solution_run1)

    #     plotSingle(
    #         value.value(batteryEnergyStorageSystem.power_energyStorageSystem),
    #         "BatteryEnergyStorageSystem",
    #     )  #  绘制电池每小时的充放能功率

    #     database = {
    #         "electricity": {  # 发电、用电、功率相关数据
    #             "list": [
    #                 groundSourceHeatPump.electricity_groundSourceHeatPump,
    #                 waterCoolingSpiralMachine.electricity_waterCoolingSpiralMachine,
    #                 heatPump.electricity_waterSourceHeatPumps,
    #                 batteryEnergyStorageSystem.power_energyStorageSystem,
    #                 photoVoltaic.power_photoVoltaic,
    #                 waterSourceHeatPumps.electricity_waterSourceHeatPumps,
    #                 power_load,
    #                 combinedHeatAndPower.power_combinedHeatAndPower,
    #                 dieselEngine.power_dieselEngine,
    #                 electricSteamGenerator.power_electricSteamGenerator,
    #                 hotWaterElectricBoiler.electricity_electricBoiler,
    #                 tripleWorkingConditionUnit.electricity_tripleWorkingConditionUnit,
    #                 doubleWorkingConditionUnit.electricity_doubleWorkingConditionUnit,
    #                 gridNet.total_power,
    #             ],
    #             "name": [
    #                 "groundSourceHeatPump.electricity_groundSourceHeatPump",
    #                 "waterCoolingSpiralMachine.electricity_waterCoolingSpiralMachine",
    #                 "heatPump.electricity_waterSourceHeatPumps",
    #                 "batteryEnergyStorageSystem.power_energyStorageSystem",
    #                 "photoVoltaic.power_photoVoltaic",
    #                 "waterSourceHeatPumps.electricity_waterSourceHeatPumps",
    #                 "power_load",
    #                 "combinedHeatAndPower.power_combinedHeatAndPower",
    #                 "dieselEngine.power_dieselEngine",
    #                 "electricSteamGenerator.power_electricSteamGenerator",
    #                 "hotWaterElectricBoiler.electricity_electricBoiler",
    #                 "tripleWorkingConditionUnit.electricity_tripleWorkingConditionUnit",
    #                 "doubleWorkingConditionUnit.electricity_doubleWorkingConditionUnit",
    #                 "gridNet.total_power",
    #             ],
    #         },
    #         "cool": {  #  制冷相关数据
    #             "list": [
    #                 heatPump.power_waterSourceHeatPumps_cool,
    #                 power_cooletStorage,
    #                 waterSourceHeatPumps.power_waterSourceHeatPumps_cool,
    #                 steamPowered_LiBr.cool_LiBr,  # cooling? 直取？
    #                 hotWaterLiBr.cool_LiBr,
    #                 waterCoolingSpiralMachine.power_waterCoolingSpiralMachine_cool,
    #                 power_iceStorage,  # consume?
    #                 tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_cool,
    #                 doubleWorkingConditionUnit.power_doubleWorkingConditionUnit_cool,
    #             ],
    #             "name": [
    #                 "heatPump.power_waterSourceHeatPumps_cool",
    #                 "power_cooletStorage",
    #                 "waterSourceHeatPumps.power_waterSourceHeatPumps_cool",
    #                 "steamPowered_LiBr.cool_LiBr",
    #                 "hotWaterLiBr.cool_LiBr",
    #                 "waterCoolingSpiralMachine.power_waterCoolingSpiralMachine_cool",
    #                 "power_iceStorage",
    #                 "tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_cool",
    #                 "doubleWorkingConditionUnit.power_doubleWorkingConditionUnit_cool",
    #             ],
    #         },
    #         "heat": {  #  制热相关数据, warm water?
    #             "list": [
    #                 heatPump.power_waterSourceHeatPumps_heat,
    #                 power_heatStorage,
    #                 waterSourceHeatPumps.power_waterSourceHeatPumps_heat,
    #                 steamAndWater_exchanger.heat_exchange,
    #                 hotWaterExchanger.heat_exchange,
    #                 tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_heat,
    #                 groundSourceHeatPump.power_groundSourceHeatPump,
    #                 heat_load,
    #             ],
    #             "name": [
    #                 "heatPump.power_waterSourceHeatPumps_heat",
    #                 "power_heatStorage",
    #                 "waterSourceHeatPumps.power_waterSourceHeatPumps_heat",
    #                 "steamAndWater_exchanger.heat_exchange",
    #                 "hotWaterExchanger.heat_exchange",
    #                 "tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_heat",
    #                 "groundSourceHeatPump.power_groundSourceHeatPump",
    #                 "heat_load",
    #             ],
    #         },
    #         "gwheat": {  # (gas) generated or wasted heat? 高温热水？
    #             "list": [
    #                 combinedHeatAndPower.gasTurbineSystem_device.heat_exchange,
    #                 combinedHeatAndPower.wasteGasAndHeat_water_device.heat_exchange,
    #                 platePhotothermal.power_photoVoltaic,
    #                 phaseChangeHotWaterStorage.power_energyStorageSystem,
    #                 municipalHotWater.heat_citySupplied,
    #                 gasBoiler_hotWater.heat_gasBoiler,
    #                 hotWaterElectricBoiler.heat_electricBoiler,
    #                 waterStorageTank.power_waterStorageTank_gheat,
    #             ],
    #             "name": [
    #                 "combinedHeatAndPower.gasTurbineSystem_device.heat_exchangeh",
    #                 "wasteGasAndHeat_water_device.heat_exchange",
    #                 "platePhotothermal.power_photoVoltaic",
    #                 "phaseChangeHotWaterStorage.power_energyStorageSystem",
    #                 "municipalHotWater.heat_citySupplied",
    #                 "gasBoiler_hotWater.heat_gasBoiler",
    #                 "hotWaterElectricBoiler.heat_electricBoiler",
    #                 "waterStorageTank.power_waterStorageTank_gheat",
    #             ],
    #         },
    #     }

    #     # 绘制(所有?)相关数据
    #     # flag = "hotWaterLiBr.cool_LiBr" # stop here!
    #     for key, value in database.items():
    #         datalist, names = value["list"], value["name"]
    #         for data, name in zip(datalist, names):
    #             # if name == flag:
    #             #     print(data)
    #             #     print("BREAK ON:", flag)
    #             #     breakpoint()
    #             plotSingle(data, name)
