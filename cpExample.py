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
    - 综合能源系统设备所有设备的年化运维成本综合最小值,即min(初始化运维成本+各设备的年化运维成本)
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
matplotlib.rc(group="font", family="YouYuan")

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
    num_hour0,
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

power_load, cool_load, heat_load, steam_load = getPowerCoolHeatSteamLoads(num_hour0)

##########################################

# is this a test on `Linear_absolute`?

# absolute1 = Linear_absolute(model1, [-5, 6], [0, 1])
# absolute1.absolute_add_constraints(model1)

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
    # GroundSourceSteamGenerator,
    # Linear_absolute,
    # CitySupply,
    GridNet,
    Linearization,
)

if __name__ == "__main__":
    model1 = Model(name="buses")

    # 获取光照、能源价格
    ##########################################
    (
        intensityOfIllumination0,
        electricity_price0,
        gas_price0,
        municipalHotWater_price0,
        municipalSteam_price0,
    ) = getResourceData(num_hour0)
    ##########################################

    # 发电及电储能装置
    ##########################################
    dieselEngine, photoVoltaic, batteryEnergyStorageSystem = electricSystemRegistration(
        model1, num_hour0, intensityOfIllumination0, day_node
    )
    ##########################################

    # 蒸汽发生装置及参数配置
    ##########################################

    (
        troughPhotoThermal,
        groundSourceSteamGenerator,
        combinedHeatAndPower,
        gasBoiler,
        municipalSteam,
    ) = steamSourcesRegistration(
        model1,
        num_hour0,
        intensityOfIllumination0,
        # day_node,
        electricity_price0,
        gas_price0,
    )

    # 以上为蒸汽发生装置
    ##########################################

    # 高温蒸汽去向
    ##########################################
    power_steam_used_product = model1.continuous_var_list(
        [i for i in range(0, num_hour0)], name="power_steam_used_product"
    )
    power_steam_used_heatcool = model1.continuous_var_list(
        [i for i in range(0, num_hour0)], name="power_steam_used_heatcool"
    )
    power_steam_sum = model1.continuous_var_list(
        [i for i in range(0, num_hour0)], name="power_steam_sum"
    )
    model1.add_constraints(
        power_steam_sum[h]
        == municipalSteam.heat_citySupplied[h]
        + combinedHeatAndPower.wasteGasAndHeat_steam_device.heat_exchange[h]
        + troughPhotoThermal.power_troughPhotoThermal_steam[h]
        + groundSourceSteamGenerator.power_groundSourceSteamGenerator_steam[h]
        + gasBoiler.heat_gasBoiler[
            h
        ]  # （每小时）所有产生蒸汽量的总和 = 市政热量 + CHP余气余热蒸汽 + 槽式光热产蒸汽 + 燃气锅炉产生热量
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
    ##########################################

    # 高温热水发生装置及水储能装置
    ##########################################
    # highTemperatureHotWater
    # 1) combinedHeatAndPower gasTurbineSystem?
    # 2) combinedHeatAndPower wasteGasAndHeat__to_water?
    # 3

    (
        platePhotothermal,
        waterStorageTank,
        municipalHotWater,
        gasBoiler_hotWater,
        phaseChangeHeatStorage,
        hotWaterElectricBoiler,
    ) = hotWaterSourcesRegistration(
        model1,
        num_hour0,
        intensityOfIllumination0,
        day_node,
        electricity_price0,
        municipalHotWater_price0,
        gas_price0,
    )
    ##########################################

    # 高温热水合计
    power_highTemperatureHotWater_sum = model1.continuous_var_list(
        [i for i in range(0, num_hour0)], name="power_highTemperatureHotWater_sum"
    )
    model1.add_constraints(
        power_highTemperatureHotWater_sum[h]
        == combinedHeatAndPower.gasTurbineSystem_device.heat_exchange[h]
        + combinedHeatAndPower.wasteGasAndHeat_water_device.heat_exchange[
            h
        ]  # wasteGasAndHeat_？
        + platePhotothermal.power_photoVoltaic[h]
        + phaseChangeHeatStorage.power_energyStorageSystem[h]
        + municipalHotWater.heat_citySupplied[h]
        + gasBoiler_hotWater.heat_gasBoiler[h]
        + hotWaterElectricBoiler.heat_electricBoiler[h]
        + waterStorageTank.power_waterStorageTank_gheat[h]  # 水储能设备发出的热量？
        for h in range(
            0, num_hour0
        )  # 高温热水 = CHP燃气轮机热交换量 + CHP供暖热水热交换量+ 平板光热发热功率 + 相变储热装置的充放能功率 + 市政热水实际消耗 + 燃气锅炉热功率 + 电锅炉热功率 + 水蓄能设备（高温？）水储能功率
    )

    # 热水溴化锂，制冷
    hotWaterLiBr = LiBrRefrigeration(
        num_hour0, model1, LiBr_device_max=10000, device_price=1000, efficiency=0.9
    )
    hotWaterLiBr.constraints_register(model1)

    # 热水交换器，吸收热量
    hotWaterExchanger = Exchanger(
        num_hour0, model1, device_max=20000, device_price=400, k=50
    )
    hotWaterExchanger.constraints_register(model1)

    # 高温热水去向
    model1.add_constraints(
        power_highTemperatureHotWater_sum[h]
        >= hotWaterLiBr.heat_LiBr_from[h] + hotWaterExchanger.heat_exchange[h]
        for h in range(0, num_hour0)  # （每小时）高温热水总热量 >= 热水溴化锂消耗热量 + 热交换器消耗热量
    )
    model1.add_constraints(
        power_highTemperatureHotWater_sum[h] >= 0 for h in range(0, num_hour0)
    )  # （每小时）高温热水总热量>=0

    # power_heatPump[h]*heatPump_flag[h]+power_waterStorageTank[h]*waterStorageTank_flag[h]+power_waterCoolingSpiralMachine[h]*waterSourceHeatPumps_flag[h]+power_LiBr[h]+power_waterCoolingSpiralMachine[h]+power_iceStorage[h]==cool_load[h]%冷量需求
    # power_heatPump[h]*(1-heatPump_flag[h])+power_waterStorageTank[h]*(1-waterStorageTank_flag[h])+power_waterSourceHeatPumps[h]*(1-waterSourceHeatPumps_flag[h])+power_gas[h]+power_groundSourceHeatPump[h]==heat_load[h]%热量需求
    # 采用线性化技巧,处理为下面的约束.基于每种设备要么制热,要么制冷。
    # 供冷:风冷heatPump groundSourceHeatPump 蓄能水罐 hotWaterLiBr机组 蒸汽LiBr机组 phaseChangeRefrigerantStorage
    # 供热:风冷heatPump groundSourceHeatPump 蓄能水罐 地热 水水Exchanger传热
    # heatPump = AirHeatPump(num_hour0, model1, device_max=10000, device_price=1000, electricity_price=electricity_price0)
    # heatPump.constraints_register(model1)

    # 冷 热 冰 供给储存消耗平衡
    ##########################################
    from demo_utils import cooletIceHeatDevicesRegistration

    (
        heatPump,
        waterSourceHeatPumps,
        waterCoolingSpiralMachine,
        tripleWorkingConditionUnit,
        doubleWorkingConditionUnit,
        groundSourceHeatPump,
        iceStorage,
        phaseChangeRefrigerantStorage,
        lowphaseChangeHeatStorage,
    ) = cooletIceHeatDevicesRegistration(
        model1,
        num_hour0,
        electricity_price0,
    )

    # 产能储能机组平衡输出功率
    ###########
    power_cooletStorage = model1.continuous_var_list(
        [i for i in range(0, num_hour0)], name="power_cooletStorage"
    )
    power_heatStorge = model1.continuous_var_list(
        [i for i in range(0, num_hour0)], name="power_heatStorge"
    )
    power_iceStorage = model1.continuous_var_list(
        [i for i in range(0, num_hour0)], name="power_iceStorage"
    )
    ###########

    # power_heatPump_cool[h]+power_cooletStorage[h]+power_waterSourceHeatPumps_cool[h]+power_zqLiBr[h]+power_hotWaterLiBr[h]+power_waterCoolingSpiralMachine_cool[h]+power_ice[h]+power_tripleWorkingConditionUnit_cool[h]+power_doubleWorkingConditionUnit_cool[h]==cool_load[h]%冷量需求

    # what is "_x"?
    model1.add_constraints(
        heatPump.power_waterSourceHeatPumps_cool[h]
        + power_cooletStorage[h]
        + waterSourceHeatPumps.power_waterSourceHeatPumps_cool[h]
        + steamPowered_LiBr.cool_LiBr[h]
        + hotWaterLiBr.cool_LiBr[h]
        + waterCoolingSpiralMachine.power_waterCoolingSpiralMachine_cool[h]
        + power_iceStorage[h]
        + tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_cool[h]
        + doubleWorkingConditionUnit.power_doubleWorkingConditionUnit_cool[h]
        == cool_load[
            h
        ]  # 冷量需求 = 热泵制冷功率 + 蓄冷机组平衡输出 + 水源热泵制冷功率 + 蒸汽溴化锂机组制冷量 + 热水溴化锂机组制冷量 + 水冷螺旋机的制冷功率 + 蓄冰机组平衡输出 + 三工况机组的制冷功率 + 双工况机组的制冷功率
        for h in range(0, num_hour0)
    )
    # power_heatPump_heat[h]+power_heatStorge[h]+power_waterSourceHeatPumps_heat[h]+power_gas_heat[h]+power_ss_heat[h]+power_groundSourceHeatPump[h]+power_tripleWorkingConditionUnit_heat[h]==heat_load[h]%热量需求
    model1.add_constraints(
        heatPump.power_waterSourceHeatPumps_heat[h]
        + power_heatStorge[h]
        + waterSourceHeatPumps.power_waterSourceHeatPumps_heat[h]
        + steamAndWater_exchanger.heat_exchange[h]
        + hotWaterExchanger.heat_exchange[h]
        + tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_heat[h]
        + groundSourceHeatPump.power_groundSourceHeatPump[h]
        == heat_load[
            h
        ]  # 热量需求 = 热泵制热功率 + 蓄热机组平衡输出 + 水源热泵制热功率 + 汽水热交换量 + 热水热交换量 + 三工况机组的制热功率 + 地源热泵输出功率
        for h in range(0, num_hour0)
    )
    # 冰蓄冷逻辑组合
    model1.add_constraints(
        tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_ice[h]
        + doubleWorkingConditionUnit.power_doubleWorkingConditionUnit_ice[h]
        + iceStorage.power_energyStorageSystem[h]
        == power_iceStorage[h]  # 蓄冰机组平衡输出 = 三工况机组的制冰功率 + 双工况机组的制冰功率 + 冰蓄能充放能功率
        for h in range(0, num_hour0)
    )
    linearization = Linearization()
    #
    linearization.max_zeros(
        # TODO: invert x/y position
        # 修改之前： 要么冰蓄冷功率为0，冰蓄能装置不充不放; 要么冰蓄冷功率等于蓄冷装置充放功率（此时冰蓄能释放能量）
        # 修改之后： 要么蓄冰机组平衡输出为0，冰蓄能装置充能（负数），制冰机组输出（正数）全部被冰蓄能装置吸收；要么制冰机组用于蓄冰的功率为0，冰蓄能装置放能（正数），蓄冰机组平衡输出（正数）全部由冰蓄能装置提供
        num_hour0,
        model1,
        y=power_iceStorage,
        x=iceStorage.power_energyStorageSystem,
    )

    # 蓄冷逻辑组合
    model1.add_constraints(
        heatPump.power_waterSourceHeatPumps_cooletStorage[h]
        + waterSourceHeatPumps.power_waterSourceHeatPumps_cooletStorage[h]
        + waterCoolingSpiralMachine.power_waterCoolingSpiralMachine_cooletStorage[h]
        + waterStorageTank.power_waterStorageTank_cool[h]
        + phaseChangeRefrigerantStorage.power_energyStorageSystem[h]
        == power_cooletStorage[
            h
        ]  # 蓄冷系统平衡功率 = 热泵蓄冷功率 + 水源热泵蓄冷功率 + 水冷螺旋机的蓄冷功率 + 水蓄能设备蓄冷充放功率 + 相变蓄冷设备充放功率
        for h in range(0, num_hour0)
    )
    linearization.max_zeros(
        num_hour0,
        model1,
        # TODO: invert x/y position
        # 修改之前：要么蓄冷设备不充不放，系统不产生冷量；要么消耗冷，冷量全部由蓄冷设备提供
        # 修改之后： 要么蓄冷机组平衡输出为0，蓄冷装置充能（负数），制冷机组输出（正数）全部被蓄冷装置吸收；要么制冷机组用于蓄冷的功率为0，蓄冷装置放能（正数），蓄冷机组平衡输出（正数）全部由蓄冷装置提供
        y=power_cooletStorage,
        x=linearization.add(  # （每小时）总蓄冷功率 = 水蓄冷功率 + 相变蓄冷功率
            num_hour0,
            model1,
            waterStorageTank.power_waterStorageTank_cool,
            phaseChangeRefrigerantStorage.power_energyStorageSystem,
        ),
    )
    # 蓄热逻辑组合
    model1.add_constraints(
        heatPump.power_waterSourceHeatPumps_heatStorge[h]
        + waterSourceHeatPumps.power_waterSourceHeatPumps_heatStorge[h]
        + waterStorageTank.power_waterStorageTank_heat[h]
        + lowphaseChangeHeatStorage.power_energyStorageSystem[h]
        == power_heatStorge[h]  # 蓄热系统功率 = 热泵蓄热功率 + 水源热泵蓄热功率 + 水蓄能设备储能功率 + 储热设备充放功率
        for h in range(0, num_hour0)
    )
    linearization.max_zeros(
        num_hour0,
        model1,
        # TODO: invert x/y position
        # 修改之前：要么蓄热设备不充不放，系统不产生热量；要么消耗热，热量全部由蓄热设备提供
        # 修改之后： 要么蓄热机组平衡输出为0，蓄热装置充能（负数），制热机组输出（正数）全部被蓄热装置吸收；要么制热用于蓄热的功率为0，蓄热装置放能（正数），蓄热机组平衡输出（正数）全部由蓄热装置提供
        y=power_heatStorge,
        x=linearization.add(
            num_hour0,
            model1,
            waterStorageTank.power_waterStorageTank_heat,
            lowphaseChangeHeatStorage.power_energyStorageSystem,
        ),
    )
    ##########################################

    # 电量平衡
    # electricity_groundSourceHeatPump[h] + electricity_waterCoolingSpiralMachine[h] + electricity_heatPump[h] - power_batteryEnergyStorageSystem[h] - power_photoVoltaic[h] + electricity_waterSourceHeatPumps[h] + power_load[h] - power_combinedHeatAndPower[h] - power_chargeaifa[h] + \
    # power_groundSourceSteamGenerator[h] + power_electricBoiler[h] + electricity_tripleWorkingConditionUnit[h] + electricity_doubleWorkingConditionUnit[h] == total_power[h]
    # 市政电力电流是双向的,其余市政是单向的。

    # what is "chargeaifa" ??

    # 电 供销平衡
    ##########################################

    # 电网
    gridNet = GridNet(
        num_hour0,
        model1,
        gridNet_device_max=200000,
        device_price=0,
        electricity_price_from=electricity_price0,
        electricity_price_to=0.35,
    )
    gridNet.constraints_register(model1, powerPeak_pre=2000)

    model1.add_constraints(
        groundSourceHeatPump.electricity_groundSourceHeatPump[h]
        + waterCoolingSpiralMachine.electricity_waterCoolingSpiralMachine[h]
        + heatPump.electricity_waterSourceHeatPumps[h]
        + waterSourceHeatPumps.electricity_waterSourceHeatPumps[h]
        + power_load[h]
        + groundSourceSteamGenerator.power_groundSourceSteamGenerator[h]
        + hotWaterElectricBoiler.electricity_electricBoiler[h]
        + tripleWorkingConditionUnit.electricity_tripleWorkingConditionUnit[h]
        + doubleWorkingConditionUnit.electricity_doubleWorkingConditionUnit[h]
        - batteryEnergyStorageSystem.power_energyStorageSystem[h]
        - photoVoltaic.power_photoVoltaic[h]
        - combinedHeatAndPower.power_combinedHeatAndPower[h]
        - dieselEngine.power_dieselEngine[h]
        == gridNet.total_power[h]  # 总的耗电量 = 用电量 - 放能量
        # 用电量 = 地源热泵每小时耗电量+水冷螺旋机的用电量+每个时刻热泵用电量+每个时刻水源热泵用电量+用电需求+地源蒸汽发生器总功率+电锅炉在每个时段的电消耗量+三工况机组的用电量+双工况机组的用电量
        # 放能量 = 每小时储能装置的充放能功率+每个小时内光伏机组发电量+热电联产在每个时段的发电量+每个小时内柴油发电机机组发电量
        for h in range(0, num_hour0)
    )
    ##########################################

    # 综合能源系统 所有设备集合
    integratedEnergySystem_device = (
        [  # all constrains in IES/IntegratedEnergySystem system
            dieselEngine,
            photoVoltaic,
            batteryEnergyStorageSystem,
            troughPhotoThermal,
            groundSourceSteamGenerator,
            combinedHeatAndPower,
            gasBoiler,
            steamAndWater_exchanger,  # qs? 气水？
            steamPowered_LiBr,  # zq? 制取？
            platePhotothermal,
            phaseChangeHeatStorage,
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
            iceStorage,  # ?
            phaseChangeRefrigerantStorage,
            lowphaseChangeHeatStorage,
            gridNet,
        ]
    )

    # 目标值 = 所有混合能源机组年运行成本总和
    objective = integratedEnergySystem_device[0].annualized
    for ii in range(1, len(integratedEnergySystem_device)):
        objective = objective + integratedEnergySystem_device[ii].annualized

    # 使得目标值最小
    model1.minimize(objective)

    model1.print_information()

    # do we have anything in conflict?
    ####
    # refiner = ConflictRefiner()  # 先实例化ConflictRefiner类
    # res = refiner.refine_conflict(model1)  # 将模型导入该类,调用方法
    # res.display()  # 显示冲突约束

    print("start calculation:")

    # 1000秒以内解出 否则放弃
    model1.set_time_limit(time_limit=1000)

    # 模型求解返回值 可为空
    solution_run1: Union[None, SolveSolution] = model1.solve(
        log_output=True
    )  # output some solution.
    # docplex.mp.solution.SolveSolution or None

    if solution_run1 is None:  # 没有解出来
        # from docplex.mp.sdetails import SolveDetails

        print("NO SOLUTION.")
    else:  # 解出来了
        print("objective: annual", solution_run1.get_value(objective))  # 所有设备年运行成本总和
        print()

        from data_visualize_utils import (
            printDecisionVariablesFromSolution,
            printIntegratedEnergySystemDeviceCounts,
            plotSingle,
        )

        printIntegratedEnergySystemDeviceCounts(integratedEnergySystem_device)
        printDecisionVariablesFromSolution(model1)

        value = Value(solution_run1)

        plotSingle(
            value.value(batteryEnergyStorageSystem.power_energyStorageSystem),
            "BatteryEnergyStorageSystem",
        )  #  绘制电池每小时的充放能功率

        database = {
            "electricity": {  # 发电、用电、功率相关数据
                "list": [
                    groundSourceHeatPump.electricity_groundSourceHeatPump,
                    waterCoolingSpiralMachine.electricity_waterCoolingSpiralMachine,
                    heatPump.electricity_waterSourceHeatPumps,
                    batteryEnergyStorageSystem.power_energyStorageSystem,
                    photoVoltaic.power_photoVoltaic,
                    waterSourceHeatPumps.electricity_waterSourceHeatPumps,
                    power_load,
                    combinedHeatAndPower.power_combinedHeatAndPower,
                    dieselEngine.power_dieselEngine,
                    groundSourceSteamGenerator.power_groundSourceSteamGenerator,
                    hotWaterElectricBoiler.electricity_electricBoiler,
                    tripleWorkingConditionUnit.electricity_tripleWorkingConditionUnit,
                    doubleWorkingConditionUnit.electricity_doubleWorkingConditionUnit,
                    gridNet.total_power,
                ],
                "name": [
                    "groundSourceHeatPump.electricity_groundSourceHeatPump",
                    "waterCoolingSpiralMachine.electricity_waterCoolingSpiralMachine",
                    "heatPump.electricity_waterSourceHeatPumps",
                    "batteryEnergyStorageSystem.power_energyStorageSystem",
                    "photoVoltaic.power_photoVoltaic",
                    "waterSourceHeatPumps.electricity_waterSourceHeatPumps",
                    "power_load",
                    "combinedHeatAndPower.power_combinedHeatAndPower",
                    "dieselEngine.power_dieselEngine",
                    "groundSourceSteamGenerator.power_groundSourceSteamGenerator",
                    "hotWaterElectricBoiler.electricity_electricBoiler",
                    "tripleWorkingConditionUnit.electricity_tripleWorkingConditionUnit",
                    "doubleWorkingConditionUnit.electricity_doubleWorkingConditionUnit",
                    "gridNet.total_power",
                ],
            },
            "cool": {  #  制冷相关数据
                "list": [
                    heatPump.power_waterSourceHeatPumps_cool,
                    power_cooletStorage,
                    waterSourceHeatPumps.power_waterSourceHeatPumps_cool,
                    steamPowered_LiBr.cool_LiBr,  # cooling? 直取？
                    hotWaterLiBr.cool_LiBr,
                    waterCoolingSpiralMachine.power_waterCoolingSpiralMachine_cool,
                    power_iceStorage,  # consume?
                    tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_cool,
                    doubleWorkingConditionUnit.power_doubleWorkingConditionUnit_cool,
                ],
                "name": [
                    "heatPump.power_waterSourceHeatPumps_cool",
                    "power_cooletStorage",
                    "waterSourceHeatPumps.power_waterSourceHeatPumps_cool",
                    "steamPowered_LiBr.cool_LiBr",
                    "hotWaterLiBr.cool_LiBr",
                    "waterCoolingSpiralMachine.power_waterCoolingSpiralMachine_cool",
                    "power_iceStorage",
                    "tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_cool",
                    "doubleWorkingConditionUnit.power_doubleWorkingConditionUnit_cool",
                ],
            },
            "heat": {  #  制热相关数据
                "list": [
                    heatPump.power_waterSourceHeatPumps_heat,
                    power_heatStorge,
                    waterSourceHeatPumps.power_waterSourceHeatPumps_heat,
                    steamAndWater_exchanger.heat_exchange,
                    hotWaterExchanger.heat_exchange,
                    tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_heat,
                    groundSourceHeatPump.power_groundSourceHeatPump,
                    heat_load,
                ],
                "name": [
                    "heatPump.power_waterSourceHeatPumps_heat",
                    "power_heatStorge",
                    "waterSourceHeatPumps.power_waterSourceHeatPumps_heat",
                    "steamAndWater_exchanger.heat_exchange",
                    "hotWaterExchanger.heat_exchange",
                    "tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_heat",
                    "groundSourceHeatPump.power_groundSourceHeatPump",
                    "heat_load",
                ],
            },
            "gwheat": {  # (gas) generated or wasted heat? 高温热水？
                "list": [
                    combinedHeatAndPower.gasTurbineSystem_device.heat_exchange,
                    combinedHeatAndPower.wasteGasAndHeat_water_device.heat_exchange,
                    platePhotothermal.power_photoVoltaic,
                    phaseChangeHeatStorage.power_energyStorageSystem,
                    municipalHotWater.heat_citySupplied,
                    gasBoiler_hotWater.heat_gasBoiler,
                    hotWaterElectricBoiler.heat_electricBoiler,
                    waterStorageTank.power_waterStorageTank_gheat,
                ],
                "name": [
                    "combinedHeatAndPower.gasTurbineSystem_device.heat_exchangeh",
                    "wasteGasAndHeat_water_device.heat_exchange",
                    "platePhotothermal.power_photoVoltaic",
                    "phaseChangeHeatStorage.power_energyStorageSystem",
                    "municipalHotWater.heat_citySupplied",
                    "gasBoiler_hotWater.heat_gasBoiler",
                    "hotWaterElectricBoiler.heat_electricBoiler",
                    "waterStorageTank.power_waterStorageTank_gheat",
                ],
            },
        }

        # 绘制(所有?)相关数据
        for key, value in database.items():
            datalist, names = value["list"], value["name"]
            for data, name in zip(datalist, names):
                plotSingle(data, name)
