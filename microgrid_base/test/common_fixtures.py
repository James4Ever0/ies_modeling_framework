from pytest import fixture
import sys

sys.path.append("../")
from ies_optim import *


@fixture
def model_wrapper():
    mw = ModelWrapper()
    yield mw
    del mw


from typing import Protocol, Any


class Request(Protocol):
    param: Any
    cache: Any


@fixture(scope="session", params=["设计规划", "仿真模拟"], ids=["PLANNING", "SIMULATION"])
def 测试计算参数(request: Request):  # _pytest.fixtures.SubRequest
    import numpy as np

    arr = abs(np.random.random((24,))).tolist()
    return 计算参数(
        计算目标="经济",
        # 计算目标="经济_环保",
        # 计算目标="环保",
        计算步长="小时",
        典型日=True,
        典型日代表的日期=[1],
        计算类型=request.param,
        风速=arr,
        光照=arr,
        气温=arr,
        年利率=0.1,
    )


# ==================================柴油==================================


@fixture
def 测试柴油信息():
    val = 柴油信息(设备名称="柴油", Price=(2, "万元/L"), 热值=(2, "kWh/L"), CO2=(2, "kg/L"))
    return val


@fixture
def 测试柴油ID():
    val = 柴油ID(
        ID=0,
        燃料接口=1,
    )
    return val


@fixture
def 测试柴油模型(测试柴油信息: 柴油信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试柴油ID: 柴油ID):
    val = 柴油模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=测试柴油ID, 设备信息=测试柴油信息)
    return val


# =================================电负荷==================================


@fixture
def 测试电负荷信息():
    val = 电负荷信息(
        设备名称="电负荷",
        EnergyConsumption=None,
        MaxEnergyConsumption=None,
        PriceModel=None,
    )
    return val


@fixture
def 测试电负荷ID():
    val = 电负荷ID(
        ID=2,
        电接口=3,
    )
    return val


@fixture
def 测试电负荷模型(测试电负荷信息: 电负荷信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试电负荷ID: 电负荷ID):
    val = 电负荷模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=测试电负荷ID, 设备信息=测试电负荷信息)
    return val


# =================================光伏发电=================================


@fixture
def 测试光伏发电信息():
    val = 光伏发电信息(
        设备名称="光伏发电",
        生产厂商="Any",
        设备型号="光伏发电1",
        Area=10,
        PowerConversionEfficiency=98,
        MaxPower=100,
        PowerDeltaLimit=None,
        CostPerKilowatt=None,
        CostPerYearPerKilowatt=None,
        VariationalCostPerWork=None,
        Life=None,
        BuildCostPerKilowatt=None,
        BuildBaseCost=None,
        MaxInstallArea=None,
        MinInstallArea=None,
        DeviceCount=None,
    )
    return val


@fixture
def 测试光伏发电ID():
    val = 光伏发电ID(
        ID=4,
        电接口=5,
    )
    return val


@fixture
def 测试光伏发电模型(
    测试光伏发电信息: 光伏发电信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试光伏发电ID: 光伏发电ID
):
    val = 光伏发电模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=测试光伏发电ID, 设备信息=测试光伏发电信息)
    return val


# =================================风力发电=================================


@fixture
def 测试风力发电信息():
    val = 风力发电信息(
        设备名称="风力发电",
        生产厂商="Any",
        设备型号="风力发电1",
        RatedPower=100,
        RatedWindSpeed=100,
        MinWindSpeed=10,
        MaxWindSpeed=200,
        PowerDeltaLimit=2,
        CostPerKilowatt=20,
        CostPerYearPerKilowatt=20,
        VariationalCostPerWork=20,
        Life=20,
        BuildCostPerKilowatt=20,
        BuildBaseCost=20,
        MaxDeviceCount=(devCount:=3),
        MinDeviceCount=devCount-0.5,
        DeviceCount=devCount,
    )
    return val


@fixture
def 测试风力发电ID():
    val = 风力发电ID(
        ID=6,
        电接口=7,
    )
    return val


@fixture
def 测试风力发电模型(
    测试风力发电信息: 风力发电信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试风力发电ID: 风力发电ID
):
    val = 风力发电模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=测试风力发电ID, 设备信息=测试风力发电信息)
    return val


# =================================柴油发电=================================


@fixture
def 测试柴油发电信息():
    val = 柴油发电信息(
        生产厂商="柴油发电1",
        设备型号="柴油发电1",
        设备名称="柴油发电1",
        RatedPower=20,
        PowerDeltaLimit=1,
        PowerStartupLimit=1,
        CostPerMachine=100,
        CostPerYearPerMachine=100,
        VariationalCostPerWork=100,
        Life=20,
        BuildCostPerMachine=10,
        BuildBaseCost=10,
        DieselToPower_Load=[[2, 10], [3, 50], [1, 100]],
        DeviceCount=1,
        MaxDeviceCount=1,
        MinDeviceCount=1,
    )
    return val


@fixture
def 测试柴油发电ID():
    val = 柴油发电ID(
        ID=8,
        燃料接口=9,
        电接口=10,
    )
    return val


@fixture
def 测试柴油发电模型(
    测试柴油发电信息: 柴油发电信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试柴油发电ID: 柴油发电ID
):
    val = 柴油发电模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=测试柴油发电ID, 设备信息=测试柴油发电信息)
    return val


# =================================锂电池==================================


@fixture
def 测试锂电池信息():
    val = 锂电池信息(
        设备名称="锂电池",
        生产厂商="Any",
        设备型号="锂电池1",
        循环边界条件="日间独立",
        # 循环边界条件="日间连接",
        RatedCapacity=20,
        BatteryDeltaLimit=10,
        ChargeEfficiency=50,
        DischargeEfficiency=50,
        MaxSOC=90,
        MinSOC=10,
        BatteryStorageDecay=0,
        # BatteryStorageDecay=10,
        TotalDischargeCapacity=100000000,
        BatteryLife=20,
        CostPerCapacity=20,
        CostPerYearPerCapacity=20,
        VariationalCostPerWork=20,
        Life=20,
        BuildCostPerCapacity=20,
        BuildBaseCost=20,
        InitSOC=89,
        # InitSOC=30,
        MaxTotalCapacity=(mcap := 500),
        MinTotalCapacity=mcap,
        TotalCapacity=mcap,
    )
    return val


@fixture
def 测试锂电池ID():
    val = 锂电池ID(
        ID=11,
        电接口=12,
    )
    return val


@fixture
def 测试锂电池模型(测试锂电池信息: 锂电池信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试锂电池ID: 锂电池ID):
    val = 锂电池模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=测试锂电池ID, 设备信息=测试锂电池信息)
    return val


# =================================变压器==================================


@fixture
def 测试变压器信息():
    val = 变压器信息(
        设备名称="变压器",
        生产厂商="Any",
        设备型号="变压器1",
        Efficiency=None,
        RatedPower=None,
        CostPerKilowatt=None,
        CostPerYearPerKilowatt=None,
        VariationalCostPerWork=None,
        Life=None,
        BuildCostPerKilowatt=None,
        BuildBaseCost=None,
        PowerParameter=None,
        LoadRedundancyParameter=None,
        MaxDeviceCount=None,
        MinDeviceCount=None,
        DeviceCount=None,
    )
    return val


@fixture
def 测试变压器ID():
    val = 变压器ID(
        ID=13,
        电输入=14,
        电输出=15,
    )
    return val


@fixture
def 测试变压器模型(测试变压器信息: 变压器信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试变压器ID: 变压器ID):
    val = 变压器模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=测试变压器ID, 设备信息=测试变压器信息)
    return val


# =================================变流器==================================


@fixture
def 测试变流器信息():
    val = 变流器信息(
        设备名称="变流器",
        生产厂商="Any",
        设备型号="变流器1",
        RatedPower=None,
        Efficiency=None,
        CostPerKilowatt=None,
        CostPerYearPerKilowatt=None,
        VariationalCostPerWork=None,
        Life=None,
        BuildCostPerKilowatt=None,
        BuildBaseCost=None,
        MaxDeviceCount=None,
        MinDeviceCount=None,
        DeviceCount=None,
    )
    return val


@fixture
def 测试变流器ID():
    val = 变流器ID(
        ID=16,
        电输入=17,
        电输出=18,
    )
    return val


@fixture
def 测试变流器模型(测试变流器信息: 变流器信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试变流器ID: 变流器ID):
    val = 变流器模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=测试变流器ID, 设备信息=测试变流器信息)
    return val


# ================================双向变流器=================================


@fixture
def 测试双向变流器信息():
    val = 双向变流器信息(
        设备名称="双向变流器",
        生产厂商="Any",
        设备型号="双向变流器1",
        RatedPower=100,
        Efficiency=98,
        CostPerKilowatt=2,
        CostPerYearPerKilowatt=2,
        VariationalCostPerWork=2,
        Life=10,
        BuildCostPerKilowatt=2,
        BuildBaseCost=2,
        MaxDeviceCount=1,
        MinDeviceCount=1-0.5,
        DeviceCount=1,
    )
    return val


@fixture
def 测试双向变流器ID():
    val = 双向变流器ID(
        ID=19,
        储能端=20,
        线路端=21,
    )
    return val


@fixture
def 测试双向变流器模型(
    测试双向变流器信息: 双向变流器信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试双向变流器ID: 双向变流器ID
):
    val = 双向变流器模型(
        PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=测试双向变流器ID, 设备信息=测试双向变流器信息
    )
    return val


# =================================传输线==================================


@fixture
def 测试传输线信息():
    val = 传输线信息(
        设备名称="传输线",
        生产厂商="Any",
        设备型号="传输线1",
        PowerTransferDecay=1,
        CostPerKilometer=2,
        CostPerYearPerKilometer=2,
        Life=100,
        BuildCostPerKilometer=20,
        BuildBaseCost=20,
        Length=10,
    )
    return val


@fixture
def 测试传输线ID():
    val = 传输线ID(
        ID=22,
        电输入=23,
        电输出=24,
    )
    return val


@fixture
def 测试传输线模型(测试传输线信息: 传输线信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试传输线ID: 传输线ID):
    val = 传输线模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=测试传输线ID, 设备信息=测试传输线信息)
    return val


# =================================计算参数=================================
@fixture
def 测试设备模型(model_wrapper: ModelWrapper, 测试计算参数: 计算参数):
    val = 设备模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, ID=0)
    return val
