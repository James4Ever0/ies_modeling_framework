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


# =================================柴油信息=================================


@fixture
def 测试柴油信息信息():
    val = 柴油信息信息(
        设备名称="柴油",
        Price=None,
        热值=None,
        CO2=None,
    )
    return val


@fixture
def 测试柴油信息ID():
    val = 柴油ID(
        ID=0,
        燃料接口=1,
    )
    return val


@fixture
def 测试柴油信息模型(
    测试柴油信息信息: 柴油信息信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试柴油信息ID: 柴油信息ID
):
    val = 柴油信息模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=柴油信息ID, 设备信息=柴油信息信息)
    return val


# ================================电负荷信息=================================


@fixture
def 测试电负荷信息信息():
    val = 电负荷信息信息(
        设备名称="电负荷",
        EnergyConsumption=None,
        MaxEnergyConsumption=None,
        PriceModel=None,
    )
    return val


@fixture
def 测试电负荷信息ID():
    val = 电负荷信息ID(
        ID=2,
        电接口=3,
    )
    return val


@fixture
def 测试电负荷信息模型(
    测试电负荷信息信息: 电负荷信息信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试电负荷信息ID: 电负荷信息ID
):
    val = 电负荷信息模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=电负荷信息ID, 设备信息=电负荷信息信息)
    return val


# ================================光伏发电信息================================


@fixture
def 测试光伏发电信息信息():
    val = 光伏发电信息信息(
        设备名称="光伏发电",
        生产厂商="Any",
        设备型号="光伏发电1",
        Area=None,
        PowerConversionEfficiency=None,
        MaxPower=None,
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
def 测试光伏发电信息ID():
    val = 光伏发电信息ID(
        ID=4,
        电接口=5,
    )
    return val


@fixture
def 测试光伏发电信息模型(
    测试光伏发电信息信息: 光伏发电信息信息,
    model_wrapper: ModelWrapper,
    测试计算参数: 计算参数,
    测试光伏发电信息ID: 光伏发电信息ID,
):
    val = 光伏发电信息模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=光伏发电信息ID, 设备信息=光伏发电信息信息)
    return val


# ================================风力发电信息================================


@fixture
def 测试风力发电信息信息():
    val = 风力发电信息信息(
        设备名称="风力发电",
        生产厂商="Any",
        设备型号="风力发电1",
        RatedPower=None,
        RatedWindSpeed=None,
        MinWindSpeed=None,
        MaxWindSpeed=None,
        PowerDeltaLimit=None,
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
def 测试风力发电信息ID():
    val = 风力发电信息ID(
        ID=6,
        电接口=7,
    )
    return val


@fixture
def 测试风力发电信息模型(
    测试风力发电信息信息: 风力发电信息信息,
    model_wrapper: ModelWrapper,
    测试计算参数: 计算参数,
    测试风力发电信息ID: 风力发电信息ID,
):
    val = 风力发电信息模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=风力发电信息ID, 设备信息=风力发电信息信息)
    return val


# ================================柴油发电信息================================


@fixture
def 测试柴油发电信息信息():
    val = 柴油发电信息信息(
        设备名称="柴油发电",
        生产厂商="Any",
        设备型号="柴油发电1",
        RatedPower=None,
        PowerDeltaLimit=None,
        PowerStartupLimit=None,
        CostPerMachine=None,
        CostPerYearPerMachine=None,
        VariationalCostPerWork=None,
        Life=None,
        BuildCostPerMachine=None,
        BuildBaseCost=None,
        MaxDeviceCount=None,
        MinDeviceCount=None,
        DeviceCount=None,
        DieselToPower_Load=None,
    )
    return val


@fixture
def 测试柴油发电信息ID():
    val = 柴油发电信息ID(
        ID=8,
        燃料接口=9,
        电接口=10,
    )
    return val


@fixture
def 测试柴油发电信息模型(
    测试柴油发电信息信息: 柴油发电信息信息,
    model_wrapper: ModelWrapper,
    测试计算参数: 计算参数,
    测试柴油发电信息ID: 柴油发电信息ID,
):
    val = 柴油发电信息模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=柴油发电信息ID, 设备信息=柴油发电信息信息)
    return val


# ================================锂电池信息=================================


@fixture
def 测试锂电池信息信息():
    val = 锂电池信息信息(
        设备名称="锂电池",
        生产厂商="Any",
        设备型号="锂电池1",
        循环边界条件=None,
        RatedCapacity=None,
        BatteryDeltaLimit=None,
        ChargeEfficiency=None,
        DischargeEfficiency=None,
        MaxSOC=None,
        MinSOC=None,
        BatteryStorageDecay=None,
        TotalDischargeCapacity=None,
        BatteryLife=None,
        CostPerCapacity=None,
        CostPerYearPerCapacity=None,
        VariationalCostPerWork=None,
        Life=None,
        BuildCostPerCapacity=None,
        BuildBaseCost=None,
        InitSOC=None,
        MaxTotalCapacity=None,
        MinTotalCapacity=None,
        TotalCapacity=None,
    )
    return val


@fixture
def 测试锂电池信息ID():
    val = 锂电池信息ID(
        ID=11,
        电接口=12,
    )
    return val


@fixture
def 测试锂电池信息模型(
    测试锂电池信息信息: 锂电池信息信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试锂电池信息ID: 锂电池信息ID
):
    val = 锂电池信息模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=锂电池信息ID, 设备信息=锂电池信息信息)
    return val


# ================================变压器信息=================================


@fixture
def 测试变压器信息信息():
    val = 变压器信息信息(
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
def 测试变压器信息ID():
    val = 变压器信息ID(
        ID=13,
        电输入=14,
        电输出=15,
    )
    return val


@fixture
def 测试变压器信息模型(
    测试变压器信息信息: 变压器信息信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试变压器信息ID: 变压器信息ID
):
    val = 变压器信息模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=变压器信息ID, 设备信息=变压器信息信息)
    return val


# ================================变流器信息=================================


@fixture
def 测试变流器信息信息():
    val = 变流器信息信息(
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
def 测试变流器信息ID():
    val = 变流器信息ID(
        ID=16,
        电输入=17,
        电输出=18,
    )
    return val


@fixture
def 测试变流器信息模型(
    测试变流器信息信息: 变流器信息信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试变流器信息ID: 变流器信息ID
):
    val = 变流器信息模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=变流器信息ID, 设备信息=变流器信息信息)
    return val


# ===============================双向变流器信息================================


@fixture
def 测试双向变流器信息信息():
    val = 双向变流器信息信息(
        设备名称="双向变流器",
        生产厂商="Any",
        设备型号="双向变流器1",
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
def 测试双向变流器信息ID():
    val = 双向变流器信息ID(
        ID=19,
        储能端=20,
        线路端=21,
    )
    return val


@fixture
def 测试双向变流器信息模型(
    测试双向变流器信息信息: 双向变流器信息信息,
    model_wrapper: ModelWrapper,
    测试计算参数: 计算参数,
    测试双向变流器信息ID: 双向变流器信息ID,
):
    val = 双向变流器信息模型(
        PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=双向变流器信息ID, 设备信息=双向变流器信息信息
    )
    return val


# ================================传输线信息=================================


@fixture
def 测试传输线信息信息():
    val = 传输线信息信息(
        设备名称="传输线",
        生产厂商="Any",
        设备型号="传输线1",
        PowerTransferDecay=None,
        CostPerKilometer=None,
        CostPerYearPerKilometer=None,
        Life=None,
        BuildCostPerKilometer=None,
        BuildBaseCost=None,
        Length=None,
    )
    return val


@fixture
def 测试传输线信息ID():
    val = 传输线信息ID(
        ID=22,
        电输入=23,
        电输出=24,
    )
    return val


@fixture
def 测试传输线信息模型(
    测试传输线信息信息: 传输线信息信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试传输线信息ID: 传输线信息ID
):
    val = 传输线信息模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=传输线信息ID, 设备信息=传输线信息信息)
    return val


# =================================计算参数=================================
@fixture
def 测试设备模型(model_wrapper: ModelWrapper, 测试计算参数: 计算参数):
    val = 设备模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, ID=0)
    return val
