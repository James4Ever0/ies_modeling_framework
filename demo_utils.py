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


def getPowerCoolHeatSteamLoads(num_hour0: int):
    """
    获取电力、供冷、供热、蒸汽负荷数据

    Args:
        num_hour0 (int): 一天小时数

    Return:
        电力、供冷、供热、蒸汽负荷数据
    """
    load = LoadGet()
    power_load = load.get_power_load(num_hour0)
    cool_load = load.get_power_load(num_hour0)
    heat_load = load.get_power_load(num_hour0)
    steam_load = load.get_power_load(num_hour0)
    return power_load, cool_load, heat_load, steam_load


from typing import Union, List


def getResourceData(num_hour0: int):
    """
    获取光照、能源价格

    Args:
        num_hour0 (int): 一天小时数

    Return:
        光照、能源价格
    """

    resource = ResourceGet()
    # model_input
    intensityOfIllumination0: Union[np.ndarray, List] = resource.get_radiation(
        "jinan_changqing-hour.dat", num_hour0
    )
    # what is the output? break here.
    electricity_price0 = resource.get_electricity_price(num_hour0)
    gas_price0 = resource.get_gas_price(num_hour0)
    municipalHotWater_price0 = resource.get_municipalHotWater_price(num_hour0)
    municipalSteam_price0 = resource.get_municipalSteam_price(num_hour0)
    return (
        intensityOfIllumination0,
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
    GroundSourceSteamGenerator,
    # Linear_absolute,
    CitySupply,
    GridNet,
    Linearization,
)

from docplex.mp.model import Model


def electricSystemRegistration(
    model1: Model, num_hour0: int, intensityOfIllumination0: np.ndarray, day_node: int
):
    """ """

    # 柴油发电机
    dieselEngine = DieselEngine(
        num_hour0, model1, dieselEngine_device_max=320, device_price=750, run_price=2
    )
    dieselEngine.constraints_register(model1)

    # 光伏
    photoVoltaic = PhotoVoltaic(
        num_hour0,
        model1,
        photoVoltaic_device_max=5000,
        device_price=4500,
        intensityOfIllumination0=intensityOfIllumination0,
        efficiency=0.8,
        device_name="PhotoVoltaic",
    )
    photoVoltaic.constraints_register(model1)

    # 电池储能
    batteryEnergyStorageSystem = EnergyStorageSystem(
        num_hour0,
        model1,
        energyStorageSystem_device_max=20000,
        energyStorageSystem_price=1800,
        powerConversionSystem_price=250,
        conversion_rate_max=2,
        efficiency=0.9,
        energyStorageSystem_init=1,
        stateOfCharge_min=0,  # state of charge
        stateOfCharge_max=1,
    )
    # original: battery
    batteryEnergyStorageSystem.constraints_register(
        model1, register_period_constraints=1, day_node=day_node
    )
    return dieselEngine, photoVoltaic, batteryEnergyStorageSystem


def steamSourcesRegistration(
    model1: Model,
    num_hour0: int,
    intensityOfIllumination0: np.ndarray,
    # day_node: int,
    electricity_price0: np.ndarray,
    gas_price0: np.ndarray,
):
    """ """

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
    return (
        troughPhotoThermal,
        groundSourceSteamGenerator,
        combinedHeatAndPower,
        gasBoiler,
        municipalSteam,
    )


def hotWaterSourcesRegistration(
    model1: Model,
    num_hour0: int,
    intensityOfIllumination0: np.ndarray,
    day_node: int,
    electricity_price0: np.ndarray,
    municipalHotWater_price0: np.ndarray,
    gas_price0: np.ndarray,
):
    """"""

    # 平板光热
    platePhotothermal = PhotoVoltaic(
        num_hour0,
        model1,
        photoVoltaic_device_max=10000,
        device_price=500,
        intensityOfIllumination0=intensityOfIllumination0,
        efficiency=0.8,
        device_name="platePhotothermal",
    )  # platePhotothermal
    platePhotothermal.constraints_register(model1)

    # 相变蓄热
    phaseChangeHeatStorage = EnergyStorageSystem(
        num_hour0,
        model1,
        energyStorageSystem_device_max=10000,
        energyStorageSystem_price=350,
        powerConversionSystem_price=0,  # free conversion?
        conversion_rate_max=0.5,
        efficiency=0.9,
        energyStorageSystem_init=1,
        stateOfCharge_min=0,
        stateOfCharge_max=1,
    )
    phaseChangeHeatStorage.constraints_register(model1)

    # 市政热水
    municipalHotWater = CitySupply(
        num_hour0,
        model1,
        citySupplied_device_max=10000,
        device_price=3000,
        run_price=municipalHotWater_price0,
        efficiency=0.9,
    )
    municipalHotWater.constraints_register(model1)

    # 热水电锅炉
    hotWaterElectricBoiler = ElectricBoiler(
        num_hour0,
        model1,
        electricBoiler_device_max=10000,
        electricBoiler_price=200,
        electricity_price=electricity_price0,
        efficiency=0.9,
    )
    hotWaterElectricBoiler.constraints_register(model1)

    # 燃气热水器
    gasBoiler_hotWater = GasBoiler(
        num_hour0,
        model1,
        gasBoiler_device_max=20000,
        gasBoiler_price=200,
        gas_price=gas_price0,
        efficiency=0.9,
    )
    gasBoiler_hotWater.constraints_register(model1)

    # 水储能罐
    waterStorageTank = WaterEnergyStorage(
        num_hour0,
        model1,
        waterStorageTank_Volume_max=10000,
        volume_price=300,
        powerConversionSystem_price=1,
        conversion_rate_max=0.5,
        efficiency=0.9,
        energyStorageSystem_init=1,
        stateOfCharge_min=0,
        stateOfCharge_max=1,
        ratio_cool=10,
        ratio_heat=10,
        ratio_gheat=20,
    )
    waterStorageTank.constraints_register(
        model1, register_period_constraints=1, day_node=day_node
    )

    return (
        platePhotothermal,
        waterStorageTank,
        municipalHotWater,
        gasBoiler_hotWater,
        phaseChangeHeatStorage,
        hotWaterElectricBoiler,
    )


def cooletIceHeatDevicesRegistration(
    model1: Model,
    num_hour0: int,
    # intensityOfIllumination0: np.ndarray,
    # day_node: int,
    electricity_price0: np.ndarray,
    # municipalHotWater_price0: np.ndarray,
    # gas_price0: np.ndarray,
):
    """"""

    # 热泵
    heatPump = WaterHeatPump(
        num_hour0,
        model1,
        device_max=20000,
        device_price=1000,
        electricity_price=electricity_price0,
        case_ratio=np.array([1, 1, 1, 1]),  # total four cases?
    )
    heatPump.constraints_register(model1)

    # 水源热泵
    waterSourceHeatPumps = WaterHeatPump(
        num_hour0,
        model1,
        device_max=2000,
        device_price=3000,
        electricity_price=electricity_price0,
        case_ratio=np.ones(4),
    )
    waterSourceHeatPumps.constraints_register(model1)

    # 水冷螺旋机
    waterCoolingSpiralMachine = WaterCoolingSpiral(
        num_hour0,
        model1,
        device_max=2000,
        device_price=1000,
        electricity_price=electricity_price0,
        case_ratio=np.array([1, 0.8]),
    )
    waterCoolingSpiralMachine.constraints_register(model1)

    # 三工况机组
    tripleWorkingConditionUnit = TripleWorkingConditionUnit(
        num_hour0,
        model1,
        device_max=20000,
        device_price=1000,
        electricity_price=electricity_price0,
        case_ratio=[1, 0.8, 0.8],
    )
    tripleWorkingConditionUnit.constraints_register(model1)

    # 双工况机组
    doubleWorkingConditionUnit = DoubleWorkingConditionUnit(
        num_hour0,
        model1,
        device_max=20000,
        device_price=1000,
        electricity_price=electricity_price0,
        case_ratio=[1, 0.8],
    )
    doubleWorkingConditionUnit.constraints_register(model1)

    # 地源热泵
    groundSourceHeatPump = GeothermalHeatPump(
        num_hour0,
        model1,
        device_max=20000,
        device_price=40000,
        electricity_price=electricity_price0,
    )
    groundSourceHeatPump.constraints_register(model1)

    # 电池？保鲜？相变？冰蓄能？
    iceStorage = EnergyStorageSystem(  # what is this?
        num_hour0,
        model1,
        energyStorageSystem_device_max=20000,
        energyStorageSystem_price=300,
        powerConversionSystem_price=1,
        conversion_rate_max=0.5,
        efficiency=0.9,
        energyStorageSystem_init=1,
        stateOfCharge_min=0,
        stateOfCharge_max=1,
    )
    iceStorage.constraints_register(model1)

    # 相变蓄冷
    phaseChangeRefrigerantStorage = EnergyStorageSystem(
        num_hour0,
        model1,
        energyStorageSystem_device_max=20000,
        energyStorageSystem_price=500,
        powerConversionSystem_price=1,
        conversion_rate_max=0.5,
        efficiency=0.9,
        energyStorageSystem_init=1,
        stateOfCharge_min=0,
        stateOfCharge_max=1,
    )
    phaseChangeRefrigerantStorage.constraints_register(model1)

    # 相变蓄热
    lowphaseChangeHeatStorage = EnergyStorageSystem(
        num_hour0,
        model1,
        energyStorageSystem_device_max=20000,
        energyStorageSystem_price=300,
        powerConversionSystem_price=1,
        conversion_rate_max=0.5,
        efficiency=0.9,
        energyStorageSystem_init=1,
        stateOfCharge_min=0,
        stateOfCharge_max=1,
    )
    lowphaseChangeHeatStorage.constraints_register(model1)

    return (
        heatPump,
        waterSourceHeatPumps,
        waterCoolingSpiralMachine,
        tripleWorkingConditionUnit,
        doubleWorkingConditionUnit,
        groundSourceHeatPump,
        iceStorage,
        phaseChangeRefrigerantStorage,
        lowphaseChangeHeatStorage,
    )
