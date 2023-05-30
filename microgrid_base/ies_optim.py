# TODO: 典型日 最终输出结果需要展开为8760
import rich

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

    DeviceCount: float
    """
    名称: 安装台数
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

    DeviceCount: float
    """
    名称: 安装台数
    单位: 台
    """

    设_DieselToPower: List[List[float]]
    """
    设: 备
    单位: 参

    DieselToPower: 燃油消耗率
    单位: L/kWh
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

    MaxSOC: float
    """
    名称: 最大SOC
    单位: percent
    """

    MinSOC: float
    """
    名称: 最小SOC
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

    InitSOC: float
    """
    名称: 初始SOC
    单位: percent
    """


class 变压器ID(BaseModel):
    ID: int
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

    DeviceCount: float
    """
    名称: 安装台数
    单位: 台
    """


class 变流器ID(BaseModel):
    ID: int
    电输入: int
    """
    类型: 变流器输入
    """
    电输出: int
    """
    类型: 电母线输出
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

    DeviceCount: float
    """
    名称: 安装台数
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

    DeviceCount: float
    """
    名称: 安装台数
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

# 风、光照
from typing import Union, Literal, List

# 需要单位明确
class 计算参数(BaseModel):
    典型日ID: Union[int, None] = None
    计算步长: Union[Literal["小时"], Literal["秒"]]
    典型日: bool
    计算类型: Union[Literal["仿真模拟"], Literal["设计规划"]]
    风速: List[float]
    """
    单位: m/s
    """
    光照: List[float]
    """
    单位: kW/m2
    """
    气温: List[float]
    """
    单位: 摄氏度
    """
    年利率: Union[float, None]
    """
    单位: percent
    """

    @property
    def 迭代步数(self):
        if self.计算步长 == "秒":
            steps = 7200
        elif self.计算步长 == "小时" and self.典型日 is False:
            steps = 8760
        elif self.计算步长 == "小时" and self.典型日 is True:
            steps = 24
        else:
            rich.print(self)
            raise Exception("未知计算参数")
        assert len(self.风速) == steps
        assert len(self.光照) == steps
        assert len(self.气温) == steps
        return steps


class POSNEG:
    def __init__(self, x, x_pos, x_neg, b_pos, b_neg, x_abs):
        self.x = x
        self.x_pos = x_pos
        self.x_neg = x_neg
        self.b_pos = b_pos
        self.b_neg = b_neg
        self.x_abs = x_abs


from functools import reduce


class 设备模型:
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, ID):
        self.model = model
        self.计算参数 = 计算参数实例
        self.ID = ID
        self.SID = 0
        self.BigM = 1e10
        """
        一个极大数
        """
        self.EPS = 1e-4
        """
        一个极小数
        """

    def getVarName(self, varName: str):
        VN = f"DI_{self.ID}_VN_{varName}"  # use underscore.
        if self.计算参数.典型日ID:
            VN = f"TD_{self.计算参数.典型日ID}_" + VN
        return VN

    def getSpecialVarName(self, varName: str):
        specialVarName = f"SP_{self.SID}_{varName}"
        self.SID += 1
        return specialVarName

    def 单变量(self, varName: str, **kwargs):
        var = self.model.__dict__[self.getVarName(varName)] = Var(**kwargs)
        return var

    def 变量列表(self, varName: str, **kwargs):
        var = self.model.__dict__[self.getVarName(varName)] = Var(
            range(self.计算参数.迭代步数), **kwargs
        )
        return var

    def RangeConstraint(self, var_1, var_2, expression):
        for i in range(self.计算参数.迭代步数):
            Constraint(expression(var_1, var_2))

    def RangeConstraintMulti(self, *vars, expression=...):  # keyword argument now.
        assert expression is not ...
        for i in range(self.计算参数.迭代步数):
            Constraint(expression(*[var[i] for var in vars]))

    def CustomRangeConstraint(self, var_1, var_2, customRange: range, expression):
        for i in customRange:
            Constraint(expression(var_1, var_2, i))

    def CustomRangeConstraintMulti(
        self, *vars, customRange: range = ..., expression=...
    ):
        assert expression is not ...
        assert customRange is not ...
        for i in customRange:
            Constraint(expression(*vars, i))

    def SumRange(self, var_1):
        return reduce(
            sequence=[var_1[i] for i in range(self.计算参数.迭代步数)],
            function=lambda x, y: x + y,
        )

    def 变量列表_带指示变量(self, varName: str, within=Reals) -> POSNEG:
        x = self.变量列表(varName, within=within)

        b_pos = self.变量列表(self.getSpecialVarName(varName), within=Boolean)
        x_pos = self.变量列表(self.getSpecialVarName(varName), within=NonNegativeReals)

        self.RangeConstraint(b_pos, x_pos, lambda x, y: x * self.BigM >= x_pos)
        b_neg = self.变量列表(self.getSpecialVarName(varName), within=Boolean)
        x_neg = self.变量列表(self.getSpecialVarName(varName), within=NonNegativeReals)

        self.RangeConstraint(b_neg, x_neg, lambda x, y: x * self.BigM >= x_neg)

        self.RangeConstraint(b_pos, b_neg, lambda x, y: x + y == 1)

        self.RangeConstraintMulti(
            x, x_pos, x_neg, expression=lambda x, y, z: x == y - z
        )

        x_abs = self.变量列表(self.getSpecialVarName(varName), within=NonNegativeReals)

        self.RangeConstraintMulti(x_pos, x_neg, x_abs, lambda x, y, z: z == x + y)

        posneg = POSNEG(x, x_pos, x_neg, b_pos, b_neg, x_abs)

        return posneg

    def Piecewise(
        self,
        var_0,
        var_1,
        pw_pts: List[float],
        f_rule: List[float],
        range_list: Union[List[int], None] = None,
        pw_repn="SOS2",
        pw_constr_type="EQ",
        unbounded_domain_var=True,
    ):
        if range_list is None:
            range_list = list(range(self.计算参数.迭代步数))
        piecewise_name = self.getSpecialVarName("PW")
        self.model.__dict__[piecewise_name] = PW = Piecewise(
            range_list,
            var_0,
            var_1,
            pw_pts,
            f_rule,
            pw_repn=pw_repn,
            pw_constr_type=pw_constr_type,
            unbounded_domain_var=unbounded_domain_var,
        )
        return PW

    def Multiply(
        self, dict_mx: dict, dict_my: dict, varName: str, precision=10, within=Reals
    ):
        #  (x+y)^2 - (x-y)^2 = 4xy
        mx, max_mx, min_mx = dict_mx["var"], dict_mx["max"], dict_mx["min"]
        my, max_my, min_my = dict_my["var"], dict_my["max"], dict_my["min"]

        m1posneg = self.变量列表_带指示变量(self.getSpecialVarName(varName))
        self.RangeConstraintMulti(
            m1posneg.x, mx, my, expression=lambda x, y, z: x == y + z
        )
        mx_my_sum_var = m1posneg.x_abs
        mx_my_sum_pow2_var = self.变量列表(self.getSpecialVarName(varName))

        m2posneg = self.变量列表_带指示变量(self.getSpecialVarName(varName))
        self.RangeConstraintMulti(
            m2posneg.x, mx, my, expression=lambda x, y, z: x == y - z
        )
        mx_my_minus_var = m2posneg.x_abs
        mx_my_minus_pow2_var = self.变量列表(self.getSpecialVarName(varName))

        l0, r0 = min_mx + min_my, max_mx + max_my
        l1, r1 = min_mx - max_my, max_mx - min_my

        def getBound(l0, r0):
            if l0 * r0 >= 0:
                l0, r0 = abs(l0), abs(r0)
                l, r = min([l0, r0]), max([l0, r0])
            else:
                l0, r0 = abs(l0), abs(r0)
                l, r = 0, max([l0, r0])
            return l, r

        mx_my_sum = np.linspace(*getBound(l0, r0), precision).tolist()

        mx_my_sum_pow2 = [x**2 for x in mx_my_sum]

        mx_my_minus = np.linspace(*getBound(l1, r1), precision).tolist()

        mx_my_minus_pow2 = [x**2 for x in mx_my_minus]

        self.Piecewise(
            mx_my_sum_var, mx_my_sum_pow2_var, pw_pts=mx_my_sum, f_rule=mx_my_sum_pow2
        )  # assume it is absolute.

        self.Piecewise(
            mx_my_minus_var,
            mx_my_minus_pow2_var,
            pw_pts=mx_my_minus,
            f_rule=mx_my_minus_pow2,
        )

        mx_my_multiply = self.变量列表(varName, within=within)

        mx_my_multiply = self.RangeConstraint(
            mx_my_sum_pow2_var, mx_my_minus_pow2_var, lambda x, y: (x - y) / 4
        )

        return mx_my_multiply


# input: negative
# output: positive
# IO: Real
import numpy as np
import math


class 光伏发电模型(设备模型):
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 光伏发电ID, 设备信息: 光伏发电信息):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)
        self.Area: float = 设备信息.Area
        """
        名称: 光伏板面积
        单位: m2
        """
        assert self.Area >= 0

        self.PowerConversionEfficiency: float = 设备信息.PowerConversionEfficiency * 0.01
        """
        名称: 电电转换效率
        单位: one <- percent
        """
        assert self.PowerConversionEfficiency >= 0

        self.MaxPower: float = 设备信息.MaxPower
        """
        名称: 最大发电功率
        单位: kilowatt
        """
        assert self.MaxPower >= 0

        self.PowerDeltaLimit: float = 设备信息.PowerDeltaLimit
        """
        名称: 发电爬坡率
        单位: one / 年
        """
        assert self.PowerDeltaLimit >= 0

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / kilowatt
        """
        assert self.CostPerWatt >= 0

        self.CostPerYear: float = 设备信息.CostPerYear
        """
        名称: 固定维护成本
        单位: 万元 / kilowatt / 年
        """
        assert self.CostPerYear >= 0

        self.VariationalCostPerPower: float = 设备信息.VariationalCostPerPower * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kilowatt_hour <- 元/kWh
        """
        assert self.VariationalCostPerPower >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / kilowatt
        """
        assert self.BuildCostPerWatt >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.MaxInstallArea: float = 设备信息.MaxInstallArea
            """
            名称: 最大安装面积
            单位: m2
            """
            assert self.MaxInstallArea >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.MinInstallArea: float = 设备信息.MinInstallArea
            """
            名称: 最小安装面积
            单位: m2
            """
            assert self.MinInstallArea >= 0

        ##### PORT VARIABLE DEFINITION ####

        self.电接口 = self.变量列表("电接口", within=NonNegativeReals)
        """
        类型: 供电端输出
        """

        # 设备特有约束（变量）
        self.电输出 = self.电接口
        if self.计算参数.计算类型 == "设计规划":
            self.MaxDeviceCount = math.floor(self.MaxInstallArea / self.Area)
            self.MinDeviceCount = math.ceil(self.MinInstallArea / self.Area)
            assert self.MinDeviceCount >= 0
            assert self.MaxDeviceCount >= self.MinDeviceCount

    def constraints_register(self):
        # 设备特有约束（非变量）

        # 设备台数约束
        if self.计算参数.计算类型 == "规划设计":
            Constraint(self.DeviceCount <= self.MaxDeviceCount)
            Constraint(self.DeviceCount >= self.MinDeviceCount)

        # 输出输入功率约束
        光电转换效率 = self.MaxPower / self.Area  # 1kW/m2光照下能产生的能量 省略除以1 单位: one
        总最大功率 = self.MaxPower * self.DeviceCount
        总面积 = self.Area * self.DeviceCount

        # 光照强度 * 总面积 * 光电转换效率 * 电电转换效率
        # (kW/m2) * m2 * one * one -> kW
        self.RangeConstraint(
            self.计算参数.光照,
            self.电输出,
            lambda x, y: x * 总面积 * 光电转换效率 * self.PowerConversionEfficiency >= y,
        )

        if self.计算参数.计算步长 == "秒":
            总最大功率 = self.MaxPower * self.DeviceCount
            最大功率变化 = 总最大功率 * self.PowerDeltaLimit / 100
            self.CustomRangeConstraintMulti(
                self.电输出,
                customRange=range(self.计算参数.迭代步数 - 1),
                expression=lambda x, i: x[i + 1] - x[i] <= 最大功率变化,
            )
            self.CustomRangeConstraintMulti(
                self.电输出,
                customRange=range(self.计算参数.迭代步数 - 1),
                expression=lambda x, i: x[i + 1] - x[i] >= -最大功率变化,
            )

        # 计算年化
        # unit: one
        Life = self.Life

        年化率 = ((1 + (self.计算参数.年利率 / 100)) ** Life) / Life

        总采购成本 = self.CostPerWatt * (总最大功率)
        总固定维护成本 = self.CostPerYear * (总最大功率)
        总建设费用 = self.BuildCostPerWatt * (总最大功率) + self.BuildBaseCost

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总可变维护成本年化 = (
            (self.SumRange(self.电输出))
            * (8760 / self.计算参数.迭代步数)
            * ((1 if self.计算参数.计算步长 == "小时" else 3600))
            * self.VariationalCostPerPower
        )

        总成本年化 = 总固定成本年化 + 总可变维护成本年化


class 风力发电模型(设备模型):
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 风力发电ID, 设备信息: 风力发电信息):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)
        self.RatedPower: float = 设备信息.RatedPower
        """
        名称: 额定功率
        单位: kilowatt
        """
        assert self.RatedPower >= 0

        self.RatedWindSpeed: float = 设备信息.RatedWindSpeed
        """
        名称: 额定风速
        单位: kilometer / 年
        """
        assert self.RatedWindSpeed >= 0

        self.MinWindSpeed: float = 设备信息.MinWindSpeed
        """
        名称: 切入风速
        单位: kilometer / 年
        """
        assert self.MinWindSpeed >= 0

        self.MaxWindSpeed: float = 设备信息.MaxWindSpeed
        """
        名称: 切出风速
        单位: kilometer / 年
        """
        assert self.MaxWindSpeed >= 0

        self.PowerDeltaLimit: float = 设备信息.PowerDeltaLimit
        """
        名称: 发电爬坡率
        单位: one / 年
        """
        assert self.PowerDeltaLimit >= 0

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / kilowatt
        """
        assert self.CostPerWatt >= 0

        self.CostPerYear: float = 设备信息.CostPerYear
        """
        名称: 固定维护成本
        单位: 万元 / kilowatt / 年
        """
        assert self.CostPerYear >= 0

        self.VariationalCostPerPower: float = 设备信息.VariationalCostPerPower * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kilowatt_hour <- 元/kWh
        """
        assert self.VariationalCostPerPower >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / kilowatt
        """
        assert self.BuildCostPerWatt >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
            """
            名称: 最大安装台数
            单位: 台
            """
            assert self.MaxDeviceCount >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.MinDeviceCount: float = 设备信息.MinDeviceCount
            """
            名称: 最小安装台数
            单位: 台
            """
            assert self.MinDeviceCount >= 0

        if self.计算参数.计算类型 == "仿真模拟":
            self.DeviceCount: float = 设备信息.DeviceCount
            """
            名称: 安装台数
            单位: 台
            """
            assert self.DeviceCount >= 0

        ##### PORT VARIABLE DEFINITION ####

        self.电接口 = self.变量列表("电接口", within=NonNegativeReals)
        """
        类型: 供电端输出
        """

        # 设备特有约束（变量）
        self.电输出 = self.电接口

    def constraints_register(self):
        # 设备特有约束（非变量）
        # define a single-variate piecewise function
        #
        #         ____
        #        /    |
        #       /     | ax^3
        #  ----/      |______
        #
        assert self.RatedWindSpeed > self.MinWindSpeed
        assert self.MaxWindSpeed > self.RatedWindSpeed

        发电曲线参数 = self.RatedPower / ((self.RatedWindSpeed - self.MinWindSpeed) ** 3)

        # windspeed (m/s) -> current power per device (kW)
        WS = np.array(self.计算参数.风速)
        单台发电功率 = np.piecewise(
            WS,
            [
                WS <= self.MinWindSpeed,
                WS > self.MinWindSpeed and WS <= self.RatedWindSpeed,
                WS > self.RatedWindSpeed and WS < self.MaxWindSpeed,
                WS >= self.MaxWindSpeed,
            ],
            [0, lambda x: 发电曲线参数 * ((x - self.MinWindSpeed) ** 3), self.RatedPower, 0],
        )
        单台发电功率 = 单台发电功率.tolist()

        # 设备台数约束
        if self.计算参数.计算类型 == "规划设计":
            Constraint(self.DeviceCount <= self.MaxDeviceCount)
            Constraint(self.DeviceCount >= self.MinDeviceCount)

        # 输出输入功率约束
        self.RangeConstraint(单台发电功率, self.电输出, lambda x, y: x * self.DeviceCount >= y)

        if self.计算参数.计算步长 == "秒":
            总最大功率 = self.MaxPower * self.DeviceCount
            最大功率变化 = 总最大功率 * self.PowerDeltaLimit / 100
            self.CustomRangeConstraintMulti(
                self.电输出,
                customRange=range(self.计算参数.迭代步数 - 1),
                expression=lambda x, i: x[i + 1] - x[i] <= 最大功率变化,
            )
            self.CustomRangeConstraintMulti(
                self.电输出,
                customRange=range(self.计算参数.迭代步数 - 1),
                expression=lambda x, i: x[i + 1] - x[i] >= -最大功率变化,
            )

        # 计算年化
        # unit: one
        Life = self.Life

        年化率 = ((1 + (self.计算参数.年利率 / 100)) ** Life) / Life

        总采购成本 = self.CostPerWatt * (self.DeviceCount * self.RatedPower)
        总固定维护成本 = self.CostPerYear * (self.DeviceCount * self.RatedPower)
        总建设费用 = (
            self.BuildCostPerWatt * (self.DeviceCount * self.RatedPower)
            + self.BuildBaseCost
        )

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总可变维护成本年化 = (
            (self.SumRange(self.电输出))
            * (8760 / self.计算参数.迭代步数)
            * ((1 if self.计算参数.计算步长 == "小时" else 3600))
            * self.VariationalCostPerPower
        )

        总成本年化 = 总固定成本年化 + 总可变维护成本年化


class 柴油发电模型(设备模型):
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 柴油发电ID, 设备信息: 柴油发电信息):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)
        self.RatedPower: float = 设备信息.RatedPower
        """
        名称: 额定功率
        单位: kilowatt
        """
        assert self.RatedPower >= 0

        self.PowerDeltaLimit: float = 设备信息.PowerDeltaLimit
        """
        名称: 发电爬坡率
        单位: one / 年
        """
        assert self.PowerDeltaLimit >= 0

        self.PowerStartupLimit: float = 设备信息.PowerStartupLimit * 0.01
        """
        名称: 启动功率百分比
        单位: one <- percent
        """
        assert self.PowerStartupLimit >= 0

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / 台
        """
        assert self.CostPerWatt >= 0

        self.CostPerYear: float = 设备信息.CostPerYear
        """
        名称: 固定维护成本
        单位: 万元 / 台 / 年
        """
        assert self.CostPerYear >= 0

        self.VariationalCostPerPower: float = 设备信息.VariationalCostPerPower * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kilowatt_hour <- 元/kWh
        """
        assert self.VariationalCostPerPower >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / 台
        """
        assert self.BuildCostPerWatt >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
            """
            名称: 最大安装台数
            单位: 台
            """
            assert self.MaxDeviceCount >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.MinDeviceCount: float = 设备信息.MinDeviceCount
            """
            名称: 最小安装台数
            单位: 台
            """
            assert self.MinDeviceCount >= 0

        if self.计算参数.计算类型 == "仿真模拟":
            self.DeviceCount: float = 设备信息.DeviceCount
            """
            名称: 安装台数
            单位: 台
            """
            assert self.DeviceCount >= 0

        self.DieselToPower_Load: List[List[float]] = [
            [v1 * 0.0010000000000000002, v2 * 0.01]
            for v1, v2 in 设备信息.DieselToPower_Load
        ]
        self.DieselToPower_Load.sort(key=lambda x: x[1])
        """
        DieselToPower: 燃油消耗率
        单位: m3 / kilowatt_hour <- L/kWh

        Load: 负载率
        单位: one <- percent
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

        # 设备特有约束（变量）
        self.电输出 = self.电接口
        self.电功率中转 = self.变量列表_带指示变量("电功率中转")

        self.单台发电功率 = self.变量列表("单台发电功率", within=NonNegativeReals)
        self.单台柴油输入 = self.变量列表("单台柴油输入", within=NonPositiveReals)

        if self.计算参数.计算类型 == "设计规划":
            self.最大油耗率 = max([x[0] for x in self.DieselToPower_Load])

            self.原电输出 = self.Multiply(
                dict(var=self.单台发电功率, max=self.RatedPower, min=0),
                dict(
                    var=self.DeviceCount,
                    max=self.MaxDeviceCount,
                    min=self.MinDeviceCount,
                ),
                "原电输出",
                within=NonNegativeReals,
            )

            self.柴油输入_ = self.Multiply(
                dict(var=self.单台柴油输入, max=0, min=-self.RatedPower * self.最大油耗率),
                dict(
                    var=self.DeviceCount,
                    max=self.MaxDeviceCount,
                    min=self.MinDeviceCount,
                ),
                "柴油输入_",
                within=NonPositiveReals,
            )
            self.RangeConstraint(self.柴油输入_, self.柴油输入, lambda x, y: x == y)
        else:
            self.原电输出 = self.变量列表("原电输出", within=NonNegativeReals)
            self.RangeConstraint(
                self.原电输出, self.单台发电功率, lambda x, y: x == y * self.DeviceCount
            )

    def constraints_register(self):
        # 设备特有约束（非变量）

        # 设备台数约束
        if self.计算参数.计算类型 == "规划设计":
            Constraint(self.DeviceCount <= self.MaxDeviceCount)
            Constraint(self.DeviceCount >= self.MinDeviceCount)

        # 输出输入功率约束
        总最小启动功率 = self.RatedPower * self.PowerStartupLimit * self.DeviceCount
        总最大输出功率 = self.RatedPower * self.DeviceCount

        self.RangeConstraintMulti(
            self.单台发电功率, expression=lambda x: x <= self.RatedPower
        )
        self.RangeConstraint(self.原电输出, self.电功率中转.x, lambda x, y: x == y + 总最小启动功率)
        self.Piecewise(
            self.单台柴油输入,
            self.单台发电功率,
            [-x[0] * self.RatedPower * x[1] for x in self.DieselToPower_Load],
            [self.RatedPower * x[1] for x in self.DieselToPower_Load],
        )
        self.RangeConstraint(
            self.电功率中转.x_pos,
            self.电输出,
            self.电功率中转.b_pos,
            lambda x, y, z: x + 总最小启动功率 * z == y,
        )

        if self.计算参数.计算步长 == "秒":
            总最大功率 = self.MaxPower * self.DeviceCount
            最大功率变化 = 总最大功率 * self.PowerDeltaLimit / 100
            self.CustomRangeConstraintMulti(
                self.原电输出,
                customRange=range(self.计算参数.迭代步数 - 1),
                expression=lambda x, i: x[i + 1] - x[i] <= 最大功率变化,
            )
            self.CustomRangeConstraintMulti(
                self.原电输出,
                customRange=range(self.计算参数.迭代步数 - 1),
                expression=lambda x, i: x[i + 1] - x[i] >= -最大功率变化,
            )

        # 计算年化
        # unit: one
        Life = self.Life

        年化率 = ((1 + (self.计算参数.年利率 / 100)) ** Life) / Life

        总采购成本 = self.CostPerWatt * (self.DeviceCount * self.RatedPower)
        总固定维护成本 = self.CostPerYear * (self.DeviceCount * self.RatedPower)
        总建设费用 = (
            self.BuildCostPerWatt * (self.DeviceCount * self.RatedPower)
            + self.BuildBaseCost
        )

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总可变维护成本年化 = (
            (self.SumRange(self.电输出))
            * (8760 / self.计算参数.迭代步数)
            * ((1 if self.计算参数.计算步长 == "小时" else 3600))
            * self.VariationalCostPerPower
        )

        总成本年化 = 总固定成本年化 + 总可变维护成本年化


class 锂电池模型(设备模型):
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 锂电池ID, 设备信息: 锂电池信息):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)
        self.RatedCapacity: float = 设备信息.RatedCapacity
        """
        名称: 额定容量
        单位: kilowatt_hour
        """
        assert self.RatedCapacity >= 0

        self.BatteryDeltaLimit: float = 设备信息.BatteryDeltaLimit
        """
        名称: 电池充放电倍率
        单位: 1 / 年
        """
        assert self.BatteryDeltaLimit >= 0

        self.ChargeEfficiency: float = 设备信息.ChargeEfficiency * 0.01
        """
        名称: 充能效率
        单位: one <- percent
        """
        assert self.ChargeEfficiency >= 0

        self.DischargeEfficiency: float = 设备信息.DischargeEfficiency * 0.01
        """
        名称: 放能效率
        单位: one <- percent
        """
        assert self.DischargeEfficiency >= 0

        self.MaxSOC: float = 设备信息.MaxSOC * 0.01
        """
        名称: 最大SOC
        单位: one <- percent
        """
        assert self.MaxSOC >= 0

        self.MinSOC: float = 设备信息.MinSOC * 0.01
        """
        名称: 最小SOC
        单位: one <- percent
        """
        assert self.MinSOC >= 0

        self.BatteryStorageDecay: float = 设备信息.BatteryStorageDecay
        """
        名称: 存储衰减
        单位: one / 年
        """
        assert self.BatteryStorageDecay >= 0

        self.TotalDischargeCapacity: float = 设备信息.TotalDischargeCapacity
        """
        名称: 生命周期总放电量
        单位: kilowatt_hour
        """
        assert self.TotalDischargeCapacity >= 0

        self.BatteryLife: float = 设备信息.BatteryLife
        """
        名称: 电池换芯周期
        单位: 年
        """
        assert self.BatteryLife >= 0

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / kilowatt_hour
        """
        assert self.CostPerWatt >= 0

        self.CostPerYear: float = 设备信息.CostPerYear
        """
        名称: 固定维护成本
        单位: 万元 / kilowatt_hour / 年
        """
        assert self.CostPerYear >= 0

        self.VariationalCostPerPower: float = 设备信息.VariationalCostPerPower * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kilowatt_hour <- 元/kWh
        """
        assert self.VariationalCostPerPower >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / kilowatt_hour
        """
        assert self.BuildCostPerWatt >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.InitSOC: float = 设备信息.InitSOC * 0.01
            """
            名称: 初始SOC
            单位: one <- percent
            """
            assert self.InitSOC >= 0

        ##### PORT VARIABLE DEFINITION ####

        self.电接口 = self.变量列表("电接口", within=Reals)
        """
        类型: 电储能端输入输出
        """

        # 设备特有约束（变量）
        if self.计算参数.计算类型 == "设计规划":
            #  初始SOC
            assert self.InitSOC >= self.MinSOC
            assert self.InitSOC <= self.MaxSOC
            self.InitActualCapacityPerUnit = (
                self.InitSOC - self.MinSOC
            ) * self.RatedCapacity

            self.MaxDeviceCount = math.floor(self.MaxTotalCapacity / self.RatedCapacity)
            self.MinDeviceCount = math.ceil(self.MinTotalCapacity / self.RatedCapacity)

        assert self.MaxSOC > self.MinSOC
        assert self.MaxSOC <= 1
        assert self.MinSOC >= 0

        self.原电接口 = self.变量列表_带指示变量("原电接口")  # 正 放电 负 充电

        self.ActualCapacityPerUnit = self.RatedCapacity * (self.MaxSOC - self.MinSOC)

        self.CurrentTotalActualCapacity = self.变量列表(
            "CurrentTotalActualCapacity", within=NonNegativeReals
        )

        self.TotalCapacity = self.DeviceCount * self.RatedCapacity

        self.TotalActualCapacity = self.DeviceCount * self.ActualCapacityPerUnit

        self.MaxTotalCapacityDelta = (
            self.BatteryDeltaLimit
            / ((1 if self.计算参数.计算步长 == "小时" else 3600))
            * self.TotalCapacity
        )

        self.TotalStorageDecay = (
            self.BatteryStorageDecay
            / 100
            / ((1 if self.计算参数.计算步长 == "小时" else 3600))
            * self.TotalCapacity
        )

    def constraints_register(self):
        # 设备特有约束（非变量）

        # 设备台数约束
        if self.计算参数.计算类型 == "规划设计":
            Constraint(self.DeviceCount <= self.MaxDeviceCount)
            Constraint(self.DeviceCount >= self.MinDeviceCount)

        # 输出输入功率约束
        self.RangeConstraintMulti(
            self.CurrentTotalActualCapacity,
            expression=lambda x: x <= self.TotalActualCapacity,
        )

        Constraint(
            self.CurrentTotalActualCapacity[0]
            == self.InitActualCapacityPerUnit * self.DeviceCount
        )

        self.CustomRangeConstraint(
            self.原电接口.x,
            self.CurrentTotalActualCapacity,
            range(self.计算参数.迭代步数 - 1),
            lambda x, y, i: x == y[i] - y[i + 1],
        )

        self.RangeConstraintMulti(
            self.原电接口.x_pos,
            self.原电接口.x_neg,
            self.电接口,
            expression=lambda x_pos, x_neg, y: x_pos * self.DischargeEfficiency
            - (x_neg + self.TotalStorageDecay) * self.ChargeEfficiency
            == y,
        )

        for i in range(self.计算参数.迭代步数 - 1):
            Constraint(
                self.CurrentTotalActualCapacity[i + 1]
                - self.CurrentTotalActualCapacity[i]
                < self.MaxTotalCapacityDelta
            )
            Constraint(
                self.CurrentTotalActualCapacity[i + 1]
                - self.CurrentTotalActualCapacity[i]
                > -self.MaxTotalCapacityDelta
            )

        if self.计算参数.计算类型 == "设计规划":
            if self.设备信息.循环边界条件 == "日间独立":
                Constraint(self.原电接口.x[0] == self.EPS)
            elif self.设备信息.循环边界条件 == "日间连接":
                Constraint(
                    self.CurrentTotalActualCapacity[0]
                    - self.CurrentTotalActualCapacity[self.计算参数.迭代步数 - 1]
                    < self.MaxTotalCapacityDelta
                )

                Constraint(
                    self.CurrentTotalActualCapacity[0]
                    - self.CurrentTotalActualCapacity[self.计算参数.迭代步数 - 1]
                    > -self.MaxTotalCapacityDelta
                )

                Constraint(
                    self.原电接口.x[0]
                    == self.CurrentTotalActualCapacity[self.计算参数.迭代步数 - 1]
                    - self.CurrentTotalActualCapacity[0]
                )
            else:
                raise Exception("未知循环边界条件:", self.设备信息.循环边界条件)
        elif self.计算参数.计算类型 == "仿真模拟":
            Constraint(self.原电接口.x[0] == self.EPS)

        # 计算年化
        # unit: one

        计算范围内总电变化量 = self.SumRange(self.原电接口.x_pos) + self.SumRange(self.原电接口.x_neg)
        +self.TotalStorageDecay * self.计算参数.迭代步数
        一小时总电变化量 = 计算范围内总电变化量 * (1 if self.计算参数.计算步长 == "小时" else 3600)
        一年总电变化量 = 一小时总电变化量 * 8760

        Constraint(
            一年总电变化量 * self.BatteryLife
            <= self.DeviceCount * self.TotalDischargeCapacity * 0.85
        )
        assert self.BatteryLife >= 1
        assert self.Life >= self.BatteryLife
        Life = self.BatteryLife

        年化率 = ((1 + (self.计算参数.年利率 / 100)) ** Life) / Life

        总采购成本 = self.CostPerWatt * (self.DeviceCount * self.RatedCapacity)
        总固定维护成本 = self.CostPerYear * (self.DeviceCount * self.RatedCapacity)
        总建设费用 = (
            self.BuildCostPerWatt * (self.DeviceCount * self.RatedCapacity)
            + self.BuildBaseCost
        )

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总可变维护成本年化 = (
            (计算范围总电变化量)
            * (8760 / self.计算参数.迭代步数)
            * ((1 if self.计算参数.计算步长 == "小时" else 3600))
            * self.VariationalCostPerPower
        )

        总成本年化 = 总固定成本年化 + 总可变维护成本年化


class 变压器模型(设备模型):
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 变压器ID, 设备信息: 变压器信息):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)
        self.Efficiency: float = 设备信息.Efficiency * 0.01
        """
        名称: 效率
        单位: one <- percent
        """
        assert self.Efficiency >= 0

        self.RatedPower: float = 设备信息.RatedPower
        """
        名称: 变压器容量
        单位: kilowatt
        """
        assert self.RatedPower >= 0

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / kilowatt
        """
        assert self.CostPerWatt >= 0

        self.CostPerYear: float = 设备信息.CostPerYear
        """
        名称: 固定维护成本
        单位: 万元 / kilowatt / 年
        """
        assert self.CostPerYear >= 0

        self.VariationalCostPerPower: float = 设备信息.VariationalCostPerPower * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kilowatt_hour <- 元/kWh
        """
        assert self.VariationalCostPerPower >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / kilowatt
        """
        assert self.BuildCostPerWatt >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
            """
            名称: 最大安装台数
            单位: 台
            """
            assert self.MaxDeviceCount >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.MinDeviceCount: float = 设备信息.MinDeviceCount
            """
            名称: 最小安装台数
            单位: 台
            """
            assert self.MinDeviceCount >= 0

        if self.计算参数.计算类型 == "仿真模拟":
            self.DeviceCount: float = 设备信息.DeviceCount
            """
            名称: 安装台数
            单位: 台
            """
            assert self.DeviceCount >= 0

        ##### PORT VARIABLE DEFINITION ####

        self.电输出 = self.变量列表("电输出", within=NonNegativeReals)
        """
        类型: 变压器输出
        """

        self.电输入 = self.变量列表("电输入", within=NegativeReals)
        """
        类型: 电母线输入
        """

        # 设备特有约束（变量）

    def constraints_register(self):
        # 设备特有约束（非变量）

        # 设备台数约束
        if self.计算参数.计算类型 == "规划设计":
            Constraint(self.DeviceCount <= self.MaxDeviceCount)
            Constraint(self.DeviceCount >= self.MinDeviceCount)

        # 输出输入功率约束
        self.RangedConstraint(self.电输入, self.电输出, lambda x, y: x=-y * self.Efficiency)
        self.RangedConstraintMulti(
            self.电输入, expression=lambda x: -x <= self.RatedPower * self.DeviceCount
        )

        # 计算年化
        # unit: one
        Life = self.Life

        年化率 = ((1 + (self.计算参数.年利率 / 100)) ** Life) / Life

        总采购成本 = self.CostPerWatt * (self.DeviceCount * self.RatedPower)
        总固定维护成本 = self.CostPerYear * (self.DeviceCount * self.RatedPower)
        总建设费用 = (
            self.BuildCostPerWatt * (self.DeviceCount * self.RatedPower)
            + self.BuildBaseCost
        )

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总可变维护成本年化 = (
            (-self.SumRange(self.电输入))
            * (8760 / self.计算参数.迭代步数)
            * ((1 if self.计算参数.计算步长 == "小时" else 3600))
            * self.VariationalCostPerPower
        )

        总成本年化 = 总固定成本年化 + 总可变维护成本年化


class 变流器模型(设备模型):
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 变流器ID, 设备信息: 变流器信息):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)
        self.RatedPower: float = 设备信息.RatedPower
        """
        名称: 额定功率
        单位: kilowatt
        """
        assert self.RatedPower >= 0

        self.Efficiency: float = 设备信息.Efficiency * 0.01
        """
        名称: 效率
        单位: one <- percent
        """
        assert self.Efficiency >= 0

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / kilowatt
        """
        assert self.CostPerWatt >= 0

        self.CostPerYear: float = 设备信息.CostPerYear
        """
        名称: 固定维护成本
        单位: 万元 / kilowatt / 年
        """
        assert self.CostPerYear >= 0

        self.VariationalCostPerPower: float = 设备信息.VariationalCostPerPower * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kilowatt_hour <- 元/kWh
        """
        assert self.VariationalCostPerPower >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / kilowatt
        """
        assert self.BuildCostPerWatt >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
            """
            名称: 最大安装台数
            单位: 台
            """
            assert self.MaxDeviceCount >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.MinDeviceCount: float = 设备信息.MinDeviceCount
            """
            名称: 最小安装台数
            单位: 台
            """
            assert self.MinDeviceCount >= 0

        if self.计算参数.计算类型 == "仿真模拟":
            self.DeviceCount: float = 设备信息.DeviceCount
            """
            名称: 安装台数
            单位: 台
            """
            assert self.DeviceCount >= 0

        ##### PORT VARIABLE DEFINITION ####

        self.电输入 = self.变量列表("电输入", within=NegativeReals)
        """
        类型: 变流器输入
        """

        self.电输出 = self.变量列表("电输出", within=NonNegativeReals)
        """
        类型: 电母线输出
        """

        # 设备特有约束（变量）

    def constraints_register(self):
        # 设备特有约束（非变量）

        # 设备台数约束
        if self.计算参数.计算类型 == "规划设计":
            Constraint(self.DeviceCount <= self.MaxDeviceCount)
            Constraint(self.DeviceCount >= self.MinDeviceCount)

        # 输出输入功率约束
        self.RangedConstraint(self.电输入, self.电输出, lambda x, y: x=-y * self.Efficiency)
        self.RangedConstraintMulti(
            self.电输入, expression=lambda x: -x <= self.RatedPower * self.DeviceCount
        )

        # 计算年化
        # unit: one
        Life = self.Life

        年化率 = ((1 + (self.计算参数.年利率 / 100)) ** Life) / Life

        总采购成本 = self.CostPerWatt * (self.DeviceCount * self.RatedPower)
        总固定维护成本 = self.CostPerYear * (self.DeviceCount * self.RatedPower)
        总建设费用 = (
            self.BuildCostPerWatt * (self.DeviceCount * self.RatedPower)
            + self.BuildBaseCost
        )

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总可变维护成本年化 = (
            (-self.SumRange(self.电输入))
            * (8760 / self.计算参数.迭代步数)
            * ((1 if self.计算参数.计算步长 == "小时" else 3600))
            * self.VariationalCostPerPower
        )

        总成本年化 = 总固定成本年化 + 总可变维护成本年化


class 双向变流器模型(设备模型):
    def __init__(
        self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 双向变流器ID, 设备信息: 双向变流器信息
    ):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)
        self.RatedPower: float = 设备信息.RatedPower
        """
        名称: 额定功率
        单位: kilowatt
        """
        assert self.RatedPower >= 0

        self.Efficiency: float = 设备信息.Efficiency * 0.01
        """
        名称: 效率
        单位: one <- percent
        """
        assert self.Efficiency >= 0

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / kilowatt
        """
        assert self.CostPerWatt >= 0

        self.CostPerYear: float = 设备信息.CostPerYear
        """
        名称: 固定维护成本
        单位: 万元 / kilowatt / 年
        """
        assert self.CostPerYear >= 0

        self.VariationalCostPerPower: float = 设备信息.VariationalCostPerPower * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kilowatt_hour <- 元/kWh
        """
        assert self.VariationalCostPerPower >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / kilowatt
        """
        assert self.BuildCostPerWatt >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
            """
            名称: 最大安装台数
            单位: 台
            """
            assert self.MaxDeviceCount >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.MinDeviceCount: float = 设备信息.MinDeviceCount
            """
            名称: 最小安装台数
            单位: 台
            """
            assert self.MinDeviceCount >= 0

        if self.计算参数.计算类型 == "仿真模拟":
            self.DeviceCount: float = 设备信息.DeviceCount
            """
            名称: 安装台数
            单位: 台
            """
            assert self.DeviceCount >= 0

        ##### PORT VARIABLE DEFINITION ####

        self.线路端 = self.变量列表("线路端", within=Reals)
        """
        类型: 双向变流器线路端输入输出
        """

        self.储能端 = self.变量列表("储能端", within=Reals)
        """
        类型: 双向变流器储能端输入输出
        """

        # 设备特有约束（变量）
        self.线路端_ = self.变量列表_带指示变量("线路端_")
        self.储能端_ = self.变量列表_带指示变量("储能端_")

    def constraints_register(self):
        # 设备特有约束（非变量）

        # 设备台数约束
        if self.计算参数.计算类型 == "规划设计":
            Constraint(self.DeviceCount <= self.MaxDeviceCount)
            Constraint(self.DeviceCount >= self.MinDeviceCount)

        # 输出输入功率约束

        self.RangedConstraint(self.线路端_.x, self.线路端, lambda x, y: x == y)
        self.RangedConstraint(self.储能端_.x, self.储能端, lambda x, y: x == y)

        self.RangedConstraint(
            self.线路端_.x_neg, self.储能端_.x_pos, lambda x, y: x=y * self.Efficiency
        )
        self.RangedConstraint(
            self.储能端_.x_neg, self.线路端_.x_pos, lambda x, y: x=y * self.Efficiency
        )

        # 计算年化
        # unit: one
        Life = self.Life

        年化率 = ((1 + (self.计算参数.年利率 / 100)) ** Life) / Life

        总采购成本 = self.CostPerWatt * (self.DeviceCount * self.RatedPower)
        总固定维护成本 = self.CostPerYear * (self.DeviceCount * self.RatedPower)
        总建设费用 = (
            self.BuildCostPerWatt * (self.DeviceCount * self.RatedPower)
            + self.BuildBaseCost
        )

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总可变维护成本年化 = (
            ((self.SumRange(self.储能端_.x_neg) + self.SumRange(self.线路端_.x_neg)))
            * (8760 / self.计算参数.迭代步数)
            * ((1 if self.计算参数.计算步长 == "小时" else 3600))
            * self.VariationalCostPerPower
        )

        总成本年化 = 总固定成本年化 + 总可变维护成本年化


class 传输线模型(设备模型):
    def __init__(self, model: ConcreteModel, 计算参数实例: 计算参数, 设备ID: 传输线ID, 设备信息: 传输线信息):
        super().__init__(model=model, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)
        self.PowerTransferDecay: float = 设备信息.PowerTransferDecay
        """
        名称: 能量衰减系数
        单位: kilowatt / kilometer
        """
        assert self.PowerTransferDecay >= 0

        self.CostPerWatt: float = 设备信息.CostPerWatt
        """
        名称: 采购成本
        单位: 万元 / kilometer
        """
        assert self.CostPerWatt >= 0

        self.VariationCostPerMeter: float = 设备信息.VariationCostPerMeter
        """
        名称: 维护成本
        单位: 万元 / kilometer / 年
        """
        assert self.VariationCostPerMeter >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerWatt: float = 设备信息.BuildCostPerWatt
        """
        名称: 建设费用系数
        单位: 万元 / kilometer
        """
        assert self.BuildCostPerWatt >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.Length: float = 设备信息.Length
            """
            名称: 长度
            单位: kilometer
            """
            assert self.Length >= 0

        if self.计算参数.计算类型 == "仿真模拟":
            self.Length: float = 设备信息.Length
            """
            名称: 长度
            单位: kilometer
            """
            assert self.Length >= 0

        ##### PORT VARIABLE DEFINITION ####

        self.电输入 = self.变量列表("电输入", within=NegativeReals)
        """
        类型: 电母线输入
        """

        self.电输出 = self.变量列表("电输出", within=NonNegativeReals)
        """
        类型: 电母线输出
        """

        # 设备特有约束（变量）
        self.电输入_去除损耗 = self.变量列表_带指示变量("电输入_去除损耗")

    def constraints_register(self):
        # 设备特有约束（非变量）

        # 设备台数约束

        # 输出输入功率约束
        TotalDecayPerStep = (
            self.Length
            * self.PowerTransferDecay
            / (1 if self.计算参数.计算步长 == "小时" else 3600)
        )
        self.RangedConstraint(
            self.电输入_去除损耗.x, self.电输入, lambda x, y: x == y + TotalDecayPerStep
        )
        self.RangedConstraint(self.电输入_去除损耗.x_neg, self.电输出, lambda x, y: x == y)

        # 计算年化
        # unit: one
        Life = self.Life

        年化率 = ((1 + (self.计算参数.年利率 / 100)) ** Life) / Life

        总采购成本 = self.CostPerWatt * (self.Length)
        总固定维护成本 = self.CostPerYear * (self.Length)
        总建设费用 = self.BuildCostPerWatt * (self.Length) + self.BuildBaseCost

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总可变维护成本年化 = (
            (-self.SumRange(self.电输入))
            * (8760 / self.计算参数.迭代步数)
            * ((1 if self.计算参数.计算步长 == "小时" else 3600))
            * self.VariationalCostPerPower
        )

        总成本年化 = 总固定成本年化 + 总可变维护成本年化
