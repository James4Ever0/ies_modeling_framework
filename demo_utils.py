"""
样例模块
"""

import numpy as np
import os
import math


class LoadGet(object):
    """
    获取逐小时冷、热、电、蒸汽负荷数据
    """

    def get_cool_load(self, num_hour: int) -> np.ndarray:
        """
        获取逐小时冷负荷数据

        Args:
            num_hour (int): 一天小时数

        Return:
            常数冷负荷数组 数组形状是`(num_hour,)` 元素全为`10000`
        """
        cool_load = np.ones(num_hour, dtype=float) * 10000
        return cool_load

    def get_heat_load(self, num_hour: int) -> np.ndarray:
        """
        获取逐小时热负荷数据

        Args:
            num_hour (int): 一天小时数

        Return:
            常数热负荷数组 数组形状是`(num_hour,)` 元素全为`10000`
        """
        heat_load = np.ones(num_hour, dtype=float) * 10000
        return heat_load

    def get_power_load(self, num_hour: int) -> np.ndarray:
        """
        获取逐小时电负荷数据

        Args:
            num_hour (int): 一天小时数

        Return:
            常数电负荷数组 数组形状是`(num_hour,)` 元素全为`10000`
        """
        power_load = np.ones(num_hour, dtype=float) * 10000
        return power_load

    def get_steam_load(self, num_hour: int) -> np.ndarray:
        """
        获取逐小时蒸汽负荷数据

        Args:
            num_hour (int): 一天小时数

        Return:
            常数蒸汽负荷数组 数组形状是`(num_hour,)` 元素全为`10000`
        """
        steam_load = np.ones(num_hour, dtype=float) * 10000
        return steam_load


class ResourceGet(object):
    """
    获取光照资源、电价、燃气价格、蒸汽价格
    """

    # 光照资源,超过一年的,将一年数据进行重复
    # light intensity ranging from 0 to 1? not even reaching 0.3
    def get_radiation(self, path: str, num_hour: int) -> np.ndarray:
        """
        从numpy二维数列文件加载每小时光照资源,如果需要超过一年光照资源数据,将第一年数据进行重复堆叠

        Args:
            path (str): 用于给出完整的文件路径
            num_hour (int): 一天小时数

        Return:
            intensityOfIllumination (np.array): 逐小时光照强度数据,数组形状为`(num_hour,)`
        """
        if os.path.exists(path):
            raw_file = np.loadtxt(path, dtype=float)
            radiation = raw_file[:, 0]
            intensityOfIllumination1 = radiation
            for loop in range(
                1, math.ceil(num_hour / 8760)
            ):  # if num_hour=24, then this is 1/365, we are not undergoing this process.
                intensityOfIllumination1 = np.concatenate(  # repeating the intensity of illumination if num_hour is longer than 8760
                    (intensityOfIllumination1, radiation), axis=0
                )

            intensityOfIllumination2 = (
                intensityOfIllumination1[0:num_hour] / 1000
            )  # 转化为kW, divide by one thousand
            # also strip redundant data.
            return intensityOfIllumination2  # shape: 1d array.
        else:
            raise Exception("File not extists.")

    def get_electricity_price(self, num_hour: int) -> np.ndarray:
        """
        一天不同小时的电价

        Args:
            num_hour (int): 一天小时数

        Return:
            常数电价数组 数组形状是`(num_hour,)` 元素全为`0.5`
        """
        electricity_price = np.ones(num_hour, dtype=float) * 0.5
        return electricity_price

    def get_gas_price(self, num_hour: int) -> np.ndarray:
        """
        一天不同小时的燃气价格

        Args:
            num_hour (int): 一天小时数

        Return:
            常数燃气价格数组 数组形状是`(num_hour,)` 元 元素全为`2.77`
        """
        gas_price = np.ones(num_hour, dtype=float) * 2.77
        return gas_price

    def get_municipalHotWater_price(self, num_hour: int) -> np.ndarray:
        """
        一天不同小时的热水价格

        Args:
            num_hour (int): 一天小时数

        Return:
            常数热水价格数组 数组形状是`(num_hour,)` 元素全为`0.3`
        """
        municipalHotWater_price = np.ones(num_hour, dtype=float) * 0.3
        return municipalHotWater_price

    def get_municipalSteam_price(self, num_h: int) -> np.ndarray:
        """
        一天不同小时的蒸汽价格

        Args:
            num_hour (int): 一天小时数

        Return:
            常数蒸气价格数组 数组形状是`(num_hour,)` 元素全为`0.3`
        """
        municipalSteam = np.ones(num_h, dtype=float) * 0.3
        return municipalSteam


def getPowerCoolHeatSteamLoads(num_hour: int):
    """
    获取电力、供冷、供热、蒸汽负荷数据

    Args:
        num_hour (int): 一天小时数

    Return:
        电力、供冷、供热、蒸汽负荷数据
    """
    load = LoadGet()
    power_load = load.get_power_load(num_hour)
    cool_load = load.get_power_load(num_hour)
    heat_load = load.get_power_load(num_hour)
    steam_load = load.get_power_load(num_hour)
    return power_load, cool_load, heat_load, steam_load


from typing import Union, List


def getResourceData(num_hour: int):
    """
    获取光照、能源价格

    Args:
        num_hour (int): 一天小时数

    Return:
        光照、能源价格
    """

    resource = ResourceGet()
    # model_input
    intensityOfIllumination: Union[np.ndarray, List] = resource.get_radiation(
        "jinan_changqing-hour.dat", num_hour  # 光照、风速
    )
    # what is the output? break here.
    electricity_price0 = resource.get_electricity_price(num_hour)
    gas_price0 = resource.get_gas_price(num_hour)
    # TODO: 按面积、人数计价热水消耗
    municipalHotWater_price0 = resource.get_municipalHotWater_price(num_hour)
    municipalSteam_price0 = resource.get_municipalSteam_price(num_hour)
    return (
        intensityOfIllumination,
        electricity_price0,
        gas_price0,
        municipalHotWater_price0,
        municipalSteam_price0,
    )


from integratedEnergySystemPrototypes import (
    # IntegratedEnergySystem,
    PhotoVoltaic,
    LiBrRefrigeration,
    DieselEngine,
    EnergyStorageSystem,
    # EnergyStorageSystemVariable,
    TroughPhotoThermal,
    CombinedHeatAndPower,
    GasBoiler,
    ElectricBoiler,
    Exchanger,
    # AirHeatPump,
    WaterHeatPump,
    WaterCoolingSpiral,
    DoubleWorkingConditionUnit,
    TripleWorkingConditionUnit,
    GeothermalHeatPump,
    WaterEnergyStorage,
    ElectricSteamGenerator,
    # Linear_absolute,
    CitySupply,
    GridNet,
    Linearization,
)

from docplex.mp.model import Model


def electricSystemRegistration(
    model: Model,
    num_hour: int,
    intensityOfIllumination: np.ndarray,
    day_node: int,
    debug: bool = False,
):
    """ """

    # 柴油发电机
    dieselEngine = DieselEngine(
        num_hour,
        model,
        device_count_max=320,
        device_price=750,
        running_price=2,
        debug=debug,
    )
    dieselEngine.constraints_register()

    # 光伏
    photoVoltaic = PhotoVoltaic(
        num_hour,
        model,
        device_count_max=5000,
        device_price=4500,
        intensityOfIllumination=intensityOfIllumination,
        efficiency=0.8,
        device_name="PhotoVoltaic",
        debug=debug,
        output_type="electricity",
    )
    photoVoltaic.constraints_register()

    # 电池储能
    batteryEnergyStorageSystem = EnergyStorageSystem(
        num_hour,
        model,
        device_count_max=20000,
        device_price=1800,
        device_price_powerConversionSystem=250,
        conversion_rate_max=2,
        efficiency=0.9,
        energy_init=1,
        stateOfCharge_min=0,  # state of charge
        stateOfCharge_max=1,
        device_name="batteryEnergyStorageSystem",
        debug=debug,
        input_type="electricity",
        output_type="electricity",
    )
    # original: battery
    batteryEnergyStorageSystem.constraints_register(
        register_period_constraints=1, day_node=day_node
    )
    return dieselEngine, photoVoltaic, batteryEnergyStorageSystem


def steamSourcesRegistration(
    model: Model,
    num_hour: int,
    intensityOfIllumination: np.ndarray,
    # day_node: int,
    electricity_price0: np.ndarray,
    gas_price0: np.ndarray,
    debug: bool = False,
):
    """ """

    # 槽式光热设备
    troughPhotoThermal = TroughPhotoThermal(
        num_hour,
        model,
        device_count_max=5000,
        device_price=2000,
        device_price_solidHeatStorage=1000,
        intensityOfIllumination=intensityOfIllumination,
        efficiency=0.8,
        debug=debug,
    )
    troughPhotoThermal.constraints_register()

    # 电用蒸汽发生器
    electricSteamGenerator = ElectricSteamGenerator(
        num_hour,
        model,
        device_count_max=20000,
        device_price=200,
        device_price_solidHeatStorage=200,  # gtxr? SolidHeatStorage？
        electricity_price=electricity_price0*0, # use gridnet?
        efficiency=0.9,
        debug=debug,
    )
    electricSteamGenerator.constraints_register()

    # 热电联产机组
    combinedHeatAndPower = CombinedHeatAndPower(
        num_hour,
        model,
        device_count_max=5,
        device_price=2000,
        gas_price=gas_price0,
        rated_power=2000,
        electricity_to_heat_ratio=1.2,  # dr? 电热?
        debug=debug,
    )
    combinedHeatAndPower.constraints_register()

    # 燃气锅炉
    gasBoiler = GasBoiler(
        num_hour,
        model,
        device_count_max=5000,
        device_price=200,
        gas_price=gas_price0,
        efficiency=0.9,
        debug=debug,
        output_type="steam",
    )
    gasBoiler.constraints_register()

    # 市政蒸汽
    municipalSteam = CitySupply(
        num_hour,
        model,
        device_count_max=5000,
        device_price=3000,
        running_price=0.3 * np.ones(num_hour),
        efficiency=0.9,
        device_name="municipalSteam",
        debug=debug,
        output_type="steam",
    )
    municipalSteam.constraints_register()
    return (
        troughPhotoThermal,
        electricSteamGenerator,
        combinedHeatAndPower,
        gasBoiler,
        municipalSteam,
    )


def hotWaterSourcesRegistration(
    model: Model,
    num_hour: int,
    intensityOfIllumination: np.ndarray,
    day_node: int,
    electricity_price0: np.ndarray,
    municipalHotWater_price0: np.ndarray,
    gas_price0: np.ndarray,
    debug: bool = False,
):
    """"""

    # 平板光热
    platePhotothermal = PhotoVoltaic(
        num_hour,
        model,
        device_count_max=10000,
        device_price=500,
        intensityOfIllumination=intensityOfIllumination,
        efficiency=0.8,
        device_name="platePhotothermal",
        debug=debug,
        output_type="hot_water",
    )  # platePhotothermal
    platePhotothermal.constraints_register()

    # 相变蓄热
    phaseChangeHotWaterStorage = EnergyStorageSystem(
        num_hour,
        model,
        device_count_max=10000,
        device_price=350,
        device_price_powerConversionSystem=1000,  # free conversion?
        conversion_rate_max=0.5,
        efficiency=0.9,
        energy_init=0,
        stateOfCharge_min=0,
        stateOfCharge_max=1,
        device_name="phaseChangeHotWaterStorage",
        debug=debug,
        input_type="hot_water",
        output_type="hot_water",
    )
    phaseChangeHotWaterStorage.constraints_register()

    # 市政热水
    municipalHotWater = CitySupply(
        num_hour,
        model,
        device_count_max=10000,
        device_price=3000,
        running_price=municipalHotWater_price0,
        efficiency=0.9,
        device_name="municipalHotWater",
        debug=debug,
        output_type="hot_water",
    )
    municipalHotWater.constraints_register()

    # 热水电锅炉
    hotWaterElectricBoiler = ElectricBoiler(  # connect to our powergrid.
        num_hour,
        model,
        device_count_max=10000,
        device_price=200,
        electricity_price=electricity_price0 * 0,
        efficiency=0.9,
        device_name="hotWaterElectricBoiler",
        debug=debug,
        output_type="hot_water",
    )
    hotWaterElectricBoiler.constraints_register()

    # 燃气热水器
    gasBoiler_hotWater = GasBoiler(
        num_hour,
        model,
        device_count_max=20000,
        device_price=200,
        gas_price=gas_price0,
        efficiency=0.9,
        device_name="gasBoiler_hotWater",
        debug=debug,
        output_type="hot_water",
    )
    gasBoiler_hotWater.constraints_register()

    # 水储能罐
    waterStorageTank = WaterEnergyStorage(
        num_hour,
        model,
        volume_max=10000,
        volume_price=300,
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
    waterStorageTank.constraints_register(
        register_period_constraints=1, day_node=day_node
    )

    return (
        platePhotothermal,
        waterStorageTank,
        municipalHotWater,
        gasBoiler_hotWater,
        phaseChangeHotWaterStorage,
        hotWaterElectricBoiler,
    )


def cooletIceHeatDevicesRegistration(
    model: Model,
    num_hour: int,
    # intensityOfIllumination: np.ndarray,
    # day_node: int,
    electricity_price0: np.ndarray,
    # municipalHotWater_price0: np.ndarray,
    # gas_price0: np.ndarray,
    debug: bool = False,
):
    """"""

    # 热泵
    heatPump = WaterHeatPump(
        num_hour,
        model,
        device_count_max=20000,
        device_price=1000,
        electricity_price=electricity_price0*0,
        case_ratio=np.array([1, 1, 1, 1]),  # total four cases?
        device_name="heatPump",
        debug=debug,
    )
    heatPump.constraints_register()

    # 水源热泵
    waterSourceHeatPump = WaterHeatPump(
        num_hour,
        model,
        device_count_max=2000,
        device_price=3000,
        electricity_price=electricity_price0*0,
        case_ratio=np.ones(4),
        device_name="waterSourceHeatPump",
        debug=debug,
    )
    waterSourceHeatPump.constraints_register()

    # 水冷螺旋机
    waterCoolingSpiralMachine = WaterCoolingSpiral(
        num_hour,
        model,
        device_count_max=2000,
        device_price=1000,
        electricity_price=electricity_price0*0,
        case_ratio=np.array([1, 0.8]),
        debug=debug,
    )
    waterCoolingSpiralMachine.constraints_register()

    # 三工况机组
    tripleWorkingConditionUnit = TripleWorkingConditionUnit(
        num_hour,
        model,
        device_count_max=20000,
        device_price=1000,
        electricity_price=electricity_price0*0,
        case_ratio=[1, 0.8, 0.8],
        debug=debug,
    )
    tripleWorkingConditionUnit.constraints_register()

    # 双工况机组
    doubleWorkingConditionUnit = DoubleWorkingConditionUnit(
        num_hour,
        model,
        device_count_max=20000,
        device_price=1000,
        electricity_price=electricity_price0*0,
        case_ratio=[1, 0.8],
        debug=debug,
    )
    doubleWorkingConditionUnit.constraints_register()

    # 地源热泵
    groundSourceHeatPump = GeothermalHeatPump(
        num_hour,
        model,
        device_count_max=20000,
        device_price=40000,
        electricity_price=electricity_price0*0,
        debug=debug,
    )
    groundSourceHeatPump.constraints_register()

    # 电池？保鲜？相变？冰蓄能？
    iceStorage = EnergyStorageSystem(  # what is this?
        num_hour,
        model,
        device_count_max=20000,
        device_price=300,
        device_price_powerConversionSystem=1,
        conversion_rate_max=0.5,
        efficiency=0.9,
        energy_init=1,
        stateOfCharge_min=0,
        stateOfCharge_max=1,
        device_name="iceStorage",
        debug=debug,
        input_type="ice",
        output_type="cold_water",
    )
    iceStorage.constraints_register()

    # 相变蓄冷
    phaseChangeColdWaterStorage = EnergyStorageSystem(
        num_hour,
        model,
        device_count_max=20000,
        device_price=500,
        device_price_powerConversionSystem=1,
        conversion_rate_max=0.5,
        efficiency=0.9,
        energy_init=1,
        stateOfCharge_min=0,
        stateOfCharge_max=1,
        device_name="phaseChangeColdWaterStorage",
        debug=debug,
        input_type="cold_water_storage",
        output_type="cold_water",
    )
    phaseChangeColdWaterStorage.constraints_register()

    # TODO: 修改为：低温水 相变蓄热
    phaseChangeWarmWaterStorage = EnergyStorageSystem(
        num_hour,
        model,
        device_count_max=20000,
        device_price=300,
        device_price_powerConversionSystem=1,
        conversion_rate_max=0.5,
        efficiency=0.9,
        energy_init=1,
        stateOfCharge_min=0,
        stateOfCharge_max=1,
        device_name="phaseChangeWarmWaterStorage",
        debug=debug,
        input_type="warm_water_storage",
        output_type="warm_water",
    )
    phaseChangeWarmWaterStorage.constraints_register()

    return (
        heatPump,
        waterSourceHeatPump,
        waterCoolingSpiralMachine,
        tripleWorkingConditionUnit,
        doubleWorkingConditionUnit,
        groundSourceHeatPump,
        iceStorage,
        phaseChangeColdWaterStorage,
        phaseChangeWarmWaterStorage,
    )
