# the main code for computing.
# currently just compute microgrid
# three computation modes:

# 8760 hours of data
# several days of data to compute a year

# 7200 seconds. simulation

# device parameters would be the same.

# load and environment might change.

# so for every device the will change.

# iterate through all device-port pairs, then retrieve attributes from another dict.

from pydantic import BaseModel
from typing import List

# string, digits, tables.
# you can dump and load from json.


class 光伏发电ID(BaseModel):
    设备: int
    电接口: int
    """
    类型: 供电端输出
    """


class 光伏发电信息(BaseModel):  # 发电设备
    生产厂商: str

    设备型号: str

    Area: float
    """
    名称: 光伏板面积
    单位: m2
    """

    PowerConversionEfficiency: float
    """
    名称: 电电转换效率
    单位: percent
    """

    MaxPower: float
    """
    名称: 最大发电功率
    单位: kWp
    """

    PowerDeltaLimit: float
    """
    名称: 发电爬坡率
    单位: percent/s
    """

    CostPerWatt: float
    """
    名称: 采购成本
    单位: 万元/kWp
    """

    CostPerYear: float
    """
    名称: 固定维护成本
    单位: 万元/(kWp*年)
    """

    VariationalCostPerPower: float
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerWatt: float
    """
    名称: 建设费用系数
    单位: 万元/kWp
    """

    BuildBaseCost: float
    """
    名称: 建设费用基数
    单位: 万元
    """

    MaxInstallArea: float
    """
    名称: 最大安装面积
    单位: m2
    """

    MinInstallArea: float
    """
    名称: 最小安装面积
    单位: m2
    """


class 风力发电ID(BaseModel):
    设备: int
    电接口: int
    """
    类型: 供电端输出
    """


class 风力发电信息(BaseModel):  # 发电设备
    生产厂商: str

    设备型号: str

    RatedPower: float
    """
    名称: 额定功率
    单位: kWp
    """

    RatedWindSpeed: float
    """
    名称: 额定风速
    单位: m/s
    """

    MinWindSpeed: float
    """
    名称: 切入风速
    单位: m/s
    """

    MaxWindSpeed: float
    """
    名称: 切出风速
    单位: m/s
    """

    PowerDeltaLimit: float
    """
    名称: 发电爬坡率
    单位: percent/s
    """

    CostPerWatt: float
    """
    名称: 采购成本
    单位: 万元/kWp
    """

    CostPerYear: float
    """
    名称: 固定维护成本
    单位: 万元/(kWp*年)
    """

    VariationalCostPerPower: float
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerWatt: float
    """
    名称: 建设费用系数
    单位: 万元/kWp
    """

    BuildBaseCost: float
    """
    名称: 建设费用基数
    单位: 万元
    """

    MaxDeviceCount: float
    """
    名称: 最大安装台数
    单位: 台
    """

    MinDeviceCount: float
    """
    名称: 最小安装台数
    单位: 台
    """


class 柴油发电ID(BaseModel):
    设备: int
    电接口: int
    """
    类型: 供电端输出
    """
    燃料接口: int
    """
    类型: 柴油输入
    """


class 柴油发电信息(BaseModel):  # 发电设备
    生产厂商: str

    设备型号: str

    RatedPower: float
    """
    名称: 额定功率
    单位: kW
    """

    PowerDeltaLimit: float
    """
    名称: 发电爬坡率
    单位: percent/s
    """

    PowerStartupLimit: float
    """
    名称: 启动功率百分比
    单位: percent
    """

    CostPerWatt: float
    """
    名称: 采购成本
    单位: 万元/台
    """

    CostPerYear: float
    """
    名称: 固定维护成本
    单位: 万元/(台*年)
    """

    VariationalCostPerPower: float
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerWatt: float
    """
    名称: 建设费用系数
    单位: 万元/台
    """

    BuildBaseCost: float
    """
    名称: 建设费用基数
    单位: 万元
    """

    MaxDeviceCount: float
    """
    名称: 最大安装台数
    单位: 台
    """

    MinDeviceCount: float
    """
    名称: 最小安装台数
    单位: 台
    """

    DieselToPower_Load: List[List[float]]
    """
    DieselToPower: 燃油消耗率
    单位: L/kWh

    Load: 负载率
    单位: percent
    """


class 锂电池ID(BaseModel):
    设备: int
    电接口: int
    """
    类型: 电储能端输入输出
    """


class 锂电池信息(BaseModel):  # 储能设备
    生产厂商: str

    设备型号: str

    RatedCapacity: float
    """
    名称: 额定容量
    单位: kWh
    """

    BatteryDeltaLimit: float
    """
    名称: 电池充放电倍率
    单位: 1/hour
    """

    ChargeEfficiency: float
    """
    名称: 充能效率
    单位: percent
    """

    DischargeEfficiency: float
    """
    名称: 放能效率
    单位: percent
    """

    BatteryStorageDecay: float
    """
    名称: 存储衰减
    单位: percent/hour
    """

    TotalDischargeCapacity: float
    """
    名称: 生命周期总放电量
    单位: kWh
    """

    BatteryLife: float
    """
    名称: 电池换芯周期
    单位: 年
    """

    CostPerWatt: float
    """
    名称: 采购成本
    单位: 万元/kWh
    """

    CostPerYear: float
    """
    名称: 固定维护成本
    单位: 万元/(kWh*年)
    """

    VariationalCostPerPower: float
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerWatt: float
    """
    名称: 建设费用系数
    单位: 万元/kWh
    """

    BuildBaseCost: float
    """
    名称: 建设费用基数
    单位: 万元
    """

    MaxDeviceCount: float
    """
    名称: 最大安装台数
    单位: 台
    """

    MinDeviceCount: float
    """
    名称: 最小安装台数
    单位: 台
    """


class 变压器ID(BaseModel):
    设备: int
    电输出: int
    """
    类型: 变压器输出
    """
    电输入: int
    """
    类型: 电母线输入
    """


class 变压器信息(BaseModel):  # 配电传输
    生产厂商: str

    设备型号: str

    Efficiency: float
    """
    名称: 效率
    单位: percent
    """

    RatedPower: float
    """
    名称: 变压器容量
    单位: kW
    """

    CostPerWatt: float
    """
    名称: 采购成本
    单位: 万元/kW
    """

    CostPerYear: float
    """
    名称: 固定维护成本
    单位: 万元/(kW*年)
    """

    VariationalCostPerPower: float
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerWatt: float
    """
    名称: 建设费用系数
    单位: 万元/kW
    """

    BuildBaseCost: float
    """
    名称: 建设费用基数
    单位: 万元
    """

    MaxDeviceCount: float
    """
    名称: 最大安装台数
    单位: 台
    """

    MinDeviceCount: float
    """
    名称: 最小安装台数
    单位: 台
    """


class 变流器ID(BaseModel):
    设备: int
    电输出: int
    """
    类型: 电母线输出
    """
    电输入: int
    """
    类型: 变流器输入
    """


class 变流器信息(BaseModel):  # 配电传输
    生产厂商: str

    设备型号: str

    RatedPower: float
    """
    名称: 额定功率
    单位: kW
    """

    Efficiency: float
    """
    名称: 效率
    单位: percent
    """

    CostPerWatt: float
    """
    名称: 采购成本
    单位: 万元/kW
    """

    CostPerYear: float
    """
    名称: 固定维护成本
    单位: 万元/(kW*年)
    """

    VariationalCostPerPower: float
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerWatt: float
    """
    名称: 建设费用系数
    单位: 万元/kW
    """

    BuildBaseCost: float
    """
    名称: 建设费用基数
    单位: 万元
    """

    MaxDeviceCount: float
    """
    名称: 最大安装台数
    单位: 台
    """

    MinDeviceCount: float
    """
    名称: 最小安装台数
    单位: 台
    """


class 双向变流器ID(BaseModel):
    设备: int
    线路端: int
    """
    类型: 双向变流器线路端输入输出
    """
    储能端: int
    """
    类型: 双向变流器储能端输入输出
    """


class 双向变流器信息(BaseModel):  # 配电传输
    生产厂商: str

    设备型号: str

    RatedPower: float
    """
    名称: 额定功率
    单位: kW
    """

    Efficiency: float
    """
    名称: 效率
    单位: percent
    """

    CostPerWatt: float
    """
    名称: 采购成本
    单位: 万元/kW
    """

    CostPerYear: float
    """
    名称: 固定维护成本
    单位: 万元/(kW*年)
    """

    VariationalCostPerPower: float
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerWatt: float
    """
    名称: 建设费用系数
    单位: 万元/kW
    """

    BuildBaseCost: float
    """
    名称: 建设费用基数
    单位: 万元
    """

    MaxDeviceCount: float
    """
    名称: 最大安装台数
    单位: 台
    """

    MinDeviceCount: float
    """
    名称: 最小安装台数
    单位: 台
    """


class 传输线ID(BaseModel):
    设备: int
    电输入: int
    """
    类型: 电母线输入
    """
    电输出: int
    """
    类型: 电母线输出
    """


class 传输线信息(BaseModel):  # 配电传输
    生产厂商: str

    设备型号: str

    PowerTransferDecay: float
    """
    名称: 能量衰减系数
    单位: kW/km
    """

    CostPerWatt: float
    """
    名称: 采购成本
    单位: 万元/km
    """

    VariationCostPerMeter: float
    """
    名称: 维护成本
    单位: 万元/(km*年)
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerWatt: float
    """
    名称: 建设费用系数
    单位: 万元/km
    """

    BuildBaseCost: float
    """
    名称: 建设费用基数
    单位: 万元
    """

    Length: float
    """
    名称: 长度
    单位: km
    """


# model structure.

import pyomo

# first convert the unit.


class 光伏发电:
    def __init__(self, 设备ID: 光伏发电ID, 设备信息: 光伏发电信息):
        ...


class 风力发电:
    def __init__(self, 设备ID: 风力发电ID, 设备信息: 风力发电信息):
        ...


class 柴油发电:
    def __init__(self, 设备ID: 柴油发电ID, 设备信息: 柴油发电信息):
        ...


class 锂电池:
    def __init__(self, 设备ID: 锂电池ID, 设备信息: 锂电池信息):
        ...


class 变压器:
    def __init__(self, 设备ID: 变压器ID, 设备信息: 变压器信息):
        ...


class 变流器:
    def __init__(self, 设备ID: 变流器ID, 设备信息: 变流器信息):
        ...


class 双向变流器:
    def __init__(self, 设备ID: 双向变流器ID, 设备信息: 双向变流器信息):
        ...


class 传输线:
    def __init__(self, 设备ID: 传输线ID, 设备信息: 传输线信息):
        ...
