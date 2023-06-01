# TODO: 典型日 最终输出结果需要展开为8760
from typing import Dict, List, Literal, Union

import rich
from pydantic import BaseModel

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

# string, digits, tables.
# you can dump and load from json.


#############
# Device ID #
#############


class 设备ID(BaseModel):
    ID: int


class 柴油ID(设备ID):
    燃料接口: int
    """
    类型: 柴油输出
    """


class 电负荷ID(设备ID):
    电接口: int
    """
    类型: 负荷电输入
    """


class 光伏发电ID(设备ID):
    电接口: int
    """
    类型: 供电端输出
    """


class 风力发电ID(设备ID):
    电接口: int
    """
    类型: 供电端输出
    """


class 柴油发电ID(设备ID):
    燃料接口: int
    """
    类型: 柴油输入
    """
    电接口: int
    """
    类型: 供电端输出
    """


class 锂电池ID(设备ID):
    电接口: int
    """
    类型: 电储能端输入输出
    """


class 变压器ID(设备ID):
    电输出: int
    """
    类型: 变压器输出
    """
    电输入: int
    """
    类型: 电母线输入
    """


class 变流器ID(设备ID):
    电输入: int
    """
    类型: 变流器输入
    """
    电输出: int
    """
    类型: 电母线输出
    """


class 双向变流器ID(设备ID):
    线路端: int
    """
    类型: 双向变流器线路端输入输出
    """
    储能端: int
    """
    类型: 双向变流器储能端输入输出
    """


class 传输线ID(设备ID):
    电输出: int
    """
    类型: 电母线输出
    """
    电输入: int
    """
    类型: 电母线输入
    """


###############
# Device Info #
###############


class 柴油信息(BaseModel):
    Price: float
    Unit: str
    DefaultUnit: str = "L/万元"


class 电负荷信息(BaseModel):
    # 正数
    EnergyConsumption: List[float]
    """
    单位: kW
    """

    MaxEnergyConsumption: Union[None, float] = None
    """
    单位: kW
    """


class 光伏发电信息(BaseModel):
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

    CostPerKilowatt: float
    """
    名称: 采购成本
    单位: 万元/kWp
    """

    CostPerYearPerKilowatt: float
    """
    名称: 固定维护成本
    单位: 万元/(kWp*年)
    """

    VariationalCostPerWork: float
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerKilowatt: float
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

    DeviceCount: float
    """
    名称: 安装台数
    单位: 台
    """


class 风力发电信息(BaseModel):
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

    CostPerKilowatt: float
    """
    名称: 采购成本
    单位: 万元/kWp
    """

    CostPerYearPerKilowatt: float
    """
    名称: 固定维护成本
    单位: 万元/(kWp*年)
    """

    VariationalCostPerWork: float
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerKilowatt: float
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


class 柴油发电信息(BaseModel):
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

    CostPerMachine: float
    """
    名称: 采购成本
    单位: 万元/台
    """

    CostPerYearPerMachine: float
    """
    名称: 固定维护成本
    单位: 万元/(台*年)
    """

    VariationalCostPerWork: float
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerMachine: float
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

    DieselToPower_Load: List[List[float]]
    """
    DieselToPower: 燃油消耗率
    单位: L/kWh

    Load: 负载率
    单位: percent
    """


class 锂电池信息(BaseModel):
    生产厂商: str

    设备型号: str

    循环边界条件: str

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

    CostPerCapacity: float
    """
    名称: 采购成本
    单位: 万元/kWh
    """

    CostPerYearPerCapacity: float
    """
    名称: 固定维护成本
    单位: 万元/(kWh*年)
    """

    VariationalCostPerWork: float
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerCapacity: float
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

    MaxTotalCapacity: float
    """
    名称: 最大设备容量
    单位: kWh
    """

    MinTotalCapacity: float
    """
    名称: 最小设备容量
    单位: kWh
    """

    DeviceCount: float
    """
    名称: 安装台数
    单位: 台
    """


class 变压器信息(BaseModel):
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

    CostPerKilowatt: float
    """
    名称: 采购成本
    单位: 万元/kW
    """

    CostPerYearPerKilowatt: float
    """
    名称: 固定维护成本
    单位: 万元/(kW*年)
    """

    VariationalCostPerWork: float
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerKilowatt: float
    """
    名称: 建设费用系数
    单位: 万元/kW
    """

    BuildBaseCost: float
    """
    名称: 建设费用基数
    单位: 万元
    """

    PowerParameter: float
    """
    名称: 功率因数
    单位: one
    """

    LoadRedundancyParameter: float
    """
    名称: 变压器冗余系数
    单位: one
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

    PowerParameter: float
    """
    名称: 功率因数
    单位: one
    """

    DeviceCount: float
    """
    名称: 安装台数
    单位: 台
    """


class 变流器信息(BaseModel):
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

    CostPerKilowatt: float
    """
    名称: 采购成本
    单位: 万元/kW
    """

    CostPerYearPerKilowatt: float
    """
    名称: 固定维护成本
    单位: 万元/(kW*年)
    """

    VariationalCostPerWork: float
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerKilowatt: float
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


class 双向变流器信息(BaseModel):
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

    CostPerKilowatt: float
    """
    名称: 采购成本
    单位: 万元/kW
    """

    CostPerYearPerKilowatt: float
    """
    名称: 固定维护成本
    单位: 万元/(kW*年)
    """

    VariationalCostPerWork: float
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerKilowatt: float
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


class 传输线信息(BaseModel):
    生产厂商: str

    设备型号: str

    PowerTransferDecay: float
    """
    名称: 能量衰减系数
    单位: kW/km
    """

    CostPerKilometer: float
    """
    名称: 采购成本
    单位: 万元/km
    """

    CostPerYearPerKilometer: float
    """
    名称: 维护成本
    单位: 万元/(km*年)
    """

    Life: float
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerKilometer: float
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


class ModelWrapper:
    def __init__(self):
        self.model = ConcreteModel()
        self.clock = {}

    def getSpecialName(self, key: str):
        val = self.clock.get(key, 0)
        name = f"{key}_{val}"
        self.clock[key] = val + 1
        return name

    def Constraint(self, *args, **kwargs):
        name = self.getSpecialName("CON")
        ret = Constraint(expr=args[0], *args[1:], **kwargs)
        self.model.__setattr__(name, ret)
        return ret

    def Var(self, name: str, *args, **kwargs):
        ret = Var(*args, **kwargs)
        self.model.__setattr__(name, ret)
        return ret

    def Objective(self, *args, **kwargs):
        name = self.getSpecialName("OBJ")
        ret = Objective(expr=args[0], *args[1:], **kwargs)
        self.model.__setattr__(name, ret)
        return ret


# first convert the unit.
# assign variables.

# shall you assign port with variables.

# 风、光照

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
    年利率: float
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

    @property
    def 时间参数(self):
        return 1 if self.计算步长 == "小时" else 3600


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
    def __init__(self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, ID):
        print("Building Device Model:", self.__class__.__name__)
        self.mw = mw
        self.PD = PD
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

    def constraints_register(self):
        print("REGISTERING: ", self.__class__.__name__)

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
        var = self.mw.Var(self.getVarName(varName), **kwargs)
        return var

    def 变量列表(self, varName: str, **kwargs):
        var = self.mw.Var(self.getVarName(varName), range(self.计算参数.迭代步数), **kwargs)
        return var

    def RangeConstraint(self, var_1, var_2, expression):
        for i in range(self.计算参数.迭代步数):
            self.mw.Constraint(expression(var_1[i], var_2[i]))

    def RangeConstraintMulti(self, *vars, expression=...):  # keyword argument now.
        assert expression is not ...
        for i in range(self.计算参数.迭代步数):
            self.mw.Constraint(expression(*[var[i] for var in vars]))

    def CustomRangeConstraint(self, var_1, var_2, customRange: range, expression):
        for i in customRange:
            self.mw.Constraint(expression(var_1, var_2, i))

    def CustomRangeConstraintMulti(
        self, *vars, customRange: range = ..., expression=...
    ):
        assert expression is not ...
        assert customRange is not ...
        for i in customRange:
            self.mw.Constraint(expression(*vars, i))

    def SumRange(self, var_1):
        return reduce(
            sequence=[var_1[i] for i in range(self.计算参数.迭代步数)],
            function=lambda x, y: x + y,
        )

    def 单变量转列表(self, var, dup=None):
        if dup is None:
            dup = self.计算参数.迭代步数
        return [var for _ in range(dup)]

    def 变量列表_带指示变量(self, varName: str, within=Reals) -> POSNEG:
        x = self.变量列表(varName, within=within)

        b_pos = self.变量列表(self.getSpecialVarName(varName), within=Boolean)
        x_pos = self.变量列表(self.getSpecialVarName(varName), within=NonNegativeReals)

        self.RangeConstraint(b_pos, x_pos, lambda x, y: x * self.BigM >= y)
        b_neg = self.变量列表(self.getSpecialVarName(varName), within=Boolean)
        x_neg = self.变量列表(self.getSpecialVarName(varName), within=NonNegativeReals)

        self.RangeConstraint(b_neg, x_neg, lambda x, y: x * self.BigM >= y)

        self.RangeConstraint(b_pos, b_neg, lambda x, y: x + y == 1)

        self.RangeConstraintMulti(
            x, x_pos, x_neg, expression=lambda x, y, z: x == y - z
        )

        x_abs = self.变量列表(self.getSpecialVarName(varName), within=NonNegativeReals)

        self.RangeConstraintMulti(
            x_pos, x_neg, x_abs, expression=lambda x, y, z: z == x + y
        )

        posneg = POSNEG(x, x_pos, x_neg, b_pos, b_neg, x_abs)

        return posneg

    def Piecewise(
        self,
        x_var,  # x_var
        y_var,  # y_var
        x_vals: List[float],
        y_vals: List[float],
        range_list: Union[List[int], None] = None,
        pw_repn="SOS2",
        pw_constr_type="EQ",
        unbounded_domain_var=True,
    ):
        if range_list is None:
            range_list = list(range(self.计算参数.迭代步数))
        piecewise_name = self.getSpecialVarName("PW")
        PW = Piecewise(
            *range_list,
            y_var,
            x_var,
            pw_pts=x_vals,
            f_rule=y_vals,
            valspw_repn=pw_repn,
            pw_constr_type=pw_constr_type,
            unbounded_domain_var=unbounded_domain_var,
        )
        self.mw.model.__setattr__(piecewise_name, PW)
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
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 光伏发电ID, 设备信息: 光伏发电信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

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
        单位: kWp
        """
        assert self.MaxPower >= 0

        self.PowerDeltaLimit: float = 设备信息.PowerDeltaLimit
        """
        名称: 发电爬坡率
        单位: percent/s
        """
        assert self.PowerDeltaLimit >= 0

        self.CostPerKilowatt: float = 设备信息.CostPerKilowatt
        """
        名称: 采购成本
        单位: 万元/kWp
        """
        assert self.CostPerKilowatt >= 0

        self.CostPerYearPerKilowatt: float = 设备信息.CostPerYearPerKilowatt
        """
        名称: 固定维护成本
        单位: 万元/(kWp*年)
        """
        assert self.CostPerYearPerKilowatt >= 0

        self.VariationalCostPerWork: float = 设备信息.VariationalCostPerWork * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kWh <- 元/kWh
        """
        assert self.VariationalCostPerWork >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerKilowatt: float = 设备信息.BuildCostPerKilowatt
        """
        名称: 建设费用系数
        单位: 万元/kWp
        """
        assert self.BuildCostPerKilowatt >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)  # type: ignore
            """
            单位： 个
            """

            self.MaxInstallArea: float = 设备信息.MaxInstallArea
            """
            名称: 最大安装面积
            单位: m2
            """
            assert self.MaxInstallArea >= 0

            self.MinInstallArea: float = 设备信息.MinInstallArea
            """
            名称: 最小安装面积
            单位: m2
            """
            assert self.MinInstallArea >= 0

        if self.计算参数.计算类型 == "仿真模拟":
            self.DeviceCount: float = 设备信息.DeviceCount
            """
            名称: 安装台数
            单位: 台
            """
            assert self.DeviceCount >= 0

        ##### PORT VARIABLE DEFINITION ####

        self.ports = {}

        self.PD[self.设备ID.电接口] = self.ports["电接口"] = self.电接口 = self.变量列表(
            "电接口", within=NonNegativeReals
        )
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
        super().constraints_register()
        # 设备特有约束（非变量）

        # 设备台数约束
        if self.计算参数.计算类型 == "规划设计":
            self.mw.Constraint(self.DeviceCount <= self.MaxDeviceCount)
            self.mw.Constraint(self.DeviceCount >= self.MinDeviceCount)

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

        总采购成本 = self.CostPerKilowatt * (总最大功率)
        总固定维护成本 = self.CostPerYearPerKilowatt * (总最大功率)
        总建设费用 = self.BuildCostPerKilowatt * (总最大功率) + self.BuildBaseCost

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总可变维护成本年化 = (
            ((self.SumRange(self.电输出)) / self.计算参数.迭代步数)
            * 8760
            * self.VariationalCostPerWork
        )
        # avg_power * 8760 = annual_work

        总成本年化 = 总固定成本年化 + 总可变维护成本年化

        return 总成本年化


class 风力发电模型(设备模型):
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 风力发电ID, 设备信息: 风力发电信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.RatedPower: float = 设备信息.RatedPower
        """
        名称: 额定功率
        单位: kWp
        """
        assert self.RatedPower >= 0

        self.RatedWindSpeed: float = 设备信息.RatedWindSpeed
        """
        名称: 额定风速
        单位: m/s
        """
        assert self.RatedWindSpeed >= 0

        self.MinWindSpeed: float = 设备信息.MinWindSpeed
        """
        名称: 切入风速
        单位: m/s
        """
        assert self.MinWindSpeed >= 0

        self.MaxWindSpeed: float = 设备信息.MaxWindSpeed
        """
        名称: 切出风速
        单位: m/s
        """
        assert self.MaxWindSpeed >= 0

        self.PowerDeltaLimit: float = 设备信息.PowerDeltaLimit
        """
        名称: 发电爬坡率
        单位: percent/s
        """
        assert self.PowerDeltaLimit >= 0

        self.CostPerKilowatt: float = 设备信息.CostPerKilowatt
        """
        名称: 采购成本
        单位: 万元/kWp
        """
        assert self.CostPerKilowatt >= 0

        self.CostPerYearPerKilowatt: float = 设备信息.CostPerYearPerKilowatt
        """
        名称: 固定维护成本
        单位: 万元/(kWp*年)
        """
        assert self.CostPerYearPerKilowatt >= 0

        self.VariationalCostPerWork: float = 设备信息.VariationalCostPerWork * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kWh <- 元/kWh
        """
        assert self.VariationalCostPerWork >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerKilowatt: float = 设备信息.BuildCostPerKilowatt
        """
        名称: 建设费用系数
        单位: 万元/kWp
        """
        assert self.BuildCostPerKilowatt >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)  # type: ignore
            """
            单位： 个
            """

            self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
            """
            名称: 最大安装台数
            单位: 台
            """
            assert self.MaxDeviceCount >= 0

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

        self.ports = {}

        self.PD[self.设备ID.电接口] = self.ports["电接口"] = self.电接口 = self.变量列表(
            "电接口", within=NonNegativeReals
        )
        """
        类型: 供电端输出
        """

        # 设备特有约束（变量）
        self.电输出 = self.电接口

    def constraints_register(self):
        super().constraints_register()
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
            self.mw.Constraint(self.DeviceCount <= self.MaxDeviceCount)
            self.mw.Constraint(self.DeviceCount >= self.MinDeviceCount)

        # 输出输入功率约束
        self.RangeConstraint(单台发电功率, self.电输出, lambda x, y: x * self.DeviceCount >= y)

        if self.计算参数.计算步长 == "秒":
            总最大功率 = self.RatedPower * self.DeviceCount
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

        总采购成本 = self.CostPerKilowatt * (self.DeviceCount * self.RatedPower)
        总固定维护成本 = self.CostPerYearPerKilowatt * (self.DeviceCount * self.RatedPower)
        总建设费用 = (
            self.BuildCostPerKilowatt * (self.DeviceCount * self.RatedPower)
            + self.BuildBaseCost
        )

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总可变维护成本年化 = (
            ((self.SumRange(self.电输出)) / self.计算参数.迭代步数)
            * 8760
            * self.VariationalCostPerWork
        )
        # avg_power * 8760 = annual_work

        总成本年化 = 总固定成本年化 + 总可变维护成本年化

        return 总成本年化


class 柴油发电模型(设备模型):
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 柴油发电ID, 设备信息: 柴油发电信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.RatedPower: float = 设备信息.RatedPower
        """
        名称: 额定功率
        单位: kW
        """
        assert self.RatedPower >= 0

        self.PowerDeltaLimit: float = 设备信息.PowerDeltaLimit
        """
        名称: 发电爬坡率
        单位: percent/s
        """
        assert self.PowerDeltaLimit >= 0

        self.PowerStartupLimit: float = 设备信息.PowerStartupLimit * 0.01
        """
        名称: 启动功率百分比
        单位: one <- percent
        """
        assert self.PowerStartupLimit >= 0

        self.CostPerMachine: float = 设备信息.CostPerMachine
        """
        名称: 采购成本
        单位: 万元/台
        """
        assert self.CostPerMachine >= 0

        self.CostPerYearPerMachine: float = 设备信息.CostPerYearPerMachine
        """
        名称: 固定维护成本
        单位: 万元/(台*年)
        """
        assert self.CostPerYearPerMachine >= 0

        self.VariationalCostPerWork: float = 设备信息.VariationalCostPerWork * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kWh <- 元/kWh
        """
        assert self.VariationalCostPerWork >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerMachine: float = 设备信息.BuildCostPerMachine
        """
        名称: 建设费用系数
        单位: 万元/台
        """
        assert self.BuildCostPerMachine >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)  # type: ignore
            """
            单位： 个
            """

            self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
            """
            名称: 最大安装台数
            单位: 台
            """
            assert self.MaxDeviceCount >= 0

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
        单位: m3 / kWh <- L/kWh

        Load: 负载率
        单位: one <- percent
        """

        ##### PORT VARIABLE DEFINITION ####

        self.ports = {}

        self.PD[self.设备ID.燃料接口] = self.ports["燃料接口"] = self.燃料接口 = self.变量列表(
            "燃料接口", within=NegativeReals
        )
        """
        类型: 柴油输入
        """

        self.PD[self.设备ID.电接口] = self.ports["电接口"] = self.电接口 = self.变量列表(
            "电接口", within=NonNegativeReals
        )
        """
        类型: 供电端输出
        """

        # 设备特有约束（变量）
        self.电输出 = self.电接口
        self.柴油输入 = self.燃料接口

        self.电功率中转 = self.变量列表_带指示变量("电功率中转")

        self.单台发电功率 = self.变量列表("单台发电功率", within=NonNegativeReals)
        self.单台柴油输入 = self.变量列表("单台柴油输入", within=NonPositiveReals)

        if self.计算参数.计算类型 == "设计规划":
            self.最大油耗率 = max([x[0] for x in self.DieselToPower_Load])

            self.原电输出 = self.Multiply(
                dict(var=self.单台发电功率, max=self.RatedPower, min=0),
                dict(
                    var=self.单变量转列表(self.DeviceCount),
                    max=self.MaxDeviceCount,
                    min=self.MinDeviceCount,
                ),
                "原电输出",
                within=NonNegativeReals,
            )

            self.柴油输入_ = self.Multiply(
                dict(var=self.单台柴油输入, max=0, min=-self.RatedPower * self.最大油耗率),
                dict(
                    var=self.单变量转列表(self.DeviceCount),
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
        super().constraints_register()
        # 设备特有约束（非变量）

        # 设备台数约束
        if self.计算参数.计算类型 == "规划设计":
            self.mw.Constraint(self.DeviceCount <= self.MaxDeviceCount)
            self.mw.Constraint(self.DeviceCount >= self.MinDeviceCount)

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
        # 柴油输入率: L/h

        self.RangeConstraintMulti(
            self.电功率中转.x_pos,
            self.电输出,
            self.电功率中转.b_pos,
            expression=lambda x, y, z: x + 总最小启动功率 * z == y,
        )

        if self.计算参数.计算步长 == "秒":
            总最大功率 = self.RatedPower * self.DeviceCount
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

        总采购成本 = self.CostPerMachine * (self.DeviceCount)
        总固定维护成本 = self.CostPerYearPerMachine * (self.DeviceCount)
        总建设费用 = self.BuildCostPerMachine * (self.DeviceCount) + self.BuildBaseCost

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总可变维护成本年化 = (
            ((self.SumRange(self.电输出)) / self.计算参数.迭代步数)
            * 8760
            * self.VariationalCostPerWork
        )
        # avg_power * 8760 = annual_work

        总成本年化 = 总固定成本年化 + 总可变维护成本年化

        return 总成本年化


class 锂电池模型(设备模型):
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 锂电池ID, 设备信息: 锂电池信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.RatedCapacity: float = 设备信息.RatedCapacity
        """
        名称: 额定容量
        单位: kWh
        """
        assert self.RatedCapacity >= 0

        self.BatteryDeltaLimit: float = 设备信息.BatteryDeltaLimit
        """
        名称: 电池充放电倍率
        单位: 1/hour
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
        单位: percent/hour
        """
        assert self.BatteryStorageDecay >= 0

        self.TotalDischargeCapacity: float = 设备信息.TotalDischargeCapacity
        """
        名称: 生命周期总放电量
        单位: kWh
        """
        assert self.TotalDischargeCapacity >= 0

        self.BatteryLife: float = 设备信息.BatteryLife
        """
        名称: 电池换芯周期
        单位: 年
        """
        assert self.BatteryLife >= 0

        self.CostPerCapacity: float = 设备信息.CostPerCapacity
        """
        名称: 采购成本
        单位: 万元/kWh
        """
        assert self.CostPerCapacity >= 0

        self.CostPerYearPerCapacity: float = 设备信息.CostPerYearPerCapacity
        """
        名称: 固定维护成本
        单位: 万元/(kWh*年)
        """
        assert self.CostPerYearPerCapacity >= 0

        self.VariationalCostPerWork: float = 设备信息.VariationalCostPerWork * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kWh <- 元/kWh
        """
        assert self.VariationalCostPerWork >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerCapacity: float = 设备信息.BuildCostPerCapacity
        """
        名称: 建设费用系数
        单位: 万元/kWh
        """
        assert self.BuildCostPerCapacity >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)  # type: ignore
            """
            单位： 个
            """

            self.InitSOC: float = 设备信息.InitSOC * 0.01
            """
            名称: 初始SOC
            单位: one <- percent
            """
            assert self.InitSOC >= 0

            self.MaxTotalCapacity: float = 设备信息.MaxTotalCapacity
            """
            名称: 最大设备容量
            单位: kWh
            """
            assert self.MaxTotalCapacity >= 0

            self.MinTotalCapacity: float = 设备信息.MinTotalCapacity
            """
            名称: 最小设备容量
            单位: kWh
            """
            assert self.MinTotalCapacity >= 0

        if self.计算参数.计算类型 == "仿真模拟":
            self.DeviceCount: float = 设备信息.DeviceCount
            """
            名称: 安装台数
            单位: 台
            """
            assert self.DeviceCount >= 0

        ##### PORT VARIABLE DEFINITION ####

        self.ports = {}

        self.PD[self.设备ID.电接口] = self.ports["电接口"] = self.电接口 = self.变量列表(
            "电接口", within=Reals
        )
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

        self.TotalCapacity = self.DeviceCount * self.RatedCapacity  # type: ignore

        self.TotalActualCapacity = self.DeviceCount * self.ActualCapacityPerUnit  # type: ignore

        self.MaxTotalCapacityDeltaPerStep = (
            self.BatteryDeltaLimit * self.TotalCapacity / (self.计算参数.时间参数)
        )
        """
        单位: kWh
        """

        self.TotalStorageDecayRate = (
            self.BatteryStorageDecay / 100
        ) * self.TotalCapacity
        """
        单位: kW
        """

    def constraints_register(self):
        super().constraints_register()
        # 设备特有约束（非变量）

        # 设备台数约束
        if self.计算参数.计算类型 == "规划设计":
            self.mw.Constraint(self.DeviceCount <= self.MaxDeviceCount)
            self.mw.Constraint(self.DeviceCount >= self.MinDeviceCount)

        # 输出输入功率约束
        self.RangeConstraintMulti(
            self.CurrentTotalActualCapacity,
            expression=lambda x: x <= self.TotalActualCapacity,
        )

        self.mw.Constraint(
            self.CurrentTotalActualCapacity[0]
            == self.InitActualCapacityPerUnit * self.DeviceCount
        )

        self.CustomRangeConstraint(
            self.原电接口.x,
            self.CurrentTotalActualCapacity,
            range(self.计算参数.迭代步数 - 1),
            lambda x, y, i: x == (y[i] - y[i + 1]) * self.计算参数.时间参数,
        )

        self.RangeConstraintMulti(
            self.原电接口.x_pos,
            self.原电接口.x_neg,
            self.电接口,
            expression=lambda x_pos, x_neg, y: x_pos * self.DischargeEfficiency
            - (x_neg + self.TotalStorageDecayRate) / self.ChargeEfficiency
            == y,
        )

        for i in range(self.计算参数.迭代步数 - 1):
            self.mw.Constraint(
                self.CurrentTotalActualCapacity[i + 1]
                - self.CurrentTotalActualCapacity[i]
                < self.MaxTotalCapacityDeltaPerStep
            )
            self.mw.Constraint(
                self.CurrentTotalActualCapacity[i + 1]
                - self.CurrentTotalActualCapacity[i]
                > -self.MaxTotalCapacityDeltaPerStep
            )

        if self.计算参数.计算类型 == "设计规划":
            if self.设备信息.循环边界条件 == "日间独立":
                self.mw.Constraint(self.原电接口.x[0] == self.EPS)
            elif self.设备信息.循环边界条件 == "日间连接":
                self.mw.Constraint(
                    self.CurrentTotalActualCapacity[0]
                    - self.CurrentTotalActualCapacity[self.计算参数.迭代步数 - 1]
                    < self.MaxTotalCapacityDeltaPerStep
                )

                self.mw.Constraint(
                    self.CurrentTotalActualCapacity[0]
                    - self.CurrentTotalActualCapacity[self.计算参数.迭代步数 - 1]
                    > -self.MaxTotalCapacityDeltaPerStep
                )

                self.mw.Constraint(
                    self.原电接口.x[0]
                    == (
                        self.CurrentTotalActualCapacity[self.计算参数.迭代步数 - 1]
                        - self.CurrentTotalActualCapacity[0]
                    )
                    * self.计算参数.时间参数
                )
            else:
                raise Exception("未知循环边界条件:", self.设备信息.循环边界条件)
        elif self.计算参数.计算类型 == "仿真模拟":
            self.mw.Constraint(self.原电接口.x[0] == self.EPS)

        # 计算年化
        # unit: one

        计算范围内总平均功率 = (
            self.SumRange(self.原电接口.x_abs) / self.计算参数.迭代步数
        ) + self.TotalStorageDecayRate  # kW
        # avg power

        一小时总电变化量 = 计算范围内总平均功率  # 省略乘1
        # kWh

        一年总电变化量 = 一小时总电变化量 * 8760

        self.mw.Constraint(
            一年总电变化量 * self.BatteryLife
            <= self.DeviceCount * self.TotalDischargeCapacity * 0.85
        )
        assert self.BatteryLife >= 1
        assert self.Life >= self.BatteryLife
        Life = self.BatteryLife

        年化率 = ((1 + (self.计算参数.年利率 / 100)) ** Life) / Life

        总采购成本 = self.CostPerCapacity * (self.DeviceCount * self.RatedCapacity)
        总固定维护成本 = self.CostPerYearPerCapacity * (self.DeviceCount * self.RatedCapacity)
        总建设费用 = (
            self.BuildCostPerCapacity * (self.DeviceCount * self.RatedCapacity)
            + self.BuildBaseCost
        )

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总可变维护成本年化 = (
            ((计算范围内总平均功率 * self.计算参数.迭代步数) / self.计算参数.迭代步数)
            * 8760
            * self.VariationalCostPerWork
        )
        # avg_power * 8760 = annual_work

        总成本年化 = 总固定成本年化 + 总可变维护成本年化

        return 总成本年化


class 变压器模型(设备模型):
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 变压器ID, 设备信息: 变压器信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.Efficiency: float = 设备信息.Efficiency * 0.01
        """
        名称: 效率
        单位: one <- percent
        """
        assert self.Efficiency >= 0

        self.RatedPower: float = 设备信息.RatedPower
        """
        名称: 变压器容量
        单位: kW
        """
        assert self.RatedPower >= 0

        self.CostPerKilowatt: float = 设备信息.CostPerKilowatt
        """
        名称: 采购成本
        单位: 万元/kW
        """
        assert self.CostPerKilowatt >= 0

        self.CostPerYearPerKilowatt: float = 设备信息.CostPerYearPerKilowatt
        """
        名称: 固定维护成本
        单位: 万元/(kW*年)
        """
        assert self.CostPerYearPerKilowatt >= 0

        self.VariationalCostPerWork: float = 设备信息.VariationalCostPerWork * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kWh <- 元/kWh
        """
        assert self.VariationalCostPerWork >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerKilowatt: float = 设备信息.BuildCostPerKilowatt
        """
        名称: 建设费用系数
        单位: 万元/kW
        """
        assert self.BuildCostPerKilowatt >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)  # type: ignore
            """
            单位： 个
            """

            self.PowerParameter: float = 设备信息.PowerParameter
            """
            名称: 功率因数
            单位: one
            """
            assert self.PowerParameter >= 0

            self.LoadRedundancyParameter: float = 设备信息.LoadRedundancyParameter
            """
            名称: 变压器冗余系数
            单位: one
            """
            assert self.LoadRedundancyParameter >= 0

            self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
            """
            名称: 最大安装台数
            单位: 台
            """
            assert self.MaxDeviceCount >= 0

            self.MinDeviceCount: float = 设备信息.MinDeviceCount
            """
            名称: 最小安装台数
            单位: 台
            """
            assert self.MinDeviceCount >= 0

        if self.计算参数.计算类型 == "仿真模拟":
            self.PowerParameter: float = 设备信息.PowerParameter
            """
            名称: 功率因数
            单位: one
            """
            assert self.PowerParameter >= 0

            self.DeviceCount: float = 设备信息.DeviceCount
            """
            名称: 安装台数
            单位: 台
            """
            assert self.DeviceCount >= 0

        ##### PORT VARIABLE DEFINITION ####

        self.ports = {}

        self.PD[self.设备ID.电输出] = self.ports["电输出"] = self.电输出 = self.变量列表(
            "电输出", within=NonNegativeReals
        )
        """
        类型: 变压器输出
        """

        self.PD[self.设备ID.电输入] = self.ports["电输入"] = self.电输入 = self.变量列表(
            "电输入", within=NegativeReals
        )
        """
        类型: 电母线输入
        """

        # 设备特有约束（变量）

        if self.计算参数.计算类型 == "设计规划":  # 在变压器和负荷的交换节点处做处理
            self.最大允许的负载总功率 = self.DeviceCount * (self.RatedPower * self.Efficiency) * self.PowerParameter / self.LoadRedundancyParameter  # type: ignore

    def constraints_register(self):
        super().constraints_register()
        # 设备特有约束（非变量）

        # 设备台数约束
        if self.计算参数.计算类型 == "规划设计":
            self.mw.Constraint(self.DeviceCount <= self.MaxDeviceCount)
            self.mw.Constraint(self.DeviceCount >= self.MinDeviceCount)

        # 输出输入功率约束
        self.RangeConstraint(self.电输入, self.电输出, lambda x, y: x == -y * self.Efficiency)
        self.RangeConstraintMulti(
            self.电输入, expression=lambda x: -x <= self.RatedPower * self.DeviceCount
        )

        # 计算年化
        # unit: one
        Life = self.Life

        年化率 = ((1 + (self.计算参数.年利率 / 100)) ** Life) / Life

        总采购成本 = self.CostPerKilowatt * (self.DeviceCount * self.RatedPower)
        总固定维护成本 = self.CostPerYearPerKilowatt * (self.DeviceCount * self.RatedPower)
        总建设费用 = (
            self.BuildCostPerKilowatt * (self.DeviceCount * self.RatedPower)
            + self.BuildBaseCost
        )

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总可变维护成本年化 = (
            ((-self.SumRange(self.电输入)) / self.计算参数.迭代步数)
            * 8760
            * self.VariationalCostPerWork
        )
        # avg_power * 8760 = annual_work

        总成本年化 = 总固定成本年化 + 总可变维护成本年化

        return 总成本年化


class 变流器模型(设备模型):
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 变流器ID, 设备信息: 变流器信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.RatedPower: float = 设备信息.RatedPower
        """
        名称: 额定功率
        单位: kW
        """
        assert self.RatedPower >= 0

        self.Efficiency: float = 设备信息.Efficiency * 0.01
        """
        名称: 效率
        单位: one <- percent
        """
        assert self.Efficiency >= 0

        self.CostPerKilowatt: float = 设备信息.CostPerKilowatt
        """
        名称: 采购成本
        单位: 万元/kW
        """
        assert self.CostPerKilowatt >= 0

        self.CostPerYearPerKilowatt: float = 设备信息.CostPerYearPerKilowatt
        """
        名称: 固定维护成本
        单位: 万元/(kW*年)
        """
        assert self.CostPerYearPerKilowatt >= 0

        self.VariationalCostPerWork: float = 设备信息.VariationalCostPerWork * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kWh <- 元/kWh
        """
        assert self.VariationalCostPerWork >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerKilowatt: float = 设备信息.BuildCostPerKilowatt
        """
        名称: 建设费用系数
        单位: 万元/kW
        """
        assert self.BuildCostPerKilowatt >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)  # type: ignore
            """
            单位： 个
            """

            self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
            """
            名称: 最大安装台数
            单位: 台
            """
            assert self.MaxDeviceCount >= 0

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

        self.ports = {}

        self.PD[self.设备ID.电输入] = self.ports["电输入"] = self.电输入 = self.变量列表(
            "电输入", within=NegativeReals
        )
        """
        类型: 变流器输入
        """

        self.PD[self.设备ID.电输出] = self.ports["电输出"] = self.电输出 = self.变量列表(
            "电输出", within=NonNegativeReals
        )
        """
        类型: 电母线输出
        """

        # 设备特有约束（变量）

    def constraints_register(self):
        super().constraints_register()
        # 设备特有约束（非变量）

        # 设备台数约束
        if self.计算参数.计算类型 == "规划设计":
            self.mw.Constraint(self.DeviceCount <= self.MaxDeviceCount)
            self.mw.Constraint(self.DeviceCount >= self.MinDeviceCount)

        # 输出输入功率约束
        self.RangeConstraint(self.电输入, self.电输出, lambda x, y: x == -y * self.Efficiency)
        self.RangeConstraintMulti(
            self.电输入, expression=lambda x: -x <= self.RatedPower * self.DeviceCount
        )

        # 计算年化
        # unit: one
        Life = self.Life

        年化率 = ((1 + (self.计算参数.年利率 / 100)) ** Life) / Life

        总采购成本 = self.CostPerKilowatt * (self.DeviceCount * self.RatedPower)
        总固定维护成本 = self.CostPerYearPerKilowatt * (self.DeviceCount * self.RatedPower)
        总建设费用 = (
            self.BuildCostPerKilowatt * (self.DeviceCount * self.RatedPower)
            + self.BuildBaseCost
        )

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总可变维护成本年化 = (
            ((-self.SumRange(self.电输入)) / self.计算参数.迭代步数)
            * 8760
            * self.VariationalCostPerWork
        )
        # avg_power * 8760 = annual_work

        总成本年化 = 总固定成本年化 + 总可变维护成本年化

        return 总成本年化


class 双向变流器模型(设备模型):
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 双向变流器ID, 设备信息: 双向变流器信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.RatedPower: float = 设备信息.RatedPower
        """
        名称: 额定功率
        单位: kW
        """
        assert self.RatedPower >= 0

        self.Efficiency: float = 设备信息.Efficiency * 0.01
        """
        名称: 效率
        单位: one <- percent
        """
        assert self.Efficiency >= 0

        self.CostPerKilowatt: float = 设备信息.CostPerKilowatt
        """
        名称: 采购成本
        单位: 万元/kW
        """
        assert self.CostPerKilowatt >= 0

        self.CostPerYearPerKilowatt: float = 设备信息.CostPerYearPerKilowatt
        """
        名称: 固定维护成本
        单位: 万元/(kW*年)
        """
        assert self.CostPerYearPerKilowatt >= 0

        self.VariationalCostPerWork: float = 设备信息.VariationalCostPerWork * 0.0001
        """
        名称: 可变维护成本
        单位: 万元 / kWh <- 元/kWh
        """
        assert self.VariationalCostPerWork >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerKilowatt: float = 设备信息.BuildCostPerKilowatt
        """
        名称: 建设费用系数
        单位: 万元/kW
        """
        assert self.BuildCostPerKilowatt >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)  # type: ignore
            """
            单位： 个
            """

            self.MaxDeviceCount: float = 设备信息.MaxDeviceCount
            """
            名称: 最大安装台数
            单位: 台
            """
            assert self.MaxDeviceCount >= 0

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

        self.ports = {}

        self.PD[self.设备ID.线路端] = self.ports["线路端"] = self.线路端 = self.变量列表(
            "线路端", within=Reals
        )
        """
        类型: 双向变流器线路端输入输出
        """

        self.PD[self.设备ID.储能端] = self.ports["储能端"] = self.储能端 = self.变量列表(
            "储能端", within=Reals
        )
        """
        类型: 双向变流器储能端输入输出
        """

        # 设备特有约束（变量）

        self.线路端_ = self.变量列表_带指示变量("线路端_")
        self.储能端_ = self.变量列表_带指示变量("储能端_")

    def constraints_register(self):
        super().constraints_register()
        # 设备特有约束（非变量）

        # 设备台数约束
        if self.计算参数.计算类型 == "规划设计":
            self.mw.Constraint(self.DeviceCount <= self.MaxDeviceCount)
            self.mw.Constraint(self.DeviceCount >= self.MinDeviceCount)

        # 输出输入功率约束

        self.RangeConstraint(self.线路端_.x, self.线路端, lambda x, y: x == y)
        self.RangeConstraint(self.储能端_.x, self.储能端, lambda x, y: x == y)

        self.RangeConstraint(
            self.线路端_.x_neg, self.储能端_.x_pos, lambda x, y: x == y * self.Efficiency
        )
        self.RangeConstraint(
            self.储能端_.x_neg, self.线路端_.x_pos, lambda x, y: x == y * self.Efficiency
        )

        # 计算年化
        # unit: one
        Life = self.Life

        年化率 = ((1 + (self.计算参数.年利率 / 100)) ** Life) / Life

        总采购成本 = self.CostPerKilowatt * (self.DeviceCount * self.RatedPower)
        总固定维护成本 = self.CostPerYearPerKilowatt * (self.DeviceCount * self.RatedPower)
        总建设费用 = (
            self.BuildCostPerKilowatt * (self.DeviceCount * self.RatedPower)
            + self.BuildBaseCost
        )

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总可变维护成本年化 = (
            (
                ((self.SumRange(self.储能端_.x_neg) + self.SumRange(self.线路端_.x_neg)))
                / self.计算参数.迭代步数
            )
            * 8760
            * self.VariationalCostPerWork
        )
        # avg_power * 8760 = annual_work

        总成本年化 = 总固定成本年化 + 总可变维护成本年化

        return 总成本年化


class 传输线模型(设备模型):
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 传输线ID, 设备信息: 传输线信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.PowerTransferDecay: float = 设备信息.PowerTransferDecay
        """
        名称: 能量衰减系数
        单位: kW/km
        """
        assert self.PowerTransferDecay >= 0

        self.CostPerKilometer: float = 设备信息.CostPerKilometer
        """
        名称: 采购成本
        单位: 万元/km
        """
        assert self.CostPerKilometer >= 0

        self.CostPerYearPerKilometer: float = 设备信息.CostPerYearPerKilometer
        """
        名称: 维护成本
        单位: 万元/(km*年)
        """
        assert self.CostPerYearPerKilometer >= 0

        self.Life: float = 设备信息.Life
        """
        名称: 设计寿命
        单位: 年
        """
        assert self.Life >= 0

        self.BuildCostPerKilometer: float = 设备信息.BuildCostPerKilometer
        """
        名称: 建设费用系数
        单位: 万元/km
        """
        assert self.BuildCostPerKilometer >= 0

        self.BuildBaseCost: float = 设备信息.BuildBaseCost
        """
        名称: 建设费用基数
        单位: 万元
        """
        assert self.BuildBaseCost >= 0

        if self.计算参数.计算类型 == "设计规划":
            self.DeviceCount = self.单变量("DeviceCount", within=NonNegativeIntegers)  # type: ignore
            """
            单位： 个
            """

            self.Length: float = 设备信息.Length
            """
            名称: 长度
            单位: km
            """
            assert self.Length >= 0

        if self.计算参数.计算类型 == "仿真模拟":
            self.Length: float = 设备信息.Length
            """
            名称: 长度
            单位: km
            """
            assert self.Length >= 0

        ##### PORT VARIABLE DEFINITION ####

        self.ports = {}

        self.PD[self.设备ID.电输出] = self.ports["电输出"] = self.电输出 = self.变量列表(
            "电输出", within=NonNegativeReals
        )
        """
        类型: 电母线输出
        """

        self.PD[self.设备ID.电输入] = self.ports["电输入"] = self.电输入 = self.变量列表(
            "电输入", within=NegativeReals
        )
        """
        类型: 电母线输入
        """

        # 设备特有约束（变量）

        self.电输入_去除损耗 = self.变量列表_带指示变量("电输入_去除损耗")

    def constraints_register(self):
        super().constraints_register()
        # 设备特有约束（非变量）

        # 设备台数约束

        # 输出输入功率约束
        TotalDecayPerStep = self.Length * self.PowerTransferDecay / self.计算参数.时间参数
        self.RangeConstraint(
            self.电输入_去除损耗.x, self.电输入, lambda x, y: x == y + TotalDecayPerStep
        )
        self.RangeConstraint(self.电输入_去除损耗.x_neg, self.电输出, lambda x, y: x == y)

        # 计算年化
        # unit: one
        Life = self.Life

        年化率 = ((1 + (self.计算参数.年利率 / 100)) ** Life) / Life

        总采购成本 = self.CostPerKilometer * (self.Length)
        总固定维护成本 = self.CostPerYearPerKilometer * (self.Length)
        总建设费用 = self.BuildCostPerKilometer * (self.Length) + self.BuildBaseCost

        总固定成本年化 = (总采购成本 + 总固定维护成本 + 总建设费用) * 年化率

        总成本年化 = 总固定成本年化

        return 总成本年化


import pint

from unit_utils import (
    unitFactorCalculator,
    ureg,
    standard_units,
    getSingleUnitConverted,
    translateUnit,
)


class 电负荷模型(设备模型):
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 电负荷ID, 设备信息: 电负荷信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        ##### PORT VARIABLE DEFINITION ####

        self.ports = {}

        self.PD[self.设备ID.电接口] = self.ports["电接口"] = self.电接口 = self.变量列表(
            "电接口", within=NegativeReals
        )
        """
        类型: 负荷电输入
        """

        assert len(self.设备信息.EnergyConsumption) == self.计算参数.迭代步数

        MaxEnergyConsumptionDefault = max(self.设备信息.EnergyConsumption)
        if self.设备信息.MaxEnergyConsumption is None:
            self.MaxEnergyConsumption = MaxEnergyConsumptionDefault
        else:
            assert self.设备信息.MaxEnergyConsumption >= MaxEnergyConsumptionDefault
            self.MaxEnergyConsumption = self.设备信息.MaxEnergyConsumption

    def constraints_register(self):
        super().constraints_register()
        self.RangeConstraint(
            self.电接口, self.设备信息.EnergyConsumption, lambda x, y: x == -y
        )
        年化费用 = 0
        return 年化费用


class 柴油模型(设备模型):
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 柴油ID, 设备信息: 柴油信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        ##### PORT VARIABLE DEFINITION ####

        self.ports = {}

        self.PD[self.设备ID.燃料接口] = self.ports["燃料接口"] = self.燃料接口 = self.变量列表(
            "燃料接口", within=NonNegativeReals
        )
        """
        类型: 柴油输出
        """

        ### UNIT COMPATIBILITY CHECK ###
        default_unit = self.设备信息.DefaultUnit
        val_unit = self.设备信息.Unit

        has_exception, _ = getSingleUnitConverted(
            default_unit=default_unit, val_unit=val_unit
        )

        if has_exception:
            raise Exception(
                f"Unit '{val_unit}' is not compatible with default unit '{default_unit}'"
            )
        ### UNIT COMPATIBILITY CHECK ###

        ### UNIT CONVERSION ###
        self.ConversionRate, self.StandardUnit = unitFactorCalculator(
            ureg, standard_units, val_unit
        )
        ### UNIT CONVERSION ###

        self.Price = self.设备信息.Price * self.ConversionRate
        self.Unit = str(self.StandardUnit)

    def constraints_register(self):
        super().constraints_register()
        平均消耗率 = self.SumRange(self.燃料接口) / self.计算参数.迭代步数

        年化费用 = 平均消耗率 * self.Price * 8760

        return 年化费用


class ModelWrapperContext:
    def __init__(self):
        mw = ModelWrapper()
        self.mw = mw

    def __enter__(self):
        print("ENTER MODEL WRAPPER CONTEXT")
        return self.mw

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # we don't have to take care of this.
        if exc_type == None:
            print("NO ERROR IN MODEL WRAPPER CONTEXT")
        else:
            print("ERROR IN MODEL WRAPPER CONTEXT")
        del self.mw.model
        del self.mw
        print("EXITING MODEL WRAPPER CONTEXT")


devInstClassMap: Dict[str, 设备模型] = {
    "柴油": 柴油模型,
    "电负荷": 电负荷模型,
    "光伏发电": 光伏发电模型,
    "风力发电": 风力发电模型,
    "柴油发电": 柴油发电模型,
    "锂电池": 锂电池模型,
    "变压器": 变压器模型,
    "变流器": 变流器模型,
    "双向变流器": 双向变流器模型,
    "传输线": 传输线模型,
}  # type: ignore

devIDClassMap: Dict[str, 设备ID] = {
    "柴油": 柴油ID,
    "电负荷": 电负荷ID,
    "光伏发电": 光伏发电ID,
    "风力发电": 风力发电ID,
    "柴油发电": 柴油发电ID,
    "锂电池": 锂电池ID,
    "变压器": 变压器ID,
    "变流器": 变流器ID,
    "双向变流器": 双向变流器ID,
    "传输线": 传输线ID,
}  # type: ignore

devInfoClassMap: Dict[str, BaseModel] = {
    "柴油": 柴油信息,
    "电负荷": 电负荷信息,
    "光伏发电": 光伏发电信息,
    "风力发电": 风力发电信息,
    "柴油发电": 柴油发电信息,
    "锂电池": 锂电池信息,
    "变压器": 变压器信息,
    "变流器": 变流器信息,
    "双向变流器": 双向变流器信息,
    "传输线": 传输线信息,
}  # type: ignore


from networkx import Graph

# partial if typical day mode is on.
def compute(
    devs: List[dict],
    adders: Dict[int, dict],
    graph_data: dict,
    G: Graph,
    mw: ModelWrapper,
):
    PD = {}
    algoParam = 计算参数.parse_obj(graph_data)

    devInstDict = {}

    for dev in devs:
        devSubtype = dev["subtype"]
        devParam = dev["param"]
        devPorts = dev["ports"]

        devID_int = dev["id"]

        devIDClass = devIDClassMap[devSubtype]

        devIDInstInit = {"ID": devID_int}
        for port_name, port_info in devPorts.items():
            port_id = port_info["id"]
            devIDInstInit.update({port_name: port_id})
        devIDInst = devIDClass.parse_obj(devIDInstInit)

        devInfoInstInit = devParam
        devInfoClass = devInfoClassMap[devSubtype]
        devInfoInst = devInfoClass.parse_obj(devInfoInstInit)

        devInstClass = devInstClassMap[devSubtype]
        devInst = devInstClass(PD=PD, mw=mw, 计算参数实例=algoParam, 设备ID=devIDInst, 设备信息=devInfoInst)  # type: ignore

        devInstDict.update({devID_int: devInst})
    for adder_index, adder in adders.items():
        input_indexs, output_indexs, io_indexs = (
            adder["input"],
            adder["output"],
            adder["IO"],
        )

        # add them all.
        for j in range(algoParam.迭代步数):
            seqsum = reduce(
                sequence=[PD[i][j] for i in input_indexs + output_indexs + io_indexs],
                function=lambda x, y: x + y,
            )

            mw.Constraint(seqsum >= 0)

        if algoParam.计算类型 == "设计规划":
            input_anchor_0 = G.nodes[input_indexs[0]]
            if input_anchor_0["subtype"] == "变压器输出":
                assert io_indexs == []

                input_limit_list = []
                for input_id in input_indexs:
                    input_anchor = G.nodes[input_id]
                    input_node_id = input_anchor["device_id"]
                    input_devInst = devInstDict[input_node_id]
                    input_limit_list.append(input_devInst.最大允许的负载总功率)
                input_limit = reduce(
                    sequence=input_limit_list, function=lambda x, y: x + y
                )

                output_limit_list = []
                for output_id in input_indexs:
                    output_anchor = G.nodes[output_id]
                    output_node_id = output_anchor["device_id"]
                    output_devInst = devInstDict[output_node_id]
                    output_limit_list.append(output_devInst.MaxEnergyConsumption)
                output_limit = reduce(
                    sequence=output_limit_list, function=lambda x, y: x + y
                )

                mw.Constraint(input_limit + output_limit >= 0)

    financial_obj_expr = reduce(
        sequence=[e.constraints_register() for e in devInstDict.values()],
        function=lambda x, y: x + y,
    )

    environment_obj_expr = ...

    obj_expr = financial_obj_expr

    return obj_expr, devInstDict, PD
    # always minimize the objective.
