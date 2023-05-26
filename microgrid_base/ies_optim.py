# TODO: 典型日 最终输出结果需要展开为8760

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
    ID: int
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
    ID: int
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
    ID: int
    燃料接口: int
    """
    类型: 柴油输入
    """
    电接口: int
    """
    类型: 供电端输出
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
    ID: int
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
    ID: int
    电输入: int
    """
    类型: 电母线输入
    """
    电输出: int
    """
    类型: 变压器输出
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
    ID: int
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
    ID: int
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
    ID: int
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


####################
# model definition #
####################

from pyomo.environ import *

# first convert the unit.
# assign variables.

# shall you assign port with variables.

# 风、光资源
from typing import Union, Literal, List

# 需要单位明确
class 计算参数(BaseModel):
    典型日ID: Union[int, None] = None
    计算步长: Union[Literal["小时"], Literal["秒"]]
    计算模式: Union[Literal["典型日"], None]
    风资源: List[float]
    """
    单位: m/s
    """
    光资源: List[float]
    """
    单位: kW/m2
    """
    气温: List[float]
    """
    单位: 摄氏度
    """

    @property
    def 迭代步数(self):
        if self.计算步长 == "秒":
            steps = 7200
        elif self.计算步长 == "小时" and self.计算模式 is None:
            steps = 8760
        elif self.计算步长 == "小时" and self.计算模式 is "典型日":
            steps = 24
        else:
            raise Exception("未知计算参数:", self.计算步长, self.计算模式)
        assert len(self.风资源) == steps
        assert len(self.光资源) == steps
        assert len(self.气温) == steps
        return steps


class 设备模型:
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, ID):
        self.model = model
        self.计算参数 = 计算参数实例
        self.ID = ID

    def getVarName(self, varName: str):
        VN = f"DI_{self.ID}_VN_{varName}"  # use underscore.
        if self.计算参数.典型日ID:
            VN = f"TD_{self.计算参数.典型日ID}_" + VN
        return VN

    def 单变量(self, varName: str, **kwargs):
        var = self.model.__dict__[self.getVarName(varName)] = Var(**kwargs)
        return var

    def 变量列表(self, varName: str, **kwargs):
        var = self.model.__dict__[self.getVarName(varName)] = Var(
            range(self.计算参数.迭代步数), **kwargs
        )
        return var


# input: negative
# output: positive
# IO: Real


class 光伏发电模型(设备模型):
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 光伏发电ID, 设备信息: 光伏发电信息):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.Area: float = 设备信息.Area
        """
        名称: 光伏板面积
        单位: m2
        """

        self.PowerConversionEfficiency: float = 设备信息.PowerConversionEfficiency * 0.01
        """
        名称: 电电转换效率
        单位: one <- percent
        """

        self.MaxPower: float = 设备信息.MaxPower
        """
        名称: 最大发电功率
        单位: kilowatt
        """

        self.PowerDeltaLimit: float = 设备信息.PowerDeltaLimit * 315575.99999999994
        """
        名称: 发电爬坡率
        单位: one / 年 <- percent/s
        """

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / kilowatt
        """

        self.CostPerYear: float = 设备信息.CostPerYear
        """
        名称: 固定维护成本
        单位: 万元 / kilowatt / 年
        """

        self.VariationalCostPerPower: float = 设备信息.VariationalCostPerPower * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kilowatt_hour <- 元/kWh
        """

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / kilowatt
        """

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """

        self.MaxInstallArea: float = 设备信息.MaxInstallArea
        """
        名称: 最大安装面积
        单位: m2
        """

        self.MinInstallArea: float = 设备信息.MinInstallArea
        """
        名称: 最小安装面积
        单位: m2
        """

        ##### PORT VARIABLE DEFINITION ####

        self.电接口 = self.变量列表("电接口", within=NonNegativeReals)
        """
        类型: 供电端输出
        """

    def constraints_register(self):
        ...


class 风力发电模型(设备模型):
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 风力发电ID, 设备信息: 风力发电信息):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.RatedPower: float = 设备信息.RatedPower
        """
        名称: 额定功率
        单位: kilowatt
        """

        self.RatedWindSpeed: float = 设备信息.RatedWindSpeed * 31557.600000000002
        """
        名称: 额定风速
        单位: kilometer / 年 <- m/s
        """

        self.MinWindSpeed: float = 设备信息.MinWindSpeed * 31557.600000000002
        """
        名称: 切入风速
        单位: kilometer / 年 <- m/s
        """

        self.MaxWindSpeed: float = 设备信息.MaxWindSpeed * 31557.600000000002
        """
        名称: 切出风速
        单位: kilometer / 年 <- m/s
        """

        self.PowerDeltaLimit: float = 设备信息.PowerDeltaLimit * 315575.99999999994
        """
        名称: 发电爬坡率
        单位: one / 年 <- percent/s
        """

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / kilowatt
        """

        self.CostPerYear: float = 设备信息.CostPerYear
        """
        名称: 固定维护成本
        单位: 万元 / kilowatt / 年
        """

        self.VariationalCostPerPower: float = 设备信息.VariationalCostPerPower * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kilowatt_hour <- 元/kWh
        """

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / kilowatt
        """

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """

        self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
        """
        名称: 最大安装台数
        单位: 台
        """

        self.MinDeviceCount: float = 设备信息.MinDeviceCount
        """
        名称: 最小安装台数
        单位: 台
        """

        ##### PORT VARIABLE DEFINITION ####

        self.电接口 = self.变量列表("电接口", within=NonNegativeReals)
        """
        类型: 供电端输出
        """

    def constraints_register(self):
        ...


class 柴油发电模型(设备模型):
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 柴油发电ID, 设备信息: 柴油发电信息):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.RatedPower: float = 设备信息.RatedPower
        """
        名称: 额定功率
        单位: kilowatt
        """

        self.PowerDeltaLimit: float = 设备信息.PowerDeltaLimit * 315575.99999999994
        """
        名称: 发电爬坡率
        单位: one / 年 <- percent/s
        """

        self.PowerStartupLimit: float = 设备信息.PowerStartupLimit * 0.01
        """
        名称: 启动功率百分比
        单位: one <- percent
        """

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / 台
        """

        self.CostPerYear: float = 设备信息.CostPerYear
        """
        名称: 固定维护成本
        单位: 万元 / 台 / 年
        """

        self.VariationalCostPerPower: float = 设备信息.VariationalCostPerPower * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kilowatt_hour <- 元/kWh
        """

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / 台
        """

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """

        self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
        """
        名称: 最大安装台数
        单位: 台
        """

        self.MinDeviceCount: float = 设备信息.MinDeviceCount
        """
        名称: 最小安装台数
        单位: 台
        """

        self.DieselToPower_Load: List[List[float]] = [
            [v1 * 0.0010000000000000002, v2 * 0.01]
            for v1, v2 in 设备信息.DieselToPower_Load
        ]
        """
        DieselToPower: 燃油消耗率
        单位: L/kWh

        Load: 负载率
        单位: percent
        """

        ##### PORT VARIABLE DEFINITION ####

        self.燃料接口 = self.变量列表("燃料接口", within=NegativeReals)
        """
        类型: 柴油输入
        """

        self.电接口 = self.变量列表("电接口", within=NonNegativeReals)
        """
        类型: 供电端输出
        """

    def constraints_register(self):
        ...


class 锂电池模型(设备模型):
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 锂电池ID, 设备信息: 锂电池信息):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.RatedCapacity: float = 设备信息.RatedCapacity
        """
        名称: 额定容量
        单位: kilowatt_hour
        """

        self.BatteryDeltaLimit: float = 设备信息.BatteryDeltaLimit * 8766.0
        """
        名称: 电池充放电倍率
        单位: 1 / 年 <- 1/hour
        """

        self.ChargeEfficiency: float = 设备信息.ChargeEfficiency * 0.01
        """
        名称: 充能效率
        单位: one <- percent
        """

        self.DischargeEfficiency: float = 设备信息.DischargeEfficiency * 0.01
        """
        名称: 放能效率
        单位: one <- percent
        """

        self.BatteryStorageDecay: float = 设备信息.BatteryStorageDecay * 87.66
        """
        名称: 存储衰减
        单位: one / 年 <- percent/hour
        """

        self.TotalDischargeCapacity: float = 设备信息.TotalDischargeCapacity
        """
        名称: 生命周期总放电量
        单位: kilowatt_hour
        """

        self.BatteryLife: float = 设备信息.BatteryLife
        """
        名称: 电池换芯周期
        单位: 年
        """

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / kilowatt_hour
        """

        self.CostPerYear: float = 设备信息.CostPerYear
        """
        名称: 固定维护成本
        单位: 万元 / kilowatt_hour / 年
        """

        self.VariationalCostPerPower: float = 设备信息.VariationalCostPerPower * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kilowatt_hour <- 元/kWh
        """

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / kilowatt_hour
        """

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """

        self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
        """
        名称: 最大安装台数
        单位: 台
        """

        self.MinDeviceCount: float = 设备信息.MinDeviceCount
        """
        名称: 最小安装台数
        单位: 台
        """

        ##### PORT VARIABLE DEFINITION ####

        self.电接口 = self.变量列表("电接口", within=Reals)
        """
        类型: 电储能端输入输出
        """

    def constraints_register(self):
        ...


class 变压器模型(设备模型):
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 变压器ID, 设备信息: 变压器信息):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.Efficiency: float = 设备信息.Efficiency * 0.01
        """
        名称: 效率
        单位: one <- percent
        """

        self.RatedPower: float = 设备信息.RatedPower
        """
        名称: 变压器容量
        单位: kilowatt
        """

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / kilowatt
        """

        self.CostPerYear: float = 设备信息.CostPerYear
        """
        名称: 固定维护成本
        单位: 万元 / kilowatt / 年
        """

        self.VariationalCostPerPower: float = 设备信息.VariationalCostPerPower * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kilowatt_hour <- 元/kWh
        """

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / kilowatt
        """

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """

        self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
        """
        名称: 最大安装台数
        单位: 台
        """

        self.MinDeviceCount: float = 设备信息.MinDeviceCount
        """
        名称: 最小安装台数
        单位: 台
        """

        ##### PORT VARIABLE DEFINITION ####

        self.电输入 = self.变量列表("电输入", within=NegativeReals)
        """
        类型: 电母线输入
        """

        self.电输出 = self.变量列表("电输出", within=NonNegativeReals)
        """
        类型: 变压器输出
        """

    def constraints_register(self):
        ...


class 变流器模型(设备模型):
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 变流器ID, 设备信息: 变流器信息):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.RatedPower: float = 设备信息.RatedPower
        """
        名称: 额定功率
        单位: kilowatt
        """

        self.Efficiency: float = 设备信息.Efficiency * 0.01
        """
        名称: 效率
        单位: one <- percent
        """

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / kilowatt
        """

        self.CostPerYear: float = 设备信息.CostPerYear
        """
        名称: 固定维护成本
        单位: 万元 / kilowatt / 年
        """

        self.VariationalCostPerPower: float = 设备信息.VariationalCostPerPower * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kilowatt_hour <- 元/kWh
        """

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / kilowatt
        """

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """

        self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
        """
        名称: 最大安装台数
        单位: 台
        """

        self.MinDeviceCount: float = 设备信息.MinDeviceCount
        """
        名称: 最小安装台数
        单位: 台
        """

        ##### PORT VARIABLE DEFINITION ####

        self.电输出 = self.变量列表("电输出", within=NonNegativeReals)
        """
        类型: 电母线输出
        """

        self.电输入 = self.变量列表("电输入", within=NegativeReals)
        """
        类型: 变流器输入
        """

    def constraints_register(self):
        ...


class 双向变流器模型(设备模型):
    def __init__(
        self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 双向变流器ID, 设备信息: 双向变流器信息
    ):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.RatedPower: float = 设备信息.RatedPower
        """
        名称: 额定功率
        单位: kilowatt
        """

        self.Efficiency: float = 设备信息.Efficiency * 0.01
        """
        名称: 效率
        单位: one <- percent
        """

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / kilowatt
        """

        self.CostPerYear: float = 设备信息.CostPerYear
        """
        名称: 固定维护成本
        单位: 万元 / kilowatt / 年
        """

        self.VariationalCostPerPower: float = 设备信息.VariationalCostPerPower * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kilowatt_hour <- 元/kWh
        """

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / kilowatt
        """

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """

        self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
        """
        名称: 最大安装台数
        单位: 台
        """

        self.MinDeviceCount: float = 设备信息.MinDeviceCount
        """
        名称: 最小安装台数
        单位: 台
        """

        ##### PORT VARIABLE DEFINITION ####

        self.线路端 = self.变量列表("线路端", within=Reals)
        """
        类型: 双向变流器线路端输入输出
        """

        self.储能端 = self.变量列表("储能端", within=Reals)
        """
        类型: 双向变流器储能端输入输出
        """

    def constraints_register(self):
        ...


class 传输线模型(设备模型):
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 传输线ID, 设备信息: 传输线信息):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.PowerTransferDecay: float = 设备信息.PowerTransferDecay
        """
        名称: 能量衰减系数
        单位: kilowatt / kilometer
        """

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / kilometer
        """

        self.VariationCostPerMeter: float = 设备信息.VariationCostPerMeter
        """
        名称: 维护成本
        单位: 万元 / kilometer / 年
        """

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / kilometer
        """

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """

        self.Length: float = 设备信息.Length
        """
        名称: 长度
        单位: kilometer
        """

        ##### PORT VARIABLE DEFINITION ####

        self.电输入 = self.变量列表("电输入", within=NegativeReals)
        """
        类型: 电母线输入
        """

        self.电输出 = self.变量列表("电输出", within=NonNegativeReals)
        """
        类型: 电母线输出
        """

    def constraints_register(self):
        ...
