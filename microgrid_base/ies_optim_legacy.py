from log_utils import logger_print
from pyomo_environ import *
from typing import cast, Optional
from config import *
from pydantic import ValidationError
import cmath
from copy import deepcopy
import copy
from error_utils import ErrorManager

# input: negative
# output: positive
# IO: Real
import numpy as np
import math


# TODO: use StrEnum (3rd party library) to replace literals in data validation and control flows.
# TODO: implement unit conversion of device info in another file with separate datamodels (another template) instead of explicit conversion in this template (create that first (skeleton) to suppress type check error)
# ref: https://pypi.org/project/StrEnum/


def getattr_with_ellipsis_fallback(obj, attrName, default=cmath.nan):
    val = getattr(obj, attrName, default)
    if val is ...:
        val = default
    return val


import os

# TODO: 典型日 最终输出结果需要展开为8760
# TODO: add more "bounds" to variables
# TODO: call external processor/parser to handle DSL, simplify expressions.
from typing import Dict, List, Tuple, Union, Callable
from pydantic import conlist, conint, confloat, constr
from constants import *
import pyomo.core.base
import parse
from export_format_units import *

try:
    from typing import Literal
except:
    from typing_extensions import Literal


import rich
from pydantic import BaseModel, Field, validator

# the main code for computing.
# currently just compute microgrid
# three computation modes:


from unit_utils import (
    unitFactorCalculator,
    ureg,
    standard_units,
    getSingleUnitConverted,
    multiplyWithUnit,
)


### 计价模型 ###
import math

# 函数参数: (power, time_in_day)
# 阶梯电价: 容量下限从0开始

# TODO: 每个月的都不同 #


def 计算年化率(_贴现率, 寿命):
    # 默认贴现率单位为%
    if _贴现率 <= 0 or 寿命 <= 0:
        年化率 = 0  # 仿真模拟的时候 用于去除和年化率有关的目标
    else:
        贴现率 = _贴现率 / 100
        年化率_CT = (1 + 贴现率) ** 寿命

        年化率 = (贴现率 * 年化率_CT) / (年化率_CT - 1)
    return 年化率


from functools import lru_cache


class 价格转换:
    @staticmethod
    @lru_cache(maxsize=1)
    def getMagnitude():
        magnitude, _ = unitFactorCalculator(ureg, standard_units, "元/kWh")
        return magnitude

    @staticmethod
    def convert(value):
        # convert to standard unit
        magnitude = 价格转换.getMagnitude()
        ret = value * magnitude
        return ret


class 常数电价(BaseModel, 价格转换):
    Price: confloat(gt=0) = Field(title="电价", description="元/kWh")

    def getFee(self, power: float, time_in_day: float) -> float:
        price = self.Price

        # unit: [currency]/[time]
        # 万元/h
        return self.convert(price * power)


class 常数氢价(BaseModel, 价格转换):
    Price: confloat(gt=0) = Field(title="氢价", description="元/kg")

    def getFee(self, power: float, time_in_day: float) -> float:
        price = self.Price

        # unit: [currency]/[time]
        # 万元/h
        return self.convert(price * power)


month_days = [31] * 每年月数
month_days[1] = 28
month_days[4 - 1] = month_days[6 - 1] = month_days[9 - 1] = month_days[11 - 1] = 30
assert sum(month_days) == 每年天数


def convertMonthToDays(month_index: int):
    assert month_index in range(12)
    ret = sum(month_days[:month_index])
    return ret


def convertDaysToMonth(day_index: float):
    acc_days = 0
    for month_cursor, days_in_month in enumerate(month_days):
        acc_days += days_in_month
        if acc_days >= day_index:
            return month_cursor
    raise Exception("Invalid day index:", day_index)


class 分月电价(BaseModel, 价格转换):
    PriceList: Tuple[
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
    ] = Field(title=f"长度为{每年月数}的价格数组", description="单位: 元/kWh")

    def getFee(self, power: float, time_in_day: float) -> float:
        current_day_index = time_in_day // 每天小时数
        month_index = convertDaysToMonth(current_day_index)

        price = self.PriceList[month_index]

        # unit: [currency]/[time]
        # 万元/h
        return self.convert(price * power)


class 分时电价(BaseModel, 价格转换):
    PriceList: Tuple[
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
    ] = Field(title=f"长度为{每天小时数}的价格数组", description="单位: 元/kWh")

    def getFee(self, power: float, time_in_day: float) -> float:
        current_time = math.floor(time_in_day % 每天小时数)

        price = self.PriceList[current_time]

        # unit: [currency]/[time]
        # 万元/h
        return self.convert(price * power)


class 分时分月电价(BaseModel, 价格转换):
    PriceStruct: Tuple[
        分时电价, 分时电价, 分时电价, 分时电价, 分时电价, 分时电价, 分时电价, 分时电价, 分时电价, 分时电价, 分时电价, 分时电价
    ] = Field(title=f"长度为{每年月数}的分时电价数组", description="单位: 元/kWh")

    def getFee(self, power: float, time_in_day: float) -> float:
        current_day_index = time_in_day // 每天小时数
        month_index = convertDaysToMonth(current_day_index)

        _分时电价 = self.PriceStruct[month_index]
        ret = _分时电价.getFee(power, time_in_day)
        return ret


class 计价阶梯(常数电价):
    LowerLimit: confloat(ge=0) = Field(title="功率下限")


class 阶梯电价(BaseModel):
    PriceStruct: conlist(计价阶梯, min_items=1) = Field(
        title="长度不定的计价阶梯列表", description="单位: 元/kWh"
    )

    @validator("PriceStruct")
    def checkPriceStruct(cls, v: List[计价阶梯]):
        v.sort(key=lambda x: x.LowerLimit)
        assert v[0].LowerLimit == 0
        return v

    def getFee(self, power: float, time_in_day: float) -> float:
        for index, elem in enumerate(self.PriceStruct):
            if elem.LowerLimit <= power:
                if (
                    index + 1 == len(self.PriceStruct)
                    or self.PriceStruct[index + 1].LowerLimit >= power
                ):
                    return elem.getFee(power, time_in_day)
        logger_print(self)
        raise Exception("Unable to get electricity price with power:", power)


class 分时阶梯电价(BaseModel):
    PriceStructList: Tuple[
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
        阶梯电价,
    ] = Field(title=f"长度为{每天小时数}的阶梯电价数组", description="单位: 元/kWh")

    def getFee(self, power: float, time_in_day: float) -> float:
        current_time = math.floor(time_in_day % 每天小时数)
        mPriceStruct = self.PriceStructList[current_time]
        result = mPriceStruct.getFee(power, time_in_day)
        return result


# 8760 hours of data
# several days of data to compute a year

# 7200 seconds. simulation

# device parameters would be the same.

# load and environment might change.

# so for every device the will change.

# iterate through all device-port pairs, then retrieve attributes from another dict.

# string, digits, tables.
# you can dump and load from json.


def quicksum_indexed_var(indexed_var):
    if isinstance(indexed_var, list):
        return sum(indexed_var)
    return sum(indexed_var.values())


#############
# Device ID #
#############
from pydantic import validator


class 设备ID(BaseModel):
    ID: conint(ge=0) = Field(title="设备ID", description="从拓扑图节点ID获取")


class 柴油ID(设备ID):
    燃料接口: conint(ge=0) = Field(title="燃料接口ID", description="接口类型: 输出")
    """
    类型: 输出
    """


class 电负荷ID(设备ID):
    电接口: conint(ge=0) = Field(title="电接口ID", description="接口类型: 输入")
    """
    类型: 输入
    """


class 光伏发电ID(设备ID):
    电接口: conint(ge=0) = Field(title="电接口ID", description="接口类型: 输出")
    """
    类型: 输出
    """


class 风力发电ID(设备ID):
    电接口: conint(ge=0) = Field(title="电接口ID", description="接口类型: 输出")
    """
    类型: 输出
    """


class 柴油发电ID(设备ID):
    电接口: conint(ge=0) = Field(title="电接口ID", description="接口类型: 输出")
    """
    类型: 输出
    """
    燃料接口: conint(ge=0) = Field(title="燃料接口ID", description="接口类型: 输入")
    """
    类型: 输入
    """


class 锂电池ID(设备ID):
    电接口: conint(ge=0) = Field(title="电接口ID", description="接口类型: 输入输出")
    """
    类型: 输入输出
    """


class 变压器ID(设备ID):
    电输入: conint(ge=0) = Field(title="电输入ID", description="接口类型: 输入")
    """
    类型: 输入
    """
    电输出: conint(ge=0) = Field(title="电输出ID", description="接口类型: 输出")
    """
    类型: 输出
    """


class 变流器ID(设备ID):
    电输入: conint(ge=0) = Field(title="电输入ID", description="接口类型: 输入")
    """
    类型: 输入
    """
    电输出: conint(ge=0) = Field(title="电输出ID", description="接口类型: 输出")
    """
    类型: 输出
    """


class 双向变流器ID(设备ID):
    线路端: conint(ge=0) = Field(title="线路端ID", description="接口类型: 输入输出")
    """
    类型: 输入输出
    """
    储能端: conint(ge=0) = Field(title="储能端ID", description="接口类型: 输入输出")
    """
    类型: 输入输出
    """


class 传输线ID(设备ID):
    电输出: conint(ge=0) = Field(title="电输出ID", description="接口类型: 输入输出")
    """
    类型: 输入输出
    """
    电输入: conint(ge=0) = Field(title="电输入ID", description="接口类型: 输入输出")
    """
    类型: 输入输出
    """


class 氢负荷ID(设备ID):
    氢气接口: conint(ge=0) = Field(title="氢气接口ID", description="接口类型: 输入")
    """
    类型: 输入
    """


class 电解槽ID(设备ID):
    设备余热接口: conint(ge=0) = Field(title="设备余热接口ID", description="接口类型: 输出")
    """
    类型: 输出
    """
    制氢接口: conint(ge=0) = Field(title="制氢接口ID", description="接口类型: 输出")
    """
    类型: 输出
    """
    电接口: conint(ge=0) = Field(title="电接口ID", description="接口类型: 输入")
    """
    类型: 输入
    """


###############
# Device Info #
###############


class 设备基础信息(BaseModel):
    设备名称: constr(min_length=1) = Field(title="设备名称")

    def toStandard(self, attr: str):
        className = self.__class__.__name__

        with ErrorManager(
            default_error=f"Instance data:\n{self.dict()}\nError converting attribute '{attr}' of class '{className}'"
        ):
            schema = self.schema()
            props = schema["properties"]

            attr_alias_dict = {k: v.get("title", None) for k, v in props.items()}
            attrName = attr if attr in props.keys() else attr_alias_dict[attr]
            assert (
                attrName
            ), f"Cannot find attribute name in class '{className}' with query '{attr}'"
            val = copy.deepcopy(getattr(self, attrName))
            if val is None:
                logger_print(
                    "Warning: Attribute '{attr}' of class '{className}' is None. Using zero instead."
                )
                return 0

            desc = props[attr]["description"]
            val_units = desc.replace("：", ":").split(":")[-1].strip()

            units = []
            for i, unit in enumerate(val_units.replace("，", ",").split(",")):
                u = unit.strip()
                if u:
                    units.append(u)

            varNames = attrName.replace("-", "_").split("_")
            assert len(varNames) == len(
                units
            ), f"units length ({units}) does not match varname length ({varNames}).\nfailed to parse unit for: {className}.{attrName}"

            assert (
                len(units) > 0
            ), f"{className}.{attrName} does not have unit definition"

            crlist = []

            for val_unit in units:
                ConversionRate, StandardUnit = unitFactorCalculator(
                    ureg, standard_units, val_unit
                )
                logger_print(
                    f"Converting param {varNames[i]} at {className}.{attrName}: {val_unit} -> {StandardUnit} (magnitude: {ConversionRate})"
                )
                crlist.append(ConversionRate)

            len_varNames = len(varNames)

            if not hasattr(val, "__iter__"):
                assert (
                    len_varNames == 1
                ), f"input value {val} failed to match shape of class {className}.{attrName} (len: {len_varNames})"
                ret_val = val * crlist[0]
            elif not hasattr(val[0], "__iter__"):
                assert (
                    len_varNames == 1
                ), f"input value {val} failed to match shape of class {className}.{attrName} (len: {len_varNames})"
                ret_val = [v * crlist[0] for v in val]
            else:
                # verify shape here.
                ret_val = []
                for it in val:
                    assert (
                        len(it) == len_varNames
                    ), f"input value {it} failed to match shape of class {className}.{attrName} (len: {len_varNames})"
                    ret_val.append([it[i] * crlist[i] for i in range(len_varNames)])
            return ret_val


class 设备信息(设备基础信息):
    生产厂商: constr(min_length=1) = Field(title="生产厂商")

    设备型号: constr(min_length=1) = Field(title="设备型号")


from enum import auto
import sys
from strenum import StrEnum


class 风力发电类型(StrEnum):
    变桨 = auto()
    定桨 = auto()
    标幺值 = auto()


class 油耗规划算法(StrEnum):
    平均 = auto()
    最佳 = auto()


class 新能源消纳约束(StrEnum):
    无 = auto()
    惩罚代价 = auto()
    限制消纳率 = auto()


class 负荷类型(StrEnum):
    Normal = auto()
    Punished = auto()
    Flexible = auto()
    Interruptable = auto()
    InterruptableAndFlexible = auto()


class Direction(StrEnum):
    Directed = auto()
    Bidirectional = auto()


class 柴油信息(设备基础信息):
    Price: Tuple[confloat(gt=0), constr(min_length=1)] = Field(
        title="Price", description="格式: [数值,单位]"
    )
    """
    格式: [数值,单位]
    """
    热值: Tuple[confloat(gt=0), constr(min_length=1)] = Field(
        title="热值", description="格式: [数值,单位]"
    )
    """
    格式: [数值,单位]
    """
    CO2: Tuple[confloat(gt=0), constr(min_length=1)] = Field(
        title="CO2", description="格式: [数值,单位]"
    )
    """
    格式: [数值,单位]
    """
    NOX: Tuple[confloat(gt=0), constr(min_length=1)] = Field(
        title="NOX", description="格式: [数值,单位]"
    )
    """
    格式: [数值,单位]
    """
    SO2: Tuple[confloat(gt=0), constr(min_length=1)] = Field(
        title="SO2", description="格式: [数值,单位]"
    )
    """
    格式: [数值,单位]
    """

    class DefaultUnits:
        Price = "万元/L"
        热值 = "kWh/L"
        CO2 = "kg/L"
        NOX = "kg/L"
        SO2 = "kg/L"


class 电负荷信息(设备基础信息):
    LoadType: 负荷类型 = Field(
        default=负荷类型.Normal,
        title="负荷类型",
        description=f"可选: {', '.join(负荷类型.__members__.keys())}",
    )

    # 正数
    PunishmentRate: confloat(ge=0) = Field(
        default=0, title="惩罚系数", description="单位: 元/kWh"
    )
    """
    单位: 元/kWh
    """

    Pmin: confloat(ge=0) = Field(default=0, title="负荷功率最小值", description="单位: kW")
    """
    单位: kW
    """

    Pmax: confloat(ge=0) = Field(default=0, title="负荷功率最大值", description="单位: kW")
    """
    单位: kW
    """

    @validator("Pmax")
    def validate_Pmax(cls, v, values):
        if values.get("LoadType", None) in [
            负荷类型.Flexible,
            负荷类型.InterruptableAndFlexible,
        ]:
            p_min = values.get("Pmin", 0)
            assert (
                v >= p_min
            ), f"Pmax must be greater than or equal to Pmin\nGiven: Pmax={v}, Pmin={p_min}"
        return v

    EnergyConsumption: List[confloat(ge=0)] = Field(title="耗能功率表", description="单位: kW")
    """
    单位: kW
    """
    MaxEnergyConsumption: Union[None, confloat(gt=0)] = Field(
        default=None, title="最大消耗功率", description="单位: kW"
    )
    """
    单位: kW
    """

    PriceModel: Union[常数电价, 阶梯电价, 分时电价, 分时阶梯电价, 分月电价, 分时分月电价] = Field(
        title="计价模型", description="单位: 元/kWh"
    )


class 光伏发电信息(设备信息):
    RenewableEnergyConsumptionConstraint: 新能源消纳约束 = Field(
        default=新能源消纳约束.无, title="新能源消纳约束", description="无、惩罚代价、限制消纳率"
    )
    RenewableEnergyConsumptionPunishmentRate: confloat(ge=0) = Field(
        default=0, title="新能源消纳约束惩罚代价", description="单位: 元/kWh"
    )
    """
    单位: 元/kWh
    """
    RenewableEnergyConsumptionRate: confloat(ge=0, le=100) = Field(
        default=0, title="新能源消纳率", description="单位: percent"
    )
    """
    单位: percent
    """

    @validator("RenewableEnergyConsumptionPunishmentRate")
    def validate_RenewableEnergyConsumptionPunishmentRate(cls, v, values):
        if (
            values.get("RenewableEnergyConsumptionConstraint", 新能源消纳约束.无)
            == 新能源消纳约束.惩罚代价
        ):
            assert v > 0, f"不合理的惩罚代价：{v}"
        return v

    Area: confloat(ge=0) = Field(title="光伏板面积", description="名称: 光伏板面积\n单位: m2")
    """
    名称: 光伏板面积
    单位: m2
    """

    PowerConversionEfficiency: confloat(ge=0) = Field(
        title="电电转换效率", description="名称: 电电转换效率\n单位: percent"
    )
    """
    名称: 电电转换效率
    单位: percent
    """

    @validator("PowerConversionEfficiency")
    def validate_PowerConversionEfficiency_for_percent_warning(cls, value):
        warning_msg = None
        field_name = "PowerConversionEfficiency"
        if value <= ies_env.PERCENT_WARNING_THRESHOLD:
            warning_msg = f"Field '{field_name}' (value: {value}; unit: percent) passed to class '{cls.__name__}' is less than or equal to {ies_env.PERCENT_WARNING_THRESHOLD}"
        if warning_msg is not None:
            if ies_env.UNIT_WARNING_AS_ERROR:
                raise Exception(warning_msg)
            else:
                logger_print(warning_msg)
        return value

    MaxPower: confloat(ge=0) = Field(title="最大发电功率", description="名称: 最大发电功率\n单位: kWp")
    """
    名称: 最大发电功率
    单位: kWp
    """

    PowerDeltaLimit: confloat(ge=0) = Field(
        title="发电爬坡率", description="名称: 发电爬坡率\n单位: percent/s"
    )
    """
    名称: 发电爬坡率
    单位: percent/s
    """

    CostPerKilowatt: confloat(ge=0) = Field(
        title="采购成本", description="名称: 采购成本\n单位: 万元/kWp"
    )
    """
    名称: 采购成本
    单位: 万元/kWp
    """

    CostPerYearPerKilowatt: confloat(ge=0) = Field(
        title="固定维护成本", description="名称: 固定维护成本\n单位: 万元/(kWp*年)"
    )
    """
    名称: 固定维护成本
    单位: 万元/(kWp*年)
    """

    VariationalCostPerWork: confloat(ge=0) = Field(
        title="可变维护成本", description="名称: 可变维护成本\n单位: 元/kWh"
    )
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: confloat(ge=0) = Field(title="设计寿命", description="名称: 设计寿命\n单位: 年")
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerKilowatt: confloat(ge=0) = Field(
        title="建设费用系数", description="名称: 建设费用系数\n单位: 万元/kWp"
    )
    """
    名称: 建设费用系数
    单位: 万元/kWp
    """

    BuildBaseCost: confloat(ge=0) = Field(
        title="建设费用基数", description="名称: 建设费用基数\n单位: 万元"
    )
    """
    名称: 建设费用基数
    单位: 万元
    """

    MaxInstallArea: confloat(ge=0) = Field(
        title="最大安装面积", description="名称: 最大安装面积\n单位: m2"
    )
    """
    名称: 最大安装面积
    单位: m2
    """

    MinInstallArea: confloat(ge=0) = Field(
        title="最小安装面积", description="名称: 最小安装面积\n单位: m2"
    )
    """
    名称: 最小安装面积
    单位: m2
    """

    DeviceCount: confloat(ge=0) = Field(title="安装台数", description="名称: 安装台数\n单位: 台")
    """
    名称: 安装台数
    单位: 台
    """


class 风力发电信息(设备信息):
    RenewableEnergyConsumptionConstraint: 新能源消纳约束 = Field(
        default=新能源消纳约束.无, title="新能源消纳约束", description="无、惩罚代价、限制消纳率"
    )
    RenewableEnergyConsumptionPunishmentRate: confloat(ge=0) = Field(
        default=0, title="新能源消纳约束惩罚代价", description="单位: 元/kWh"
    )
    """
    单位: 元/kWh
    """
    RenewableEnergyConsumptionRate: confloat(ge=0, le=100) = Field(
        default=0, title="新能源消纳率", description="单位: percent"
    )
    """
    单位: percent
    """

    @validator("RenewableEnergyConsumptionPunishmentRate")
    def validate_RenewableEnergyConsumptionPunishmentRate(cls, v, values):
        if (
            values.get("RenewableEnergyConsumptionConstraint", 新能源消纳约束.无)
            == 新能源消纳约束.惩罚代价
        ):
            assert v > 0, f"不合理的惩罚代价：{v}"
        return v

    machineType: 风力发电类型 = Field(
        default=风力发电类型.变桨, title="选择风力发电类型", description="定桨、变桨（默认）、标幺值"
    )
    normalizedPower: Union[None, List[float]] = Field(
        default=None,
        title="风力发电标幺值",
        description="空或数组(典型日长度为24,全年逐时长度为8760,秒级长度为7200)",
    )

    CutoutPower: confloat(ge=0) = Field(title="切出功率", description="名称: 切出功率\n单位: kWp")
    """
    名称: 切出功率
    单位: kWp
    """

    RatedPower: confloat(ge=0) = Field(title="额定功率", description="名称: 额定功率\n单位: kWp")
    """
    名称: 额定功率
    单位: kWp
    """

    RatedWindSpeed: confloat(ge=0) = Field(
        title="额定风速", description="名称: 额定风速\n单位: m/s"
    )
    """
    名称: 额定风速
    单位: m/s
    """

    MinWindSpeed: confloat(ge=0) = Field(title="切入风速", description="名称: 切入风速\n单位: m/s")
    """
    名称: 切入风速
    单位: m/s
    """

    MaxWindSpeed: confloat(ge=0) = Field(title="切出风速", description="名称: 切出风速\n单位: m/s")
    """
    名称: 切出风速
    单位: m/s
    """

    PowerDeltaLimit: confloat(ge=0) = Field(
        title="发电爬坡率", description="名称: 发电爬坡率\n单位: percent/s"
    )
    """
    名称: 发电爬坡率
    单位: percent/s
    """

    CostPerKilowatt: confloat(ge=0) = Field(
        title="采购成本", description="名称: 采购成本\n单位: 万元/kWp"
    )
    """
    名称: 采购成本
    单位: 万元/kWp
    """

    CostPerYearPerKilowatt: confloat(ge=0) = Field(
        title="固定维护成本", description="名称: 固定维护成本\n单位: 万元/(kWp*年)"
    )
    """
    名称: 固定维护成本
    单位: 万元/(kWp*年)
    """

    VariationalCostPerWork: confloat(ge=0) = Field(
        title="可变维护成本", description="名称: 可变维护成本\n单位: 元/kWh"
    )
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: confloat(ge=0) = Field(title="设计寿命", description="名称: 设计寿命\n单位: 年")
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerKilowatt: confloat(ge=0) = Field(
        title="建设费用系数", description="名称: 建设费用系数\n单位: 万元/kWp"
    )
    """
    名称: 建设费用系数
    单位: 万元/kWp
    """

    BuildBaseCost: confloat(ge=0) = Field(
        title="建设费用基数", description="名称: 建设费用基数\n单位: 万元"
    )
    """
    名称: 建设费用基数
    单位: 万元
    """

    MaxDeviceCount: confloat(ge=0) = Field(
        title="最大安装台数", description="名称: 最大安装台数\n单位: 台"
    )
    """
    名称: 最大安装台数
    单位: 台
    """

    MinDeviceCount: confloat(ge=0) = Field(
        title="最小安装台数", description="名称: 最小安装台数\n单位: 台"
    )
    """
    名称: 最小安装台数
    单位: 台
    """

    DeviceCount: confloat(ge=0) = Field(title="安装台数", description="名称: 安装台数\n单位: 台")
    """
    名称: 安装台数
    单位: 台
    """

    @validator("RatedPower")
    def checkRatedPower(cls, v, values):
        CutoutPower = values.get("CutoutPower", None)
        if CutoutPower is None:
            # instead of Exception, which will make pydantic panic!
            raise ValidationError("风力发电没有传入切出功率")
        else:
            assert CutoutPower <= v, f"切出功率({CutoutPower})必须小于额定功率({v})"
        return v


class 柴油发电信息(设备信息):
    unitAnnualOperatingTimeConstraint: bool = Field(
        default=False, title="机组年运行时间约束", description="若选否，变量约束不创建，变量为自由变量，降低计算量"
    )
    maximumAnnualOperatingTimeLimitOfTheUnit: conint(ge=0) = Field(
        default=0, title="机组年运行时间最高限值", description="单位：小时"
    )
    considerUnitStartUpCosts: bool = Field(
        default=False, title="考虑机组启动费用", description="若选否，变量约束不创建，变量为自由变量，降低计算量"
    )
    unitSingleStartupCost: conint(ge=0) = Field(
        default=0, title="机组单次启动费用", description="单位：元/次"
    )
    unitPlanningAlgorithmSelection: 油耗规划算法 = Field(
        default=油耗规划算法.平均, title="机组规划算法选择", description="平均/最佳"
    )
    averageLoadRate: confloat(ge=0, le=100) = Field(
        default=0, title="平均负载率", description="单位：percent"
    )

    RatedPower: confloat(ge=0) = Field(title="额定功率", description="名称: 额定功率\n单位: kW")
    """
    名称: 额定功率
    单位: kW
    """

    PowerDeltaLimit: confloat(ge=0) = Field(
        title="发电爬坡率", description="名称: 发电爬坡率\n单位: percent/s"
    )
    """
    名称: 发电爬坡率
    单位: percent/s
    """

    PowerStartupLimit: confloat(ge=0) = Field(
        title="启动功率百分比", description="名称: 启动功率百分比\n单位: percent"
    )
    """
    名称: 启动功率百分比
    单位: percent
    """

    @validator("PowerStartupLimit")
    def validate_PowerStartupLimit_for_percent_warning(cls, value):
        warning_msg = None
        field_name = "PowerStartupLimit"
        if value <= ies_env.PERCENT_WARNING_THRESHOLD:
            warning_msg = f"Field '{field_name}' (value: {value}; unit: percent) passed to class '{cls.__name__}' is less than or equal to {ies_env.PERCENT_WARNING_THRESHOLD}"
        if warning_msg is not None:
            if ies_env.UNIT_WARNING_AS_ERROR:
                raise Exception(warning_msg)
            else:
                logger_print(warning_msg)
        return value

    CostPerMachine: confloat(ge=0) = Field(
        title="采购成本", description="名称: 采购成本\n单位: 万元/台"
    )
    """
    名称: 采购成本
    单位: 万元/台
    """

    CostPerYearPerMachine: confloat(ge=0) = Field(
        title="固定维护成本", description="名称: 固定维护成本\n单位: 万元/(台*年)"
    )
    """
    名称: 固定维护成本
    单位: 万元/(台*年)
    """

    VariationalCostPerWork: confloat(ge=0) = Field(
        title="可变维护成本", description="名称: 可变维护成本\n单位: 元/kWh"
    )
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: confloat(ge=0) = Field(title="设计寿命", description="名称: 设计寿命\n单位: 年")
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerMachine: confloat(ge=0) = Field(
        title="建设费用系数", description="名称: 建设费用系数\n单位: 万元/台"
    )
    """
    名称: 建设费用系数
    单位: 万元/台
    """

    BuildBaseCost: confloat(ge=0) = Field(
        title="建设费用基数", description="名称: 建设费用基数\n单位: 万元"
    )
    """
    名称: 建设费用基数
    单位: 万元
    """

    MaxDeviceCount: confloat(ge=0) = Field(
        title="最大安装台数", description="名称: 最大安装台数\n单位: 台"
    )
    """
    名称: 最大安装台数
    单位: 台
    """

    MinDeviceCount: confloat(ge=0) = Field(
        title="最小安装台数", description="名称: 最小安装台数\n单位: 台"
    )
    """
    名称: 最小安装台数
    单位: 台
    """

    DeviceCount: confloat(ge=0) = Field(title="安装台数", description="名称: 安装台数\n单位: 台")
    """
    名称: 安装台数
    单位: 台
    """

    DieselToPower_Load: List[Tuple[confloat(gt=0), confloat(ge=0)]] = Field(
        title="燃油消耗率_负载率",
        description="DieselToPower: 燃油消耗率\n单位: L/kWh\nLoad: 负载率\n单位: percent",
    )
    """
    DieselToPower: 燃油消耗率
    单位: L/kWh

    Load: 负载率
    单位: percent
    """


class 锂电池信息(设备信息):
    循环边界条件: constr(min_length=1) = Field(title="循环边界条件")

    RatedCapacity: confloat(ge=0) = Field(title="额定容量", description="名称: 额定容量\n单位: kWh")
    """
    名称: 额定容量
    单位: kWh
    """

    BatteryDeltaLimit: confloat(ge=0) = Field(
        title="电池充放电倍率", description="名称: 电池充放电倍率\n单位: 1/hour"
    )
    """
    名称: 电池充放电倍率
    单位: 1/hour
    """

    ChargeEfficiency: confloat(ge=0) = Field(
        title="充能效率", description="名称: 充能效率\n单位: percent"
    )
    """
    名称: 充能效率
    单位: percent
    """

    @validator("ChargeEfficiency")
    def validate_ChargeEfficiency_for_percent_warning(cls, value):
        warning_msg = None
        field_name = "ChargeEfficiency"
        if value <= ies_env.PERCENT_WARNING_THRESHOLD:
            warning_msg = f"Field '{field_name}' (value: {value}; unit: percent) passed to class '{cls.__name__}' is less than or equal to {ies_env.PERCENT_WARNING_THRESHOLD}"
        if warning_msg is not None:
            if ies_env.UNIT_WARNING_AS_ERROR:
                raise Exception(warning_msg)
            else:
                logger_print(warning_msg)
        return value

    DischargeEfficiency: confloat(ge=0) = Field(
        title="放能效率", description="名称: 放能效率\n单位: percent"
    )
    """
    名称: 放能效率
    单位: percent
    """

    @validator("DischargeEfficiency")
    def validate_DischargeEfficiency_for_percent_warning(cls, value):
        warning_msg = None
        field_name = "DischargeEfficiency"
        if value <= ies_env.PERCENT_WARNING_THRESHOLD:
            warning_msg = f"Field '{field_name}' (value: {value}; unit: percent) passed to class '{cls.__name__}' is less than or equal to {ies_env.PERCENT_WARNING_THRESHOLD}"
        if warning_msg is not None:
            if ies_env.UNIT_WARNING_AS_ERROR:
                raise Exception(warning_msg)
            else:
                logger_print(warning_msg)
        return value

    MaxSOC: confloat(ge=0) = Field(title="最大SOC", description="名称: 最大SOC\n单位: percent")
    """
    名称: 最大SOC
    单位: percent
    """

    @validator("MaxSOC")
    def validate_MaxSOC_for_percent_warning(cls, value):
        warning_msg = None
        field_name = "MaxSOC"
        if value <= ies_env.PERCENT_WARNING_THRESHOLD:
            warning_msg = f"Field '{field_name}' (value: {value}; unit: percent) passed to class '{cls.__name__}' is less than or equal to {ies_env.PERCENT_WARNING_THRESHOLD}"
        if warning_msg is not None:
            if ies_env.UNIT_WARNING_AS_ERROR:
                raise Exception(warning_msg)
            else:
                logger_print(warning_msg)
        return value

    MinSOC: confloat(ge=0) = Field(title="最小SOC", description="名称: 最小SOC\n单位: percent")
    """
    名称: 最小SOC
    单位: percent
    """

    @validator("MinSOC")
    def validate_MinSOC_for_percent_warning(cls, value):
        warning_msg = None
        field_name = "MinSOC"
        if value <= ies_env.PERCENT_WARNING_THRESHOLD:
            warning_msg = f"Field '{field_name}' (value: {value}; unit: percent) passed to class '{cls.__name__}' is less than or equal to {ies_env.PERCENT_WARNING_THRESHOLD}"
        if warning_msg is not None:
            if ies_env.UNIT_WARNING_AS_ERROR:
                raise Exception(warning_msg)
            else:
                logger_print(warning_msg)
        return value

    BatteryStorageDecay: confloat(ge=0) = Field(
        title="存储衰减", description="名称: 存储衰减\n单位: percent/hour"
    )
    """
    名称: 存储衰减
    单位: percent/hour
    """

    LifetimeCycleCount: confloat(ge=0) = Field(
        title="等效完全循环次数", description="名称: 等效完全循环次数\n单位: 次"
    )
    """
    名称: 等效完全循环次数
    单位: 次
    """

    BatteryLife: confloat(ge=0) = Field(title="电池换芯周期", description="名称: 电池换芯周期\n单位: 年")
    """
    名称: 电池换芯周期
    单位: 年
    """

    CostPerCapacity: confloat(ge=0) = Field(
        title="采购成本", description="名称: 采购成本\n单位: 万元/kWh"
    )
    """
    名称: 采购成本
    单位: 万元/kWh
    """

    CostPerYearPerCapacity: confloat(ge=0) = Field(
        title="固定维护成本", description="名称: 固定维护成本\n单位: 万元/(kWh*年)"
    )
    """
    名称: 固定维护成本
    单位: 万元/(kWh*年)
    """

    VariationalCostPerWork: confloat(ge=0) = Field(
        title="可变维护成本", description="名称: 可变维护成本\n单位: 元/kWh"
    )
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: confloat(ge=0) = Field(title="设计寿命", description="名称: 设计寿命\n单位: 年")
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerCapacity: confloat(ge=0) = Field(
        title="建设费用系数", description="名称: 建设费用系数\n单位: 万元/kWh"
    )
    """
    名称: 建设费用系数
    单位: 万元/kWh
    """

    BuildBaseCost: confloat(ge=0) = Field(
        title="建设费用基数", description="名称: 建设费用基数\n单位: 万元"
    )
    """
    名称: 建设费用基数
    单位: 万元
    """

    InitSOC: confloat(ge=0) = Field(title="初始SOC", description="名称: 初始SOC\n单位: percent")
    """
    名称: 初始SOC
    单位: percent
    """

    @validator("InitSOC")
    def validate_InitSOC_for_percent_warning(cls, value):
        warning_msg = None
        field_name = "InitSOC"
        if value <= ies_env.PERCENT_WARNING_THRESHOLD:
            warning_msg = f"Field '{field_name}' (value: {value}; unit: percent) passed to class '{cls.__name__}' is less than or equal to {ies_env.PERCENT_WARNING_THRESHOLD}"
        if warning_msg is not None:
            if ies_env.UNIT_WARNING_AS_ERROR:
                raise Exception(warning_msg)
            else:
                logger_print(warning_msg)
        return value

    MaxTotalCapacity: confloat(ge=0) = Field(
        title="最大设备容量", description="名称: 最大设备容量\n单位: kWh"
    )
    """
    名称: 最大设备容量
    单位: kWh
    """

    MinTotalCapacity: confloat(ge=0) = Field(
        title="最小设备容量", description="名称: 最小设备容量\n单位: kWh"
    )
    """
    名称: 最小设备容量
    单位: kWh
    """

    TotalCapacity: confloat(ge=0) = Field(title="设备容量", description="名称: 设备容量\n单位: kWh")
    """
    名称: 设备容量
    单位: kWh
    """


class 变压器信息(设备信息):
    direction: Direction = Field(
        default=Direction.Directed, title="单双向模式", description="默认为单向"
    )

    Efficiency: confloat(ge=0) = Field(title="效率", description="名称: 效率\n单位: percent")
    """
    名称: 效率
    单位: percent
    """

    @validator("Efficiency")
    def validate_Efficiency_for_percent_warning(cls, value):
        warning_msg = None
        field_name = "Efficiency"
        if value <= ies_env.PERCENT_WARNING_THRESHOLD:
            warning_msg = f"Field '{field_name}' (value: {value}; unit: percent) passed to class '{cls.__name__}' is less than or equal to {ies_env.PERCENT_WARNING_THRESHOLD}"
        if warning_msg is not None:
            if ies_env.UNIT_WARNING_AS_ERROR:
                raise Exception(warning_msg)
            else:
                logger_print(warning_msg)
        return value

    RatedPower: confloat(ge=0) = Field(title="变压器容量", description="名称: 变压器容量\n单位: kW")
    """
    名称: 变压器容量
    单位: kW
    """

    CostPerKilowatt: confloat(ge=0) = Field(
        title="采购成本", description="名称: 采购成本\n单位: 万元/kW"
    )
    """
    名称: 采购成本
    单位: 万元/kW
    """

    CostPerYearPerKilowatt: confloat(ge=0) = Field(
        title="固定维护成本", description="名称: 固定维护成本\n单位: 万元/(kW*年)"
    )
    """
    名称: 固定维护成本
    单位: 万元/(kW*年)
    """

    VariationalCostPerWork: confloat(ge=0) = Field(
        title="可变维护成本", description="名称: 可变维护成本\n单位: 元/kWh"
    )
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: confloat(ge=0) = Field(title="设计寿命", description="名称: 设计寿命\n单位: 年")
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerKilowatt: confloat(ge=0) = Field(
        title="建设费用系数", description="名称: 建设费用系数\n单位: 万元/kW"
    )
    """
    名称: 建设费用系数
    单位: 万元/kW
    """

    BuildBaseCost: confloat(ge=0) = Field(
        title="建设费用基数", description="名称: 建设费用基数\n单位: 万元"
    )
    """
    名称: 建设费用基数
    单位: 万元
    """

    PowerParameter: confloat(ge=0) = Field(
        title="功率因数", description="名称: 功率因数\n单位: one"
    )
    """
    名称: 功率因数
    单位: one
    """

    LoadRedundancyParameter: confloat(ge=0) = Field(
        title="变压器冗余系数", description="名称: 变压器冗余系数\n单位: one"
    )
    """
    名称: 变压器冗余系数
    单位: one
    """

    MaxDeviceCount: confloat(ge=0) = Field(
        title="最大安装台数", description="名称: 最大安装台数\n单位: 台"
    )
    """
    名称: 最大安装台数
    单位: 台
    """

    MinDeviceCount: confloat(ge=0) = Field(
        title="最小安装台数", description="名称: 最小安装台数\n单位: 台"
    )
    """
    名称: 最小安装台数
    单位: 台
    """

    DeviceCount: confloat(ge=0) = Field(title="安装台数", description="名称: 安装台数\n单位: 台")
    """
    名称: 安装台数
    单位: 台
    """


class 变流器信息(设备信息):
    RatedPower: confloat(ge=0) = Field(title="额定功率", description="名称: 额定功率\n单位: kW")
    """
    名称: 额定功率
    单位: kW
    """

    Efficiency: confloat(ge=0) = Field(title="效率", description="名称: 效率\n单位: percent")
    """
    名称: 效率
    单位: percent
    """

    @validator("Efficiency")
    def validate_Efficiency_for_percent_warning(cls, value):
        warning_msg = None
        field_name = "Efficiency"
        if value <= ies_env.PERCENT_WARNING_THRESHOLD:
            warning_msg = f"Field '{field_name}' (value: {value}; unit: percent) passed to class '{cls.__name__}' is less than or equal to {ies_env.PERCENT_WARNING_THRESHOLD}"
        if warning_msg is not None:
            if ies_env.UNIT_WARNING_AS_ERROR:
                raise Exception(warning_msg)
            else:
                logger_print(warning_msg)
        return value

    CostPerKilowatt: confloat(ge=0) = Field(
        title="采购成本", description="名称: 采购成本\n单位: 万元/kW"
    )
    """
    名称: 采购成本
    单位: 万元/kW
    """

    CostPerYearPerKilowatt: confloat(ge=0) = Field(
        title="固定维护成本", description="名称: 固定维护成本\n单位: 万元/(kW*年)"
    )
    """
    名称: 固定维护成本
    单位: 万元/(kW*年)
    """

    VariationalCostPerWork: confloat(ge=0) = Field(
        title="可变维护成本", description="名称: 可变维护成本\n单位: 元/kWh"
    )
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: confloat(ge=0) = Field(title="设计寿命", description="名称: 设计寿命\n单位: 年")
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerKilowatt: confloat(ge=0) = Field(
        title="建设费用系数", description="名称: 建设费用系数\n单位: 万元/kW"
    )
    """
    名称: 建设费用系数
    单位: 万元/kW
    """

    BuildBaseCost: confloat(ge=0) = Field(
        title="建设费用基数", description="名称: 建设费用基数\n单位: 万元"
    )
    """
    名称: 建设费用基数
    单位: 万元
    """

    MaxDeviceCount: confloat(ge=0) = Field(
        title="最大安装台数", description="名称: 最大安装台数\n单位: 台"
    )
    """
    名称: 最大安装台数
    单位: 台
    """

    MinDeviceCount: confloat(ge=0) = Field(
        title="最小安装台数", description="名称: 最小安装台数\n单位: 台"
    )
    """
    名称: 最小安装台数
    单位: 台
    """

    DeviceCount: confloat(ge=0) = Field(title="安装台数", description="名称: 安装台数\n单位: 台")
    """
    名称: 安装台数
    单位: 台
    """


class 双向变流器信息(设备信息):
    RatedPower: confloat(ge=0) = Field(title="额定功率", description="名称: 额定功率\n单位: kW")
    """
    名称: 额定功率
    单位: kW
    """

    Efficiency: confloat(ge=0) = Field(title="效率", description="名称: 效率\n单位: percent")
    """
    名称: 效率
    单位: percent
    """

    @validator("Efficiency")
    def validate_Efficiency_for_percent_warning(cls, value):
        warning_msg = None
        field_name = "Efficiency"
        if value <= ies_env.PERCENT_WARNING_THRESHOLD:
            warning_msg = f"Field '{field_name}' (value: {value}; unit: percent) passed to class '{cls.__name__}' is less than or equal to {ies_env.PERCENT_WARNING_THRESHOLD}"
        if warning_msg is not None:
            if ies_env.UNIT_WARNING_AS_ERROR:
                raise Exception(warning_msg)
            else:
                logger_print(warning_msg)
        return value

    CostPerKilowatt: confloat(ge=0) = Field(
        title="采购成本", description="名称: 采购成本\n单位: 万元/kW"
    )
    """
    名称: 采购成本
    单位: 万元/kW
    """

    CostPerYearPerKilowatt: confloat(ge=0) = Field(
        title="固定维护成本", description="名称: 固定维护成本\n单位: 万元/(kW*年)"
    )
    """
    名称: 固定维护成本
    单位: 万元/(kW*年)
    """

    VariationalCostPerWork: confloat(ge=0) = Field(
        title="可变维护成本", description="名称: 可变维护成本\n单位: 元/kWh"
    )
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: confloat(ge=0) = Field(title="设计寿命", description="名称: 设计寿命\n单位: 年")
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerKilowatt: confloat(ge=0) = Field(
        title="建设费用系数", description="名称: 建设费用系数\n单位: 万元/kW"
    )
    """
    名称: 建设费用系数
    单位: 万元/kW
    """

    BuildBaseCost: confloat(ge=0) = Field(
        title="建设费用基数", description="名称: 建设费用基数\n单位: 万元"
    )
    """
    名称: 建设费用基数
    单位: 万元
    """

    MaxDeviceCount: confloat(ge=0) = Field(
        title="最大安装台数", description="名称: 最大安装台数\n单位: 台"
    )
    """
    名称: 最大安装台数
    单位: 台
    """

    MinDeviceCount: confloat(ge=0) = Field(
        title="最小安装台数", description="名称: 最小安装台数\n单位: 台"
    )
    """
    名称: 最小安装台数
    单位: 台
    """

    DeviceCount: confloat(ge=0) = Field(title="安装台数", description="名称: 安装台数\n单位: 台")
    """
    名称: 安装台数
    单位: 台
    """


class 传输线信息(设备信息):
    Optimize: bool = Field(
        default=False, title="是否优化线径", description="若选是，根据电负荷峰值确定传输电功率; 选否，则输入给定传输电功率值"
    )
    U: confloat(gt=0) = Field(title="传输电压", description="单位: V")
    """
    单位: V
    """
    Rho: confloat(gt=0) = Field(title="传输线电阻率", description="单位: Ω*m")
    """
    单位: Ω*m
    """
    GivenAveragePower: confloat(gt=0) = Field(title="平均功率", description="单位: kW")
    """
    单位: kW
    """
    GivenMaxPower: confloat(gt=0) = Field(title="峰值功率", description="单位: kW")
    """
    单位: kW
    """

    Pwire_Asec_Pr: List[Tuple[confloat(gt=0), confloat(gt=0), confloat(gt=0)]] = Field(
        title="传输电功率上限-截面积-单位长度价格", description="单位：kW，mm2，万元/km"
    )
    """
    Pwire（传输电功率上限）
    单位：kW
    
    Asec（截面积）
    单位：mm2
    
    Pr（单位长度价格）
    单位：万元/km
    """

    PowerTransferDecay: confloat(ge=0) = Field(
        title="能量衰减系数", description="名称: 能量衰减系数\n单位: kW/km"
    )
    """
    名称: 能量衰减系数
    单位: kW/km
    """

    CostPerKilometer: confloat(ge=0) = Field(
        title="采购成本", description="名称: 采购成本\n单位: 万元/km"
    )
    """
    名称: 采购成本
    单位: 万元/km
    """

    CostPerYearPerKilometer: confloat(ge=0) = Field(
        title="维护成本", description="名称: 维护成本\n单位: 万元/(km*年)"
    )
    """
    名称: 维护成本
    单位: 万元/(km*年)
    """

    Life: confloat(ge=0) = Field(title="设计寿命", description="名称: 设计寿命\n单位: 年")
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerKilometer: confloat(ge=0) = Field(
        title="建设费用系数", description="名称: 建设费用系数\n单位: 万元/km"
    )
    """
    名称: 建设费用系数
    单位: 万元/km
    """

    BuildBaseCost: confloat(ge=0) = Field(
        title="建设费用基数", description="名称: 建设费用基数\n单位: 万元"
    )
    """
    名称: 建设费用基数
    单位: 万元
    """

    Length: confloat(ge=0) = Field(title="长度", description="名称: 长度\n单位: km")
    """
    名称: 长度
    单位: km
    """


class 氢负荷信息(设备基础信息):
    LoadType: 负荷类型 = Field(
        default=负荷类型.Normal,
        title="负荷类型",
        description=f"可选: {', '.join(负荷类型.__members__.keys())}",
    )

    # 正数
    PunishmentRate: confloat(ge=0) = Field(
        default=0, title="惩罚系数", description="单位: 元/kg"
    )
    """
    单位: 元/kg
    """

    Pmin: confloat(ge=0) = Field(default=0, title="负荷功率最小值", description="单位: kg")
    """
    单位: kg
    """

    Pmax: confloat(ge=0) = Field(default=0, title="负荷功率最大值", description="单位: kg")
    """
    单位: kg
    """

    @validator("Pmax")
    def validate_Pmax(cls, v, values):
        if values.get("LoadType", None) in [
            负荷类型.Flexible,
            负荷类型.InterruptableAndFlexible,
        ]:
            p_min = values.get("Pmin", 0)
            assert (
                v >= p_min
            ), f"Pmax must be greater than or equal to Pmin\nGiven: Pmax={v}, Pmin={p_min}"
        return v

    EnergyConsumption: List[confloat(ge=0)] = Field(title="耗能功率表", description="单位: kg")
    """
    单位: kg
    """

    PriceModel: 常数氢价 = Field(title="计价模型", description="单位: 元/kg")


class 电解槽信息(设备信息):
    StartupCountLimit: Optional[int] = Field(
        default=None, title="启动次数限制", description="默认为null"
    )
    LHVHydrogen: float = Field(default=33.3, title="氢气热值", description="单位: kWh/kg")
    """
    单位: kWh/kg
    """

    RatedInputPower: confloat(ge=0) = Field(
        title="额定输入功率", description="名称: 额定输入功率\n单位: kW"
    )
    """
    名称: 额定输入功率
    单位: kW
    """

    HydrogenGenerationStartupRate: confloat(ge=0) = Field(
        title="制氢启动功率比值", description="名称: 制氢启动功率比值\n单位: percent"
    )
    """
    名称: 制氢启动功率比值
    单位: percent
    """

    @validator("HydrogenGenerationStartupRate")
    def validate_HydrogenGenerationStartupRate_for_percent_warning(cls, value):
        warning_msg = None
        field_name = "HydrogenGenerationStartupRate"
        if value <= ies_env.PERCENT_WARNING_THRESHOLD:
            warning_msg = f"Field '{field_name}' (value: {value}; unit: percent) passed to class '{cls.__name__}' is less than or equal to {ies_env.PERCENT_WARNING_THRESHOLD}"
        if warning_msg is not None:
            if ies_env.UNIT_WARNING_AS_ERROR:
                raise Exception(warning_msg)
            else:
                logger_print(warning_msg)
        return value

    HydrogenGenerationEfficiency: confloat(ge=0) = Field(
        title="制氢效率", description="名称: 制氢效率\n单位: percent"
    )
    """
    名称: 制氢效率
    单位: percent
    """

    @validator("HydrogenGenerationEfficiency")
    def validate_HydrogenGenerationEfficiency_for_percent_warning(cls, value):
        warning_msg = None
        field_name = "HydrogenGenerationEfficiency"
        if value <= ies_env.PERCENT_WARNING_THRESHOLD:
            warning_msg = f"Field '{field_name}' (value: {value}; unit: percent) passed to class '{cls.__name__}' is less than or equal to {ies_env.PERCENT_WARNING_THRESHOLD}"
        if warning_msg is not None:
            if ies_env.UNIT_WARNING_AS_ERROR:
                raise Exception(warning_msg)
            else:
                logger_print(warning_msg)
        return value

    DeltaLimit: confloat(ge=0) = Field(
        title="爬坡率", description="名称: 爬坡率\n单位: percent/s"
    )
    """
    名称: 爬坡率
    单位: percent/s
    """

    HeatRecycleEfficiency: confloat(ge=0) = Field(
        title="热量回收效率", description="名称: 热量回收效率\n单位: percent"
    )
    """
    名称: 热量回收效率
    单位: percent
    """

    @validator("HeatRecycleEfficiency")
    def validate_HeatRecycleEfficiency_for_percent_warning(cls, value):
        warning_msg = None
        field_name = "HeatRecycleEfficiency"
        if value <= ies_env.PERCENT_WARNING_THRESHOLD:
            warning_msg = f"Field '{field_name}' (value: {value}; unit: percent) passed to class '{cls.__name__}' is less than or equal to {ies_env.PERCENT_WARNING_THRESHOLD}"
        if warning_msg is not None:
            if ies_env.UNIT_WARNING_AS_ERROR:
                raise Exception(warning_msg)
            else:
                logger_print(warning_msg)
        return value

    CostPerMachine: confloat(ge=0) = Field(
        title="采购成本", description="名称: 采购成本\n单位: 万元/台"
    )
    """
    名称: 采购成本
    单位: 万元/台
    """

    CostPerYearPerMachine: confloat(ge=0) = Field(
        title="固定维护成本", description="名称: 固定维护成本\n单位: 万元/(台*年)"
    )
    """
    名称: 固定维护成本
    单位: 万元/(台*年)
    """

    VariationalCostPerWork: confloat(ge=0) = Field(
        title="可变维护成本", description="名称: 可变维护成本\n单位: 元/kWh"
    )
    """
    名称: 可变维护成本
    单位: 元/kWh
    """

    Life: confloat(ge=0) = Field(title="设计寿命", description="名称: 设计寿命\n单位: 年")
    """
    名称: 设计寿命
    单位: 年
    """

    BuildCostPerMachine: confloat(ge=0) = Field(
        title="建设费用系数", description="名称: 建设费用系数\n单位: 万元/台"
    )
    """
    名称: 建设费用系数
    单位: 万元/台
    """

    BuildBaseCost: confloat(ge=0) = Field(
        title="建设费用基数", description="名称: 建设费用基数\n单位: 万元"
    )
    """
    名称: 建设费用基数
    单位: 万元
    """

    MaxDeviceCount: confloat(ge=0) = Field(
        title="最大安装台数", description="名称: 最大安装台数\n单位: 台"
    )
    """
    名称: 最大安装台数
    单位: 台
    """

    MinDeviceCount: confloat(ge=0) = Field(
        title="最小安装台数", description="名称: 最小安装台数\n单位: 台"
    )
    """
    名称: 最小安装台数
    单位: 台
    """

    DeviceCount: confloat(ge=0) = Field(title="安装台数", description="名称: 安装台数\n单位: 台")
    """
    名称: 安装台数
    单位: 台
    """


####################
# model definition #
####################


from sympy.polys.polytools import Poly
import re
from sympy import sympify

# taking too long. recursion.
from progressbar import progressbar

from expr_utils import getExprStrParsedToExprList


def withBanner(banner: str = ""):
    def decorator(func):
        def inner_func(*args, **kwargs):
            logger_print(f"_____________{banner}_____________")
            val = func(*args, **kwargs)
            logger_print(f"_____________{banner}_____________")
            return val

        return inner_func

    return decorator


@withBanner("ERROR LOG")
def examineSubExprDegree(expr):
    data = str(expr)
    exprlist = getExprStrParsedToExprList(data)
    logger_print("ANALYSING TERMS")
    for subexpr in progressbar(exprlist):
        subpoly = Poly(subexpr)
        subpoly_deg = subpoly.total_degree()
        if subpoly_deg not in [0, 1]:
            logger_print()
            logger_print("Abnormal subexpression poly degree:", subpoly_deg)
            # recover expression representation
            logger_print("Abnormal expression:", subexpr)
    logger_print()


from collections import defaultdict


import flashtext


class SharedParams(BaseModel):
    典型日: bool
    计算步长: Literal["小时", "秒"]
    计算类型: Literal["仿真模拟", "设计规划"]
    计算目标: Literal["经济", "环保", "经济_环保"]


class InputParams(SharedParams):
    calcParamList: List
    rangeDict: Union[None, dict]
    needResult: bool
    additional_constraints: dict


class ModelWrapper:
    inputParams: InputParams

    def __init__(self, model: Optional[ConcreteModel] = None, cloned: bool = False):
        self.model = model if model is not None else ConcreteModel()
        self.clock = {}
        self.cloned = cloned
        self.assumptions: List[Callable] = []
        self.keyword_processor = flashtext.KeywordProcessor()
        self._obj = ...
        self._obj_expr = ...
        self._submodelName = "defaultSubmodelName"
        self.varNameToSubmodelName = cast(
            Dict[str, str], defaultdict(lambda: "unknownSubmodelName")
        )
        self.submodelNameToVarName = cast(Dict[str, List[str]], defaultdict(lambda: []))
        self.submodelNameToVarName.update({self._submodelName: []})

        self._submodelClassName = "defaultSubmodelClassName"
        self.varNameToSubmodelClassName = cast(
            Dict[str, str], defaultdict(lambda: "unknownSubmodelClassName")
        )
        self.submodelClassNameToVarName = cast(
            Dict[str, List[str]], defaultdict(lambda: [])
        )
        self.submodelClassNameToVarName.update({self._submodelClassName: []})

        # TODO: put assumptions into here after any operation using BigM notation (like multiplication)

    def objGetter(self):
        return self._obj

    def objSetter(self, val):
        self._obj = val

    obj = property(fget=objGetter, fset=objSetter)

    def obj_exprGetter(self):
        return self._obj_expr

    def obj_exprSetter(self, val):
        self._obj_expr = val

    obj_expr = property(fget=obj_exprGetter, fset=obj_exprSetter)

    def setSubmodelName(self, submodelName: str):
        assert isinstance(
            submodelName, str
        ), f"submodelName must be a string!\nsubmodelName: {repr(submodelName)}"
        assert len(submodelName) >= 1, "zero length submodelName submitted."
        submodelName = submodelName.strip()
        self._submodelName = submodelName
        self.submodelNameToVarName[submodelName] = self.submodelNameToVarName.get(
            submodelName, []
        )

    def getSubmodelName(self):
        return self._submodelName

    submodelName = property(fset=setSubmodelName, fget=getSubmodelName)

    def setSubmodelClassName(self, submodelClassName: str):
        assert isinstance(
            submodelClassName, str
        ), f"submodelClassName must be a string!\nsubmodelClassName: {repr(submodelClassName)}"
        assert len(submodelClassName) >= 1, "zero length submodelClassName submitted."
        submodelClassName = submodelClassName.strip()
        self._submodelClassName = submodelClassName
        self.submodelClassNameToVarName[
            submodelClassName
        ] = self.submodelClassNameToVarName.get(submodelClassName, [])

    def getSubmodelClassName(self):
        return self._submodelClassName

    submodelClassName = property(fset=setSubmodelClassName, fget=getSubmodelClassName)

    def check_assumptions(self):
        # TODO: call this function after model solved.
        for assumption in self.assumptions:
            assumption()
        self.assumptions = []  # clear assumptions

    def word_counter(self, text: str) -> Dict[str, int]:
        keywords_found = self.keyword_processor.extract_keywords(text)

        keyword_counts = {}
        for keyword in keywords_found:
            keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1

        return keyword_counts

    def __del__(self):
        del self.model
        del self.clock
        del self

    def getSpecialName(self, key: str):
        val = self.clock.get(key, 0)
        name = f"{key}_{val}"
        self.clock[key] = val + 1
        return name

    def Disjunct(self, expression_disjunct: list):
        assert isinstance(expression_disjunct, list)
        name = self.getSpecialName("DJ")
        DJ = Disjunct()
        for i, expr in enumerate(expression_disjunct):
            expr_name = f"expr_{i}"
            self.checkExpressionPolynomialDegree(expr, f"Disjunct_Expression_{i}")
            cons = Constraint(expr=expr)
            DJ.__setattr__(expr_name, cons)
        self.model.__setattr__(name, DJ)
        return DJ

    @staticmethod
    def checkExpressionPolynomialDegree(expr, caller):
        deg = getattr(expr, "polynomial_degree", 0)
        if deg:
            deg = expr.polynomial_degree()
        if deg is None:  # possibly division found
            raise Exception("invalid polynomial degree for:", expr.to_string())
        if deg != 1:
            logger_print("EXPR DEG:", deg)
            expr_repr = f"{str(expr) if len(str(expr))<200 else str(expr)[:200]+'...'}"
            logger_print("EXPR:", expr_repr)
            # only if deg > 0 we need further inspection.
            if deg > 0:
                # TODO: use regex to simplify expression here.
                examineSubExprDegree(expr)
            error_msg = f"[{caller}] Unacceptable polynomial degree for expression."
            raise Exception(error_msg)

    def DisjunctiveConstraints(self, expression_disjunct_list: list[list]):
        assert isinstance(expression_disjunct_list, list)
        DJL = []
        for expression_disjunct in expression_disjunct_list:
            DJ = self.Disjunct(expression_disjunct)
            DJL.append(DJ)
        name = self.getSpecialName("DJV")
        DJV = Disjunction(expr=DJL)
        self.model.__setattr__(name, DJV)
        return DJV, DJL

    def Constraint(self, *args, **kwargs):
        expr = kwargs.pop("expr", args[0] if len(args) > 0 else None)
        if expr is None:
            logger_print("ARGS:", args)
            logger_print("KWARGS:", kwargs)
            raise Exception("Not passing expression to method 'Constraint'")
        self.checkExpressionPolynomialDegree(expr, caller="Constraint")
        name = self.getSpecialName("CON")
        if "initialize" in kwargs.keys():
            del kwargs["initialize"]
        ret = Constraint(expr=expr, *args[1:], **kwargs)
        assert (
            getattr(self.model, name, None) is None
        ), f"错误: 不能设置两次相同的变量名称\n重复变量: { name }"
        self.model.__setattr__(name, ret)

        self.varNameToSubmodelName[name] = self.submodelName
        self.submodelNameToVarName
        self.submodelNameToVarName[self.submodelName].append(name)
        self.keyword_processor.add_keyword(name)

        self.varNameToSubmodelClassName[name] = self.submodelClassName
        self.submodelClassNameToVarName
        self.submodelClassNameToVarName[self.submodelClassName].append(name)
        self.keyword_processor.add_keyword(name)

        return ret

    def Var(self, name: str, *args, **kwargs):
        if "initialize" in kwargs.keys():
            del kwargs["initialize"]
        if ies_env.VAR_INIT_AS_ZERO is not None:
            kwargs["initialize"] = 0
        ret = Var(*args, **kwargs)
        assert (
            getattr(self.model, name, None) is None
        ), f"错误: 不能设置两次相同的变量名称\n重复变量: { name }"
        self.model.__setattr__(name, ret)

        self.varNameToSubmodelName[name] = self.submodelName
        self.submodelNameToVarName
        self.submodelNameToVarName[self.submodelName].append(name)
        self.keyword_processor.add_keyword(name)

        self.varNameToSubmodelClassName[name] = self.submodelClassName
        self.submodelClassNameToVarName
        self.submodelClassNameToVarName[self.submodelClassName].append(name)
        self.keyword_processor.add_keyword(name)

        return ret

    def Objective(self, *args, **kwargs):
        expr = kwargs.pop("expr", args[0] if len(args) > 0 else None)
        if expr is None:
            logger_print("ARGS:", args)
            logger_print("KWARGS:", kwargs)
            raise Exception("Not passing expression to method 'Objective'")
        self.checkExpressionPolynomialDegree(expr, caller="Objective")
        name = self.getSpecialName("OBJ")
        if "initialize" in kwargs.keys():
            del kwargs["initialize"]
        ret = Objective(expr=expr, *args[1:], **kwargs)
        self.obj = ret
        self.obj_expr = expr
        assert (
            getattr(self.model, name, None) is None
        ), f"错误: 不能设置两次相同的变量名称\n重复变量: { name }"
        self.model.__setattr__(name, ret)

        self.varNameToSubmodelName[name] = self.submodelName
        self.submodelNameToVarName
        self.submodelNameToVarName[self.submodelName].append(name)
        self.keyword_processor.add_keyword(name)

        self.varNameToSubmodelClassName[name] = self.submodelClassName
        self.submodelClassNameToVarName
        self.submodelClassNameToVarName[self.submodelClassName].append(name)
        self.keyword_processor.add_keyword(name)

        return ret

    def Block(self, model: Optional[ConcreteModel] = None, cloned: bool = False):
        wrapper = ModelWrapper(model, cloned=cloned)
        name = self.getSpecialName("BLK")
        self.model.__setattr__(name, wrapper.model)
        self.varNameToSubmodelName[name] = self.submodelName
        self.submodelNameToVarName
        self.submodelNameToVarName[self.submodelName].append(name)
        self.keyword_processor.add_keyword(name)

        self.varNameToSubmodelClassName[name] = self.submodelClassName
        self.submodelClassNameToVarName
        self.submodelClassNameToVarName[self.submodelClassName].append(name)
        self.keyword_processor.add_keyword(name)

        return wrapper


# first convert the unit.
# assign variables.

# shall you assign port with variables.

# 风、光照


# 需要明确单位
class 计算参数(SharedParams):
    典型日ID: Union[conint(ge=0), None] = None  # increse by external loop

    分时计价开始时间点: float = Field(
        default=0,
        title="秒级仿真时 开始时间在一天中的哪个小时",
        description=f"取值范围: 0-{每天小时数}",
        ge=0,
        le=每天小时数,
    )

    分时计价开始月份: int = Field(
        default=0, title="秒级仿真时 开始时间在一年中的哪个月份", description="取值范围: 0-11", le=11, ge=0
    )

    典型日代表的日期: conlist(
        conint(ge=0, lt=365), min_items=0, max_items=365, unique_items=True
    ) = []

    @validator("典型日代表的日期")
    def validate_typical_day(cls, v, values):
        if values["典型日"]:
            len_v = len(v)
            assert len_v > 0
            assert len_v <= 365
        return v

    风速: List[confloat(ge=0)]
    """
    单位: m/s
    """
    光照: List[confloat(ge=0)]
    """
    单位: kW/m2
    """
    气温: List[confloat(ge=0)]
    """
    单位: 摄氏度
    """
    贴现率: confloat(ge=0, le=100) = Field(title="贴现率", description="单位: percent")
    """
    单位: percent
    """

    @property
    def 迭代步数(self):
        if self.计算步长 == "秒":
            steps = 两小时秒数
        elif self.计算步长 == "小时" and self.典型日 is False:
            steps = 每年小时数
        elif self.计算步长 == "小时" and self.典型日 is True:
            steps = 每天小时数
        else:
            logger_print(self)
            raise Exception("未知计算参数")
        errors = []

        if not len(self.风速) == steps:
            errors.append(f"风速长度应该是{steps} 实际:{len(self.风速)}")
        if not len(self.光照) == steps:
            errors.append(f"光照长度应该是{steps} 实际:{len(self.光照)}")
        if not len(self.气温) == steps:
            errors.append(f"气温长度应该是{steps} 实际:{len(self.气温)}")

        if errors:
            raise Exception("\n".join(errors))
        return steps

    @property
    def 时间参数(self):
        """
        如果计算步长为秒，那么返回3600
        如果计算步长为小时，那么返回1

        相当于返回一小时内有多少计算步长
        """
        return 1 if self.计算步长 == "小时" else 每小时秒数

    @property
    def deltaT(self):
        """
        如果计算步长为秒，那么返回1/3600
        如果计算步长为小时，那么返回1

        相当于返回一个计算步长内有多少小时
        """
        return 1 / self.时间参数

    @property
    def 总计算时长(self):
        """
        返回该计算模式下总共有多少小时
        """
        return self.迭代步数 / self.时间参数


class POSNEG:
    def __init__(self, x, x_pos, x_neg, b_pos, b_neg, x_abs):
        self.x = x
        self.x_pos = x_pos
        self.x_neg = x_neg
        self.b_pos = b_pos
        self.b_neg = b_neg
        self.x_abs = x_abs


try:
    from typing import Protocol
except:
    from typing_extensions import Protocol


class 可购买类(Protocol):
    是否购买: ...
    总采购成本: ...
    总建设费用: ...
    总固定维护成本: ...
    总固定成本年化: ...
    总成本年化: ...
    总可变维护成本年化: ...

    def BinVarMultiplySingle(self, *args, **kwargs):
        ...


class 设备模型:
    def __init__(self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, ID: int):
        logger_print(
            "Building Device Model:", submodelClassName := self.__class__.__name__
        )
        submodelName = f"{submodelClassName}_{ID}"
        self.mw = mw
        self.mw.submodelName = submodelName
        self.mw.submodelClassName = submodelClassName
        self.PD = PD
        self.计算参数 = 计算参数实例
        self.ID = ID
        self.SID = 0
        self.BigM = 1e7  # 这个数不能太大 否则就会报错
        """
        一个极大数
        """
        self.EPS = 1e-4
        """
        一个极小数
        """
        self.总采购成本 = 0
        self.总建设费用 = 0
        self.总固定维护成本 = 0
        self.总固定成本年化 = 0
        self.总成本年化 = 0
        self.总可变维护成本年化 = 0
        self.年化率 = ...

    def TimeSummation(self, target: list, source, mrange=None):
        mrange = self.getRange(mrange)
        for i in mrange:
            target[i] += source[i]
        return target

    @staticmethod
    def 处理最终财务输出(mclass: 可购买类):
        mclass.总采购成本 = mclass.BinVarMultiplySingle(mclass.是否购买, mclass.总采购成本)
        mclass.总建设费用 = mclass.BinVarMultiplySingle(mclass.是否购买, mclass.总建设费用)
        mclass.总固定维护成本 = mclass.BinVarMultiplySingle(mclass.是否购买, mclass.总固定维护成本)
        mclass.总固定成本年化 = mclass.BinVarMultiplySingle(mclass.是否购买, mclass.总固定成本年化)
        mclass.总成本年化 = mclass.BinVarMultiplySingle(mclass.是否购买, mclass.总成本年化)
        mclass.总可变维护成本年化 = mclass.BinVarMultiplySingle(mclass.是否购买, mclass.总可变维护成本年化)

    def constraints_register(self):
        if self.__class__.__name__ == "设备模型":
            raise NotImplementedError("Must be implemented by subclasses.")
        logger_print("REGISTERING: ", self.__class__.__name__)

    def getVarName(self, varName: str):
        VN = f"DI_{self.ID}_VN_{varName}"  # use underscore.
        if self.计算参数.典型日ID is not None:  # starting from 0, so be careful!
            VN = f"TD_{self.计算参数.典型日ID}_" + VN
        return VN

    def getSpecialVarName(self, varName: str):
        specialVarName = f"SP_{self.SID}_{varName}"
        self.SID += 1
        return specialVarName

    def 单变量(self, varName: str, **kwargs):
        var = self.mw.Var(self.getVarName(varName), **kwargs)
        return var

    def getRange(self, mrange: range = None):
        if mrange is None:
            mrange = range(self.计算参数.迭代步数)
        return mrange

    def 变量列表(self, varName: str, mrange: range = None, **kwargs):
        var = self.mw.Var(self.getVarName(varName), self.getRange(mrange), **kwargs)
        return var

    def DisjunctiveRangeConstraint(
        self, var_1, var_2, expression=..., mrange: range = None
    ):
        assert expression is not ...
        ret_list = []
        for i in self.getRange(mrange):
            ret_elem = self.mw.DisjunctiveConstraints(expression(var_1[i], var_2[i]))
            ret_list.append(ret_elem)
        return ret_list

    def DisjunctiveRangeConstraintMulti(
        self, *vars, expression=..., mrange: range = None
    ):
        assert expression is not ...
        ret_list = []
        for i in self.getRange(mrange):
            ret_elem = self.mw.DisjunctiveConstraints(
                expression(*[var[i] for var in vars])
            )
            ret_list.append(ret_elem)
        return ret_list

    def RangeConstraint(self, var_1, var_2, expression=..., mrange: range = None):
        assert expression is not ...
        ret_list = []
        for i in self.getRange(mrange):
            ret_elem = self.mw.Constraint(expression(var_1[i], var_2[i]))
            ret_list.append(ret_elem)
        return ret_list

    def RangeConstraintMulti(self, *vars, expression=..., mrange: range = None):
        assert expression is not ...
        ret_list = []
        for i in self.getRange(mrange):
            ret_elem = self.mw.Constraint(expression(*[var[i] for var in vars]))
            ret_list.append(ret_elem)
        return ret_list

    def CustomDisjunctiveRangeConstraint(
        self, var_1, var_2, expression=..., customRange: range = ...
    ):
        assert customRange is not ...
        assert expression is not ...
        ret_list = []
        for i in customRange:
            ret_elem = self.mw.DisjunctiveConstraints(expression(var_1, var_2, i))
            ret_list.append(ret_elem)
        return ret_list

    def CustomDisjunctiveRangeConstraintMulti(
        self, *vars, expression=..., customRange: range = ...
    ):
        assert customRange is not ...
        assert expression is not ...
        ret_list = []
        for i in customRange:
            ret_elem = self.mw.DisjunctiveConstraints(expression(*vars, i))
            ret_list.append(ret_elem)
        return ret_list

    def CustomRangeConstraint(
        self, var_1, var_2, expression=..., customRange: range = ...
    ):
        assert customRange is not ...
        assert expression is not ...
        ret_list = []
        for i in customRange:
            ret_elem = self.mw.Constraint(expression(var_1, var_2, i))
            ret_list.append(ret_elem)
        return ret_list

    def CustomRangeConstraintMulti(
        self, *vars, expression=..., customRange: range = ...
    ):
        assert customRange is not ...
        assert expression is not ...
        ret_list = []
        for i in customRange:
            ret_elem = self.mw.Constraint(expression(*vars, i))
            ret_list.append(ret_elem)
        return ret_list

    def SumRange(self, var_1, mrange: range = None):
        return sum([var_1[i] for i in self.getRange(mrange)])

    def 单变量转列表(self, var, dup: int = None):
        if dup is None:
            dup = self.计算参数.迭代步数
        return [var for _ in range(dup)]

    def 单表达式生成指示变量(self, varName: str, expr):
        # where to exclude type from type hints?
        # or what language can express type exclusion?
        posneg = self.变量列表_带指示变量(varName, exprList=[expr], mrange=range(1))
        ret = POSNEG(
            posneg.x[0],
            posneg.x_pos[0],
            posneg.x_neg[0],
            posneg.b_pos[0],
            posneg.b_neg[0],
            posneg.x_abs[0],
        )
        return ret

    def 变量列表_带指示变量(
        self, varName: str, exprList: list = None, within=Reals, mrange: range = None
    ) -> POSNEG:
        # can replace with disjunctions
        if exprList:
            x = exprList
        else:
            x = self.变量列表(varName, within=within, mrange=mrange)

        b_pos = self.变量列表(
            self.getSpecialVarName(varName), within=Boolean, mrange=mrange
        )
        x_pos = self.变量列表(
            self.getSpecialVarName(varName), within=NonNegativeReals, mrange=mrange
        )

        self.RangeConstraint(
            b_pos, x_pos, lambda x, y: x * self.BigM >= y, mrange=mrange
        )
        b_neg = self.变量列表(
            self.getSpecialVarName(varName), within=Boolean, mrange=mrange
        )
        x_neg = self.变量列表(
            self.getSpecialVarName(varName), within=NonNegativeReals, mrange=mrange
        )

        self.RangeConstraint(
            b_neg, x_neg, lambda x, y: x * self.BigM >= y, mrange=mrange
        )

        self.RangeConstraint(b_pos, b_neg, lambda x, y: x + y == 1, mrange=mrange)

        self.RangeConstraintMulti(
            x, x_pos, x_neg, expression=lambda x, y, z: x == y - z, mrange=mrange
        )

        x_abs = self.变量列表(
            self.getSpecialVarName(varName), within=NonNegativeReals, mrange=mrange
        )

        self.RangeConstraintMulti(
            x_pos, x_neg, x_abs, expression=lambda x, y, z: z == x + y, mrange=mrange
        )

        posneg = POSNEG(x, x_pos, x_neg, b_pos, b_neg, x_abs)

        return posneg

    def DisjunctivePair(self, x_var, y_var, x_vals: List[float], y_vals: List[float]):
        assert len(x_vals) == len(y_vals)
        DJL = []

        x_lb, x_ub = min(x_vals), max(x_vals)
        y_lb, y_ub = min(y_vals), max(y_vals)

        for x_value, y_value in zip(x_vals, y_vals):
            disjunct_name = self.getSpecialVarName("DJ")
            DJ = Disjunct()

            x_var.setlb(x_lb)
            x_var.setub(x_ub)

            y_var.setlb(y_lb)
            y_var.setub(y_ub)

            DJ.cons_x = Constraint(expr=x_var == x_value)
            DJ.cons_y = Constraint(expr=y_var == y_value)
            assert (
                getattr(self.mw.model, disjunct_name, None) is None
            ), f"错误: 不能设置两次相同的变量名称\n重复变量: { disjunct_name }"
            self.mw.model.__setattr__(disjunct_name, DJ)

            DJL.append(DJ)

        disjunctive_name = self.getSpecialVarName("DJV")
        DJV = Disjunction(expr=DJL)
        assert (
            getattr(self.mw.model, disjunctive_name, None) is None
        ), f"错误: 不能设置两次相同的变量名称\n重复变量: { disjunctive_name }"
        self.mw.model.__setattr__(disjunctive_name, DJV)

        return DJL, DJV

    def DisjunctivePairList(
        self,
        x_var_list,
        y_var_list,
        x_vals: List[float],
        y_vals: List[float],
        range_list: Union[List[int], None] = None,
    ):
        # TODO: detect and transform model if disjuction is detected in model components
        range_list = self.getRangeList(range_list)
        DJV_LIST = []
        for i in range_list:
            _, DJV = self.DisjunctivePair(x_var_list[i], y_var_list[i], x_vals, y_vals)
            DJV_LIST.append(DJV)
        return DJV_LIST

    def PiecewisePair(
        self,
        x_var,
        y_var,
        x_vals: List[float],
        y_vals: List[float],
        pw_repn="MC",
        pw_constr_type="EQ",
        unbounded_domain_var=True,
        warn_domain_coverage=False,
        preprocessed=False,
    ):
        if not preprocessed:
            _x_vals, _y_vals = self.PreprocessPiecewiseValueList(x_vals, y_vals)
        else:
            _x_vals, _y_vals = x_vals, y_vals

        piecewise_name = self.getSpecialVarName("PW")
        PW = Piecewise(
            y_var,
            x_var,
            pw_pts=_x_vals,
            f_rule=_y_vals,
            pw_repn=pw_repn,
            pw_constr_type=pw_constr_type,
            unbounded_domain_var=unbounded_domain_var,
            warn_domain_coverage=warn_domain_coverage,  # to suppress warning
        )
        assert (
            getattr(self.mw.model, piecewise_name, None) is None
        ), f"错误: 不能设置两次相同的变量名称\n重复变量: { piecewise_name }"
        self.mw.model.__setattr__(piecewise_name, PW)

        return PW

    @staticmethod
    def PreprocessPiecewiseValueList(
        x_vals: List[float], y_vals: List[float], expand_val=1e3
    ):
        assert x_vals[0] <= x_vals[-1]
        _x_vals = [x_vals[0] - expand_val] + x_vals + [x_vals[-1] + expand_val]
        _y_vals = [y_vals[0]] + y_vals + [y_vals[-1]]
        return _x_vals, _y_vals

    def getRangeList(self, range_list):
        if range_list is None:
            range_list = list(range(self.计算参数.迭代步数))
        return range_list

    def Piecewise(
        self,
        x_var,
        y_var,
        x_vals: List[float],
        y_vals: List[float],
        range_list: Union[List[int], None] = None,
        pw_repn="MC",
        pw_constr_type="EQ",
        unbounded_domain_var=True,
        warn_domain_coverage=False,
    ):
        # TODO: if performance overhead is significant, shall use "MC" piecewise functions, or stepwise functions.
        x_var_list = x_var
        y_var_list = y_var

        # BUG: x out of bound, resulting into unsolvable problem.

        _x_vals, _y_vals = self.PreprocessPiecewiseValueList(x_vals, y_vals)

        range_list = self.getRangeList(range_list)

        PWL = []
        for i in range_list:
            PW = self.PiecewisePair(
                x_var_list[i],
                y_var_list[i],
                x_vals=_x_vals,
                y_vals=_y_vals,
                pw_repn=pw_repn,
                pw_constr_type=pw_constr_type,
                unbounded_domain_var=unbounded_domain_var,
                warn_domain_coverage=warn_domain_coverage,
                preprocessed=True,
            )
            PWL.append(PW)
        return PWL

    @staticmethod
    def breakdownExpression(expr):
        expr_type = type(expr)

        assert (
            expr_type != pyomo.core.base.var.IndexedVar
        ), f"Expression: {repr(expr)[:200]}\nInvalid expression type."

        # otherwise, expression types.
        is_linear, results = pyomo.core.expr.current.decompose_term(expr)
        if is_linear:
            return results
        else:
            examineSubExprDegree(expr)
            raise Exception(
                f"Nonlinear expression found while breaking down.\nExpression type: {type(expr)}"
            )

    def BinVarMultiplySingle(self, b_var, x_var, recurse=True):
        assert b_var.is_binary()
        assert type(x_var) is not pyomo.core.base.var.IndexedVar

        numeric_types = [float, int]
        if recurse:
            # tear down x_var
            h_list = []
            for sub_x_var in self.breakdownExpression(x_var):
                _h = self.BinVarMultiplySingle(b_var, sub_x_var, recurse=False)
                h_list.append(_h)
            return sum(h_list)
        else:
            if type(x_var) == tuple:
                assert len(x_var) == 2, f"Invalid `x_var`: {x_var}"
                # format: (factor, x_var)
                assert type(x_var[0]) in [
                    float,
                    int,
                ], f"Invalid `x_var` format: {x_var}\nShould be: (factor (float), x_var (Var))"
                factor, _x_var = x_var
                if _x_var is None:  # constant.
                    return factor * b_var
            else:
                factor = 1
                _x_var = x_var
                if type(_x_var) in numeric_types:
                    return _x_var * b_var

            h = self.单变量(self.getSpecialVarName("BVM"), within=Reals)

            self.mw.Constraint(h <= b_var * self.BigM)
            self.mw.Constraint(h >= -b_var * self.BigM)
            self.mw.Constraint(h <= _x_var + (1 - b_var) * self.BigM)
            self.mw.Constraint(h >= _x_var - (1 - b_var) * self.BigM)
            return h * factor

    def Multiply(
        self, dict_mx: dict, dict_my: dict, varName: str, precision=10, within=Reals
    ):  # two continuous multiplication
        #  (x+y)^2 - (x-y)^2 = 4xy
        mx, max_mx, min_mx = dict_mx["var"], dict_mx["max"], dict_mx["min"]
        my, max_my, min_my = dict_my["var"], dict_my["max"], dict_my["min"]
        assert not mx[0].is_binary()
        assert not my[0].is_binary()

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
            x_var=mx_my_sum_var,
            y_var=mx_my_sum_pow2_var,
            x_vals=mx_my_sum,
            y_vals=mx_my_sum_pow2,
        )  # assume it is absolute.

        self.Piecewise(
            x_var=mx_my_minus_var,
            y_var=mx_my_minus_pow2_var,
            x_vals=mx_my_minus,
            y_vals=mx_my_minus_pow2,
        )

        mx_my_multiply = self.变量列表(varName, within=within)

        self.RangeConstraintMulti(
            mx_my_sum_pow2_var,
            mx_my_minus_pow2_var,
            mx_my_multiply,
            expression=lambda x, y, z: (x - y) / 4 == z,
        )

        return mx_my_multiply


class 光伏发电模型(设备模型):
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 光伏发电ID, 设备信息: 光伏发电信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.RenewableEnergyConsumptionPunishmentRate = self.设备信息.toStandard(
            "RenewableEnergyConsumptionPunishmentRate"
        )
        self.RenewableEnergyConsumptionConstraint = (
            self.设备信息.RenewableEnergyConsumptionConstraint
        )
        self.RenewableEnergyConsumptionRate = self.设备信息.toStandard(
            "RenewableEnergyConsumptionRate"
        )
        self.discardedRenewableEnergyPower = self.变量列表(
            "discardedRenewableEnergyPower", within=NonNegativeReals
        )
        self.punishRate = 0
        """
        惩罚代价
        单位：万元/h
        """
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
            # BUG: if unbounded, then we get some error.
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
        类型: 输出
        """

        # 设备特有约束（变量）
        self.电输出 = self.电接口

        if self.计算参数.计算类型 == "设计规划":
            # TODO：标准光照下出力
            self.MaxDeviceCount = math.ceil(self.MaxInstallArea / self.Area)
            self.MinDeviceCount = math.floor(self.MinInstallArea / self.Area)
            assert self.MinDeviceCount >= 0
            assert self.MaxDeviceCount >= self.MinDeviceCount

        self.POSNEG_是否购买 = self.单表达式生成指示变量("POSNEG_是否购买", self.DeviceCount - 0.5)
        self.是否购买 = self.POSNEG_是否购买.b_pos

        if isinstance(self.DeviceCount, Var):  # 设备台数约束
            self.DeviceCount.setlb(self.MinDeviceCount)
            self.DeviceCount.setub(self.MaxDeviceCount)

    def constraints_register(self):
        super().constraints_register()
        # 设备特有约束（非变量）

        # 输出输入功率约束
        光电转换效率 = self.MaxPower / self.Area  # 1kW/m2光照下能产生的能量 省略除以1 单位: one
        assert 光电转换效率 <= 1, f"光电转换效率数值不正常: {光电转换效率} (应当在0-1之间)\n光电转换效率 = 单块最大功率 / 单块面积"
        总最大功率 = self.MaxPower * self.DeviceCount
        总面积 = self.Area * self.DeviceCount

        # 光照强度 * 总面积 * 光电转换效率 * 电电转换效率
        # (kW/m2) * m2 * one * one -> kW
        self.RangeConstraintMulti(
            self.计算参数.光照,
            self.电输出,
            self.discardedRenewableEnergyPower,
            expression=lambda x, y, z: x * 总面积 * 光电转换效率 * self.PowerConversionEfficiency
            == y + z,
        )

        # BUG: 限制最大功率输出（标准光照下）
        self.RangeConstraintMulti(
            self.电输出,
            expression=lambda x: x
            <= self.MaxPower * self.DeviceCount * self.PowerConversionEfficiency,
        )

        if self.RenewableEnergyConsumptionConstraint == 新能源消纳约束.惩罚代价:
            self.punishRate = (
                quicksum_indexed_var(self.discardedRenewableEnergyPower)
                / self.计算参数.迭代步数
            ) * self.RenewableEnergyConsumptionPunishmentRate
        elif self.RenewableEnergyConsumptionConstraint == 新能源消纳约束.限制消纳率:
            self.mw.Constraint(
                expr=(1 - self.RenewableEnergyConsumptionRate)
                * quicksum_indexed_var(self.电输出)
                > self.RenewableEnergyConsumptionRate
                * quicksum_indexed_var(self.discardedRenewableEnergyPower)
            )
        elif self.RenewableEnergyConsumptionConstraint == 新能源消纳约束.无:
            ...
        else:
            raise Exception(
                f"未知新能源消纳约束：{self.RenewableEnergyConsumptionConstraint}\n元件模型: {self.__class__.__name__}"
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
        self.年化率 = 计算年化率(self.计算参数.贴现率, Life)

        self.总采购成本 = self.CostPerKilowatt * (总最大功率)
        self.总固定维护成本 = self.CostPerYearPerKilowatt * (总最大功率)
        self.总建设费用 = self.BuildCostPerKilowatt * (总最大功率) + self.BuildBaseCost

        self.总固定成本年化 = (self.总采购成本 + self.总建设费用) * self.年化率 + self.总固定维护成本

        self.总可变维护成本年化 = (
            ((self.SumRange(self.电输出)) / self.计算参数.迭代步数)
            * 每年小时数
            * self.VariationalCostPerWork
        )
        # avg_power * 8760 = annual_work

        self.总成本年化 = self.总固定成本年化 + self.总可变维护成本年化

        self.处理最终财务输出(self)

        return self.总成本年化


class 风力发电模型(设备模型):
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 风力发电ID, 设备信息: 风力发电信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.RenewableEnergyConsumptionPunishmentRate = self.设备信息.toStandard(
            "RenewableEnergyConsumptionPunishmentRate"
        )
        self.RenewableEnergyConsumptionConstraint = (
            self.设备信息.RenewableEnergyConsumptionConstraint
        )
        self.RenewableEnergyConsumptionRate = self.设备信息.toStandard(
            "RenewableEnergyConsumptionRate"
        )
        self.discardedRenewableEnergyPower = self.变量列表(
            "discardedRenewableEnergyPower", within=NonNegativeReals
        )
        self.punishRate = 0
        """
        惩罚代价
        单位：万元/h
        """
        self.CutoutPower: float = 设备信息.CutoutPower
        """
        名称: 切出功率
        单位: kWp
        """
        assert self.CutoutPower >= 0

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
            # BUG: if unbounded, then we get some error.
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
        类型: 输出
        """

        # 设备特有约束（变量）
        self.电输出 = self.电接口
        self.单台发电功率 = ...

        self.POSNEG_是否购买 = self.单表达式生成指示变量("POSNEG_是否购买", self.DeviceCount - 0.5)
        self.是否购买 = self.POSNEG_是否购买.b_pos

        if isinstance(self.DeviceCount, Var):  # 设备台数约束
            self.DeviceCount.setlb(self.MinDeviceCount)
            self.DeviceCount.setub(self.MaxDeviceCount)

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
        assert self.RatedWindSpeed >= self.MinWindSpeed
        assert self.MaxWindSpeed >= self.RatedWindSpeed

        if self.设备信息.machineType in [风力发电类型.变桨, 风力发电类型.定桨]:
            发电曲线参数 = self.RatedPower / ((self.RatedWindSpeed - self.MinWindSpeed) ** 3)

            # windspeed (m/s) -> current power per device (kW)
            WS = np.array(
                self.计算参数.风速, dtype=np.float64
            )  # BUG: before that it was "np.int64", which introduce errors.
            if self.设备信息.machineType == 风力发电类型.定桨:
                # 额定功率 +( (切出功率 - 额定功率)*(实际风速-额定风速)) / (切出风速-额定风速)
                定桨风机特有函数 = lambda 实际风速: self.RatedPower + (
                    (self.CutoutPower - self.RatedPower) * (实际风速 - self.RatedWindSpeed)
                ) / (self.MaxWindSpeed - self.RatedWindSpeed)
            self.单台发电功率 = 单台发电功率 = np.piecewise(
                WS,
                [
                    WS <= self.MinWindSpeed,
                    np.logical_and(WS > self.MinWindSpeed, WS <= self.RatedWindSpeed),
                    np.logical_and(WS > self.RatedWindSpeed, WS <= self.MaxWindSpeed),
                    WS > self.MaxWindSpeed,
                ],
                [
                    0,
                    lambda x: 发电曲线参数 * ((x - self.MinWindSpeed) ** 3),
                    self.RatedPower if self.设备信息.machineType == 风力发电类型.变桨 else 定桨风机特有函数,
                    0,
                ],
            )
            self.单台发电功率 = 单台发电功率 = 单台发电功率.tolist()
        elif self.设备信息.machineType in [风力发电类型.标幺值]:
            assert self.设备信息.normalizedPower is not None, "标幺值风机不能传空的标幺值"
            assert (length := len(self.设备信息.normalizedPower)) == (
                required_length := self.计算参数.迭代步数
            ), f"标幺值长度不合理\n迭代步数: {required_length}\n实际: {length}"
            self.单台发电功率 = 单台发电功率 = [
                self.RatedPower * normalizedPower
                for normalizedPower in self.设备信息.normalizedPower
            ]
        else:
            raise Exception(f"未知风机类型：{self.设备信息.machineType}")

        # 输出输入功率约束
        self.RangeConstraintMulti(
            单台发电功率,
            self.电输出,
            self.discardedRenewableEnergyPower,
            expression=lambda x, y, z: x * self.DeviceCount == y + z,
        )
        if self.RenewableEnergyConsumptionConstraint == 新能源消纳约束.惩罚代价:
            self.punishRate = (
                quicksum_indexed_var(self.discardedRenewableEnergyPower)
                / self.计算参数.迭代步数
            ) * self.RenewableEnergyConsumptionPunishmentRate
        elif self.RenewableEnergyConsumptionConstraint == 新能源消纳约束.限制消纳率:
            self.mw.Constraint(
                expr=(1 - self.RenewableEnergyConsumptionRate)
                * quicksum_indexed_var(self.电输出)
                > self.RenewableEnergyConsumptionRate
                * quicksum_indexed_var(self.discardedRenewableEnergyPower)
            )
        elif self.RenewableEnergyConsumptionConstraint == 新能源消纳约束.无:
            ...
        else:
            raise Exception(
                f"未知新能源消纳约束：{self.RenewableEnergyConsumptionConstraint}\n元件模型: {self.__class__.__name__}"
            )

        if self.计算参数.计算步长 == "秒" and self.设备信息.machineType != 风力发电类型.标幺值:
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
        self.年化率 = 计算年化率(self.计算参数.贴现率, Life)

        self.总采购成本 = self.CostPerKilowatt * (self.DeviceCount * self.RatedPower)
        self.总固定维护成本 = self.CostPerYearPerKilowatt * (
            self.DeviceCount * self.RatedPower
        )
        self.总建设费用 = (
            self.BuildCostPerKilowatt * (self.DeviceCount * self.RatedPower)
            + self.BuildBaseCost
        )

        self.总固定成本年化 = (self.总采购成本 + self.总建设费用) * self.年化率 + self.总固定维护成本

        self.总可变维护成本年化 = (
            ((self.SumRange(self.电输出)) / self.计算参数.迭代步数)
            * 每年小时数
            * self.VariationalCostPerWork
        )
        # avg_power * 8760 = annual_work

        self.总成本年化 = self.总固定成本年化 + self.总可变维护成本年化

        self.处理最终财务输出(self)

        return self.总成本年化


class 柴油发电模型(设备模型):
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 柴油发电ID, 设备信息: 柴油发电信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.燃料热值: float = 0  # 需要拓扑解析之后进行赋值
        self.unitSingleStartupCost = self.设备信息.toStandard("unitSingleStartupCost")
        self.averageLoadRate = self.设备信息.toStandard("averageLoadRate")
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
            # BUG: if unbounded, then we get some error.
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
        """
        DieselToPower: 燃油消耗率
        单位: m3 / kWh <- L/kWh

        Load: 负载率
        单位: one <- percent
        """
        self.DieselToPower_Load.sort(key=lambda x: x[1])

        ##### PORT VARIABLE DEFINITION ####

        self.ports = {}

        self.PD[self.设备ID.电接口] = self.ports["电接口"] = self.电接口 = self.变量列表(
            "电接口", within=NonNegativeReals
        )
        """
        类型: 输出
        """

        self.PD[self.设备ID.燃料接口] = self.ports["燃料接口"] = self.燃料接口 = self.变量列表(
            "燃料接口", within=NonPositiveReals
        )
        """
        类型: 输入
        """

        # 设备特有约束（变量）
        self.电输出 = self.电接口
        self.柴油输入 = self.燃料接口

        self.Nrun_indicators = self.变量列表_带指示变量("Nrun_indicators")
        self.机组年运行时间 = (
            quicksum_indexed_var(self.Nrun_indicators.b_pos) / self.计算参数.迭代步数
        ) * 8760

        # TODO: define some variables with expression

        self.Nrun = self.变量列表("Nrun", within=NonNegativeIntegers)
        """
        机组开启台数
        """
        self.RangeConstraint(
            self.Nrun, self.Nrun_indicators.x, expression=lambda x, y: x == y + 0.5
        )

        self.RangeConstraintMulti(self.Nrun, expression=lambda x: x <= self.DeviceCount)
        self.Nstart = self.变量列表_带指示变量("Nstart")
        """
        机组开启台数求导
        """
        self.mw.Constraint(expr=self.Nstart.x[0] == 0)
        self.CustomRangeConstraintMulti(
            self.Nstart.x,
            self.Nrun,
            expression=lambda x, y, i: x[i + 1] == y[i + 1] - y[i],
            customRange=range(self.计算参数.迭代步数 - 1),
        )

        self.机组年启动次数 = quicksum_indexed_var(self.Nstart.x_pos) * (
            8760 / self.计算参数.总计算时长
        )

        if self.设备信息.unitAnnualOperatingTimeConstraint:
            self.mw.Constraint(
                expr=self.机组年运行时间 <= self.设备信息.maximumAnnualOperatingTimeLimitOfTheUnit
            )

        self.annualUnitStartupCosts = 0
        if self.设备信息.considerUnitStartUpCosts:
            self.annualUnitStartupCosts = self.机组年启动次数 * self.unitSingleStartupCost

        if self.设备信息.unitPlanningAlgorithmSelection == 油耗规划算法.平均:
            x = self.averageLoadRate
            xp = [e[1] for e in self.DieselToPower_Load]
            fp = [e[0] for e in self.DieselToPower_Load]
            self.averageDieselConsumptionRate = np.interp(x, xp, fp)

        elif self.设备信息.unitPlanningAlgorithmSelection == 油耗规划算法.最佳:
            self.子机组列表 = []
            self.子机组柴油输入列表 = []
            self.子机组电输出列表 = []
            self.子机组是否开启列表 = []
            self.子机组是否真的开启列表 = []
            self.子机组数目 = (
                self.MaxDeviceCount if self.计算参数.计算类型 == "设计规划" else self.DeviceCount
            )
            self.子机组数目 = int(self.子机组数目)
            self.子机组是否购买 = self.变量列表(
                "子机组是否购买", mrange=range(self.子机组数目), within=Boolean
            )

            for i in range(self.子机组数目):
                logger_print(f"正在创建第{i+1}个柴油子机组模型")
                subModelWrapper = self.mw.Block()
                子机组模型 = 设备模型({}, subModelWrapper, self.计算参数, i)
                self.子机组列表.append(子机组模型)

                子机组柴油输入 = 子机组模型.变量列表("子机组柴油输入", within=NonPositiveReals)
                self.子机组柴油输入列表.append(子机组柴油输入)

                子机组电输出 = 子机组模型.变量列表("子机组电输出", within=NonNegativeReals)
                self.子机组电输出列表.append(子机组电输出)

                子机组是否开启 = 子机组模型.变量列表("子机组是否开启", within=Boolean)
                self.子机组是否开启列表.append(子机组是否开启)

                子机组是否真的开启 = 子机组模型.变量列表("子机组是否真的开启", within=Boolean)
                self.子机组是否真的开启列表.append(子机组是否真的开启)

            # define series of submodels
        else:
            raise Exception("未知油耗规划算法：", self.设备信息.unitPlanningAlgorithmSelection)

        self.POSNEG_是否购买 = self.单表达式生成指示变量("POSNEG_是否购买", self.DeviceCount - 0.5)
        self.是否购买 = self.POSNEG_是否购买.b_pos

        if isinstance(self.DeviceCount, Var):  # 设备台数约束
            self.DeviceCount.setlb(self.MinDeviceCount)
            self.DeviceCount.setub(self.MaxDeviceCount)

    def constraints_register(self):
        super().constraints_register()
        # 设备特有约束（非变量）

        assert self.燃料热值 != 0
        assert type(self.燃料热值) in [int, float]

        # 输出输入功率约束

        if self.设备信息.unitPlanningAlgorithmSelection == 油耗规划算法.平均:
            self.RangeConstraint(
                self.电输出,
                self.Nrun_indicators.b_pos,
                lambda x, y: x >= y * self.RatedPower * self.PowerStartupLimit,
            )
            self.RangeConstraint(
                self.电输出, self.Nrun, lambda x, y: x <= y * self.RatedPower
            )
            self.RangeConstraint(
                self.电输出, self.Nrun, lambda x, y: x >= (y - 1) * self.RatedPower
            )

            self.RangeConstraint(
                self.柴油输入,
                self.电输出,
                lambda x, y: -x == self.averageDieselConsumptionRate * y,
            )

        elif self.设备信息.unitPlanningAlgorithmSelection == 油耗规划算法.最佳:
            子机组购买数目 = 0

            子机组柴油输入求和 = [0] * self.计算参数.迭代步数
            子机组电输出求和 = [0] * self.计算参数.迭代步数
            子机组是否真的开启求和 = [0] * self.计算参数.迭代步数

            for i in range(self.子机组数目):
                logger_print(f"正在为第{i+1}个柴油子机组模型创建约束")

                子机组模型: 设备模型 = self.子机组列表[i]

                子机组柴油输入 = self.子机组柴油输入列表[i]
                子机组电输出 = self.子机组电输出列表[i]
                子机组是否开启 = self.子机组是否开启列表[i]
                子机组是否真的开启 = self.子机组是否真的开启列表[i]

                子机组是否购买 = self.子机组是否购买[i]

                子机组模型.RangeConstraintMulti(
                    子机组电输出, expression=lambda x: x <= 子机组是否购买 * self.BigM
                )
                子机组模型.RangeConstraint(
                    子机组电输出, 子机组是否开启, expression=lambda x, y: x <= y * self.RatedPower
                )
                子机组模型.RangeConstraint(
                    子机组电输出,
                    子机组是否开启,
                    expression=lambda x, y: x
                    >= y * self.RatedPower * self.PowerStartupLimit,
                )

                子机组模型.RangeConstraint(
                    子机组是否开启,
                    子机组是否真的开启,
                    expression=lambda x, y: 子机组模型.BinVarMultiplySingle(子机组是否购买, x) == y,
                )

                if self.计算参数.计算步长 == "秒":
                    # deltalimit
                    subModelElectricityPowerDeltaLimit = (
                        self.RatedPower * self.PowerDeltaLimit / 100
                    )

                    子机组模型.CustomRangeConstraintMulti(
                        子机组电输出,
                        子机组是否真的开启,
                        customRange=range(self.计算参数.迭代步数),
                        expression=lambda x, y, i: x[i + 1] - x[i]
                        >= -subModelElectricityPowerDeltaLimit * y,
                    )
                    子机组模型.CustomRangeConstraintMulti(
                        子机组电输出,
                        子机组是否真的开启,
                        customRange=range(self.计算参数.迭代步数),
                        expression=lambda x, y, i: x[i + 1] - x[i]
                        <= subModelElectricityPowerDeltaLimit * y,
                    )

                子机组柴油输入求和 = 子机组模型.TimeSummation(子机组柴油输入求和, 子机组柴油输入)
                子机组电输出求和 = 子机组模型.TimeSummation(子机组电输出求和, 子机组电输出)
                子机组是否真的开启求和 = 子机组模型.TimeSummation(子机组是否真的开启求和, 子机组是否真的开启)

                子机组模型.Piecewise(
                    y_var=子机组柴油输入,
                    x_var=子机组电输出,
                    y_vals=[
                        -x[0] * self.RatedPower * x[1] for x in self.DieselToPower_Load
                    ],
                    x_vals=[self.RatedPower * x[1] for x in self.DieselToPower_Load],
                )
            子机组购买数目 = quicksum_indexed_var(self.子机组是否购买)
            self.mw.Constraint(expr=子机组购买数目 == self.DeviceCount)
            self.RangeConstraint(self.Nrun, 子机组是否真的开启求和, expression=lambda x, y: x == y)

            self.RangeConstraint(self.柴油输入, 子机组柴油输入求和, expression=lambda x, y: x == y)
            self.RangeConstraint(self.电输出, 子机组电输出求和, expression=lambda x, y: x == y)
        else:
            raise Exception(f"未知油耗规划算法：{self.设备信息.unitPlanningAlgorithmSelection}")

        if (
            self.计算参数.计算步长 == "秒"
            and self.设备信息.unitPlanningAlgorithmSelection != 油耗规划算法.最佳
        ):
            总最大功率 = self.RatedPower * self.DeviceCount
            最大功率变化 = 总最大功率 * self.PowerDeltaLimit / 100
            最大下行功率变化生成 = (
                lambda Nrun_t: Nrun_t * self.RatedPower * self.PowerDeltaLimit / 100
            )
            self.CustomRangeConstraintMulti(
                self.电输出,
                customRange=range(self.计算参数.迭代步数 - 1),
                expression=lambda x, i: x[i + 1] - x[i] <= 最大功率变化,
            )
            self.CustomRangeConstraintMulti(
                self.电输出,
                self.Nrun,
                customRange=range(self.计算参数.迭代步数 - 1),
                expression=lambda x, y, i: x[i + 1] - x[i] >= -最大下行功率变化生成(y[i]),
            )

        # 计算年化
        # unit: one
        Life = self.Life
        self.年化率 = 计算年化率(self.计算参数.贴现率, Life)

        self.总采购成本 = self.CostPerMachine * (self.DeviceCount)
        self.总固定维护成本 = self.CostPerYearPerMachine * (self.DeviceCount)
        self.总建设费用 = self.BuildCostPerMachine * (self.DeviceCount) + self.BuildBaseCost

        self.总固定成本年化 = (self.总采购成本 + self.总建设费用) * self.年化率 + self.总固定维护成本

        self.总可变维护成本年化 = (
            ((self.SumRange(self.电输出)) / self.计算参数.迭代步数)
            * 每年小时数
            * self.VariationalCostPerWork
        )
        # avg_power * 8760 = annual_work
        self.总可变维护成本年化 += self.annualUnitStartupCosts

        self.总成本年化 = self.总固定成本年化 + self.总可变维护成本年化

        self.处理最终财务输出(self)

        return self.总成本年化


class 电解槽模型(设备模型):
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 电解槽ID, 设备信息: 电解槽信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        self.LHVHydrogen = self.设备信息.toStandard("LHVHydrogen")
        self.StartupCountLimit = self.设备信息.StartupCountLimit
        self.HasStartupCountLimit = self.StartupCountLimit is not None
        self.RatedInputPower: float = 设备信息.RatedInputPower
        """
        名称: 额定输入功率
        单位: kW
        """
        assert self.RatedInputPower >= 0

        self.HydrogenGenerationStartupRate: float = (
            设备信息.HydrogenGenerationStartupRate * 0.01
        )
        """
        名称: 制氢启动功率比值
        单位: one <- percent
        """
        assert self.HydrogenGenerationStartupRate >= 0

        self.HydrogenGenerationEfficiency: float = (
            设备信息.HydrogenGenerationEfficiency * 0.01
        )
        """
        名称: 制氢效率
        单位: one <- percent
        """
        assert self.HydrogenGenerationEfficiency >= 0

        self.DeltaLimit: float = 设备信息.DeltaLimit
        """
        名称: 爬坡率
        单位: percent/s
        """
        assert self.DeltaLimit >= 0

        self.HeatRecycleEfficiency: float = 设备信息.HeatRecycleEfficiency * 0.01
        """
        名称: 热量回收效率
        单位: one <- percent
        """
        assert self.HeatRecycleEfficiency >= 0

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
            # BUG: if unbounded, then we get some error.
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

        self.PD[self.设备ID.设备余热接口] = self.ports["设备余热接口"] = self.设备余热接口 = self.变量列表(
            "设备余热接口", within=NonNegativeReals
        )
        """
        类型: 输出
        """

        self.PD[self.设备ID.制氢接口] = self.ports["制氢接口"] = self.制氢接口 = self.变量列表(
            "制氢接口", within=NonNegativeReals
        )
        """
        类型: 输出
        """

        self.PD[self.设备ID.电接口] = self.ports["电接口"] = self.电接口 = self.变量列表(
            "电接口", within=NonPositiveReals
        )
        """
        类型: 输入
        """

        # 设备特有约束（变量）

        self.Nrun_indicators = self.变量列表_带指示变量("Nrun_indicators")
        self.机组年运行时间 = (
            quicksum_indexed_var(self.Nrun_indicators.b_pos) / self.计算参数.迭代步数
        ) * 8760

        self.RangeConstraint(
            self.电接口,
            self.Nrun_indicators.x,
            expression=lambda x, y: -(
                x + self.RatedInputPower * self.HydrogenGenerationStartupRate
            )
            - self.EPS
            == y,
        )
        self.机组年启动次数 = 0

        self.POSNEG_是否购买 = self.单表达式生成指示变量("POSNEG_是否购买", self.DeviceCount - 0.5)
        self.是否购买 = self.POSNEG_是否购买.b_pos

        if isinstance(self.DeviceCount, Var):  # 设备台数约束
            self.DeviceCount.setlb(self.MinDeviceCount)
            self.DeviceCount.setub(self.MaxDeviceCount)

    def constraints_register(self):
        super().constraints_register()
        # 设备特有约束（非变量）

        # 输出输入功率约束

        self.RangeConstraintMulti(
            self.电接口, expression=lambda x: -x <= self.DeviceCount * self.RatedInputPower
        )

        self.DisjunctiveRangeConstraintMulti(
            self.电接口,
            expression=lambda x: [
                [x == 0],
                [-x >= self.RatedInputPower * self.HydrogenGenerationStartupRate],
            ],
        )

        self.RangeConstraint(
            self.电接口,
            self.制氢接口,
            expression=lambda x, y: y
            == -(x * self.HydrogenGenerationEfficiency) / self.LHVHydrogen,
        )

        self.RangeConstraint(
            self.电接口,
            self.设备余热接口,
            expression=lambda x, y: y
            == -(x * (1 - self.HydrogenGenerationEfficiency))
            * self.HeatRecycleEfficiency,
        )

        启动指示变量 = self.变量列表_带指示变量("启动指示变量")
        self.__setattr__("启动指示变量", 启动指示变量)
        self.mw.Constraint(
            expr=启动指示变量.x[self.计算参数.迭代步数 - 1] == self.Nrun_indicators.x_pos[0]
        )
        self.CustomRangeConstraintMulti(
            self.Nrun_indicators.x_pos,
            启动指示变量.x,
            expression=lambda x, y, i: (x[i + 1] - x[i]) - 0.5 == y[i],
            customRange=range(self.计算参数.迭代步数 - 1),
        )

        self.机组年启动次数 = quicksum_indexed_var(self.启动指示变量.x_pos) * (
            8760 / self.计算参数.总计算时长
        )

        if self.HasStartupCountLimit:
            # differentiation?
            startupCount = self.SumRange(启动指示变量.x_pos)
            self.mw.Constraint(expr=startupCount < self.StartupCountLimit)

        if self.计算参数.计算步长 == "秒":
            # TODO: 如果位于启动或者关闭时刻 自动去掉限制
            deltaLimit = (
                self.DeviceCount * self.RatedInputPower * self.设备信息.DeltaLimit / 100
            )
            self.CustomRangeConstraintMulti(
                self.电接口,
                expression=lambda x, i: (x[i + 1] - x[i]) >= deltaLimit,
                customRange=range(self.计算参数.迭代步数 - 1),
            )
            self.CustomRangeConstraintMulti(
                self.电接口,
                expression=lambda x, i: (x[i + 1] - x[i]) <= deltaLimit,
                customRange=range(self.计算参数.迭代步数 - 1),
            )

        # 计算年化
        # unit: one
        Life = self.Life
        self.年化率 = 计算年化率(self.计算参数.贴现率, Life)

        self.总采购成本 = self.CostPerMachine * (self.DeviceCount)
        self.总固定维护成本 = self.CostPerYearPerMachine * (self.DeviceCount)
        self.总建设费用 = self.BuildCostPerMachine * (self.DeviceCount) + self.BuildBaseCost

        self.总固定成本年化 = (self.总采购成本 + self.总建设费用) * self.年化率 + self.总固定维护成本

        self.总可变维护成本年化 = (
            ((-self.SumRange(self.电接口)) / self.计算参数.迭代步数)
            * 每年小时数
            * self.VariationalCostPerWork
        )
        # avg_power * 8760 = annual_work

        self.总成本年化 = self.总固定成本年化 + self.总可变维护成本年化

        self.处理最终财务输出(self)

        return self.总成本年化


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

        self.LifetimeCycleCount: float = 设备信息.LifetimeCycleCount
        """
        名称: 等效完全循环次数
        单位: 次
        """
        assert self.LifetimeCycleCount >= 0

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
            # BUG: if unbounded, then we get some error.
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
            self.DeviceCount = round(
                self.设备信息.TotalCapacity / self.设备信息.RatedCapacity
            )  # for better user experience.
            self.InitSOC: float = 设备信息.InitSOC * 0.01
            """
            名称: 初始SOC
            单位: one <- percent
            """
            assert self.InitSOC >= 0

            self.TotalCapacity: float = 设备信息.TotalCapacity
            """
            名称: 设备容量
            单位: kWh
            """
            assert self.TotalCapacity >= 0

        ##### PORT VARIABLE DEFINITION ####

        self.ports = {}

        self.PD[self.设备ID.电接口] = self.ports["电接口"] = self.电接口 = self.变量列表(
            "电接口", within=Reals
        )
        """
        类型: 输入输出
        """

        # 设备特有约束（变量）

        assert self.InitSOC >= self.MinSOC
        assert self.InitSOC <= self.MaxSOC
        self.InitCapacityPerUnit = self.InitSOC * self.RatedCapacity

        if self.计算参数.计算类型 == "设计规划":
            #  初始SOC
            self.MaxDeviceCount = math.floor(self.MaxTotalCapacity / self.RatedCapacity)
            self.MinDeviceCount = math.ceil(self.MinTotalCapacity / self.RatedCapacity)

            self.TotalCapacity = self.DeviceCount * self.RatedCapacity  # type: ignore

        assert self.MaxSOC >= self.MinSOC
        assert self.MaxSOC <= 1
        assert self.MinSOC >= 0

        self.原电接口 = self.变量列表_带指示变量("原电接口")  # 正 放电 负 充电

        self.CurrentTotalCapacity = self.变量列表(
            "CurrentTotalCapacity", within=NonNegativeReals
        )

        # reserved expression list. do not use it in any constraints.
        self.SOC = [
            self.CurrentTotalCapacity[i] / self.TotalCapacity
            for i in self.CurrentTotalCapacity
        ]

        self.RangeConstraintMulti(
            self.CurrentTotalCapacity,
            expression=lambda x: x >= self.TotalCapacity * self.MinSOC,
        )
        self.RangeConstraintMulti(
            self.CurrentTotalCapacity,
            expression=lambda x: x <= self.TotalCapacity * self.MaxSOC,
        )

        self.MaxTotalChargeOrDischargeRate = self.BatteryDeltaLimit * self.TotalCapacity
        """
        最大总充放功率
        单位: kW
        """

        self.sigma = self.BatteryStorageDecay / 100
        """
        衰减率
        单位: 1/h
        """

        self.POSNEG_是否购买 = self.单表达式生成指示变量("POSNEG_是否购买", self.DeviceCount - 0.5)
        self.是否购买 = self.POSNEG_是否购买.b_pos

        if isinstance(self.DeviceCount, Var):  # 设备台数约束
            self.DeviceCount.setlb(self.MinDeviceCount)
            self.DeviceCount.setub(self.MaxDeviceCount)

    def constraints_register(self):
        super().constraints_register()
        # 设备特有约束（非变量）

        # 输出输入功率约束

        self.mw.Constraint(
            self.CurrentTotalCapacity[0] == self.InitCapacityPerUnit * self.DeviceCount
        )

        self.CustomRangeConstraintMulti(
            self.原电接口.x,
            self.CurrentTotalCapacity,
            customRange=range(self.计算参数.迭代步数 - 1),
            expression=lambda x, y, i: x[i] * self.计算参数.deltaT
            == (y[i] * (1 - self.计算参数.deltaT * self.sigma) - y[i + 1]),
        )
        self.RangeConstraintMulti(
            self.原电接口.x_pos,
            self.原电接口.x_neg,
            self.电接口,
            expression=lambda x_pos, x_neg, y: x_pos * self.DischargeEfficiency
            - (x_neg) / self.ChargeEfficiency
            == y,
        )
        self.RangeConstraintMulti(
            self.原电接口.x_abs,
            expression=lambda x: x <= self.MaxTotalChargeOrDischargeRate,
        )

        if self.计算参数.典型日:
            self.mw.Constraint(
                self.CurrentTotalCapacity[self.计算参数.迭代步数 - 1]
                == self.CurrentTotalCapacity[0]
            )

        # 计算年化
        # unit: one

        # TODO: to get LifetimeDischargeCapacityPerUnit working
        self.LifetimeDischargeCapacityPerUnit = (
            self.LifetimeCycleCount * self.RatedCapacity
        )
        """
        单块电池生命周期总放电量
        单位: kWh
        """

        计算范围内总平均放电功率 = self.SumRange(self.原电接口.x_pos) / self.计算参数.迭代步数  # kW
        # avg power

        一小时总电变化量 = 计算范围内总平均放电功率  # 省略乘1
        # kWh

        一年总电变化量 = 一小时总电变化量 * 每年小时数

        self.mw.Constraint(
            一年总电变化量 * self.BatteryLife
            <= self.DeviceCount * self.LifetimeDischargeCapacityPerUnit * 0.85
        )
        assert self.BatteryLife >= 1
        assert self.Life >= self.BatteryLife
        Life = self.BatteryLife
        self.年化率 = 计算年化率(self.计算参数.贴现率, Life)

        self.总采购成本 = self.CostPerCapacity * (self.DeviceCount * self.RatedCapacity)
        self.总固定维护成本 = self.CostPerYearPerCapacity * (
            self.DeviceCount * self.RatedCapacity
        )
        self.总建设费用 = (
            self.BuildCostPerCapacity * (self.DeviceCount * self.RatedCapacity)
            + self.BuildBaseCost
        )

        self.总固定成本年化 = (self.总采购成本 + self.总建设费用) * self.年化率 + self.总固定维护成本

        self.总可变维护成本年化 = (
            ((计算范围内总平均放电功率 * self.计算参数.迭代步数) / self.计算参数.迭代步数)
            * 每年小时数
            * self.VariationalCostPerWork
        )
        # avg_power * 8760 = annual_work

        self.总成本年化 = self.总固定成本年化 + self.总可变维护成本年化

        self.处理最终财务输出(self)

        return self.总成本年化


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
            # BUG: if unbounded, then we get some error.
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

        self.PD[self.设备ID.电输入] = self.ports["电输入"] = self.电输入 = self.变量列表(
            "电输入", within=Reals
        )
        """
        类型: 输入
        """

        self.PD[self.设备ID.电输出] = self.ports["电输出"] = self.电输出 = self.变量列表(
            "电输出", within=Reals
        )
        """
        类型: 输出
        """

        # 设备特有约束（变量）

        self.PowerInput_ = self.变量列表_带指示变量("PowerInput_")
        self.PowerOutput_ = self.变量列表_带指示变量("PowerOutput_")

        self.RangeConstraint(
            self.电输入, self.PowerInput_.x, expression=lambda x, y: x == y
        )
        self.RangeConstraint(
            self.电输出, self.PowerOutput_.x, expression=lambda x, y: x == y
        )

        self.RangeConstraint(
            self.PowerInput_.b_pos,
            self.PowerOutput_.b_pos,
            expression=lambda x, y: x + y <= 1,
        )
        self.RangeConstraint(
            self.PowerInput_.b_neg,
            self.PowerOutput_.b_neg,
            expression=lambda x, y: x + y <= 1,
        )

        if self.设备信息.direction == Direction.Directed:
            self.RangeConstraintMulti(
                self.PowerInput_.x_pos, expression=lambda x: x == 0
            )
            self.RangeConstraintMulti(
                self.PowerOutput_.x_neg, expression=lambda x: x == 0
            )

        if self.计算参数.计算类型 == "设计规划":  # 在变压器和负荷的交换节点处做处理
            self.最大允许的负载总功率 = self.DeviceCount * (self.RatedPower * self.Efficiency) * self.PowerParameter / (1 if 0 == self.LoadRedundancyParameter else self.LoadRedundancyParameter)  # type: ignore

        self.POSNEG_是否购买 = self.单表达式生成指示变量("POSNEG_是否购买", self.DeviceCount - 0.5)
        self.是否购买 = self.POSNEG_是否购买.b_pos

        if isinstance(self.DeviceCount, Var):  # 设备台数约束
            self.DeviceCount.setlb(self.MinDeviceCount)
            self.DeviceCount.setub(self.MaxDeviceCount)

    def constraints_register(self):
        super().constraints_register()
        # 设备特有约束（非变量）

        # 输出输入功率约束
        # TODO: figure out what "PowerParameter" does
        # TODO: fix efficiency issue
        self.RangeConstraint(
            self.PowerInput_.x_neg,
            self.PowerOutput_.x_pos,
            lambda x, y: x * self.Efficiency * self.PowerParameter == y,
        )
        self.RangeConstraint(
            self.PowerOutput_.x_neg,
            self.PowerInput_.x_pos,
            lambda x, y: x * self.Efficiency * self.PowerParameter == y,
        )

        self.RangeConstraintMulti(
            self.PowerInput_.x_neg,
            expression=lambda x: x <= self.RatedPower * self.DeviceCount,
        )
        self.RangeConstraintMulti(
            self.PowerOutput_.x_neg,
            expression=lambda x: x <= self.RatedPower * self.DeviceCount,
        )

        # 计算年化
        # unit: one
        Life = self.Life
        self.年化率 = 计算年化率(self.计算参数.贴现率, Life)

        self.总采购成本 = self.CostPerKilowatt * (self.DeviceCount * self.RatedPower)
        self.总固定维护成本 = self.CostPerYearPerKilowatt * (
            self.DeviceCount * self.RatedPower
        )
        self.总建设费用 = (
            self.BuildCostPerKilowatt * (self.DeviceCount * self.RatedPower)
            + self.BuildBaseCost
        )

        self.总固定成本年化 = (self.总采购成本 + self.总建设费用) * self.年化率 + self.总固定维护成本

        self.总可变维护成本年化 = (
            (
                (
                    (
                        self.SumRange(self.PowerInput_.x_neg)
                        + self.SumRange(self.PowerOutput_.x_neg)
                    )
                )
                / self.计算参数.迭代步数
            )
            * 每年小时数
            * self.VariationalCostPerWork
        )
        # avg_power * 8760 = annual_work

        self.总成本年化 = self.总固定成本年化 + self.总可变维护成本年化

        self.处理最终财务输出(self)

        return self.总成本年化


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
            # BUG: if unbounded, then we get some error.
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
            "电输入", within=NonPositiveReals
        )
        """
        类型: 输入
        """

        self.PD[self.设备ID.电输出] = self.ports["电输出"] = self.电输出 = self.变量列表(
            "电输出", within=NonNegativeReals
        )
        """
        类型: 输出
        """

        # 设备特有约束（变量）

        self.POSNEG_是否购买 = self.单表达式生成指示变量("POSNEG_是否购买", self.DeviceCount - 0.5)
        self.是否购买 = self.POSNEG_是否购买.b_pos

        if isinstance(self.DeviceCount, Var):  # 设备台数约束
            self.DeviceCount.setlb(self.MinDeviceCount)
            self.DeviceCount.setub(self.MaxDeviceCount)

    def constraints_register(self):
        super().constraints_register()
        # 设备特有约束（非变量）

        # 输出输入功率约束
        # TODO: figure out what "PowerParameter" does
        # TODO: fix efficiency issue
        self.RangeConstraint(self.电输入, self.电输出, lambda x, y: x * self.Efficiency == -y)
        self.RangeConstraintMulti(
            self.电输入, expression=lambda x: -x <= self.RatedPower * self.DeviceCount
        )

        # 计算年化
        # unit: one
        Life = self.Life
        self.年化率 = 计算年化率(self.计算参数.贴现率, Life)

        self.总采购成本 = self.CostPerKilowatt * (self.DeviceCount * self.RatedPower)
        self.总固定维护成本 = self.CostPerYearPerKilowatt * (
            self.DeviceCount * self.RatedPower
        )
        self.总建设费用 = (
            self.BuildCostPerKilowatt * (self.DeviceCount * self.RatedPower)
            + self.BuildBaseCost
        )

        self.总固定成本年化 = (self.总采购成本 + self.总建设费用) * self.年化率 + self.总固定维护成本

        self.总可变维护成本年化 = (
            ((-self.SumRange(self.电输入)) / self.计算参数.迭代步数)
            * 每年小时数
            * self.VariationalCostPerWork
        )
        # avg_power * 8760 = annual_work

        self.总成本年化 = self.总固定成本年化 + self.总可变维护成本年化

        self.处理最终财务输出(self)

        return self.总成本年化


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
            # BUG: if unbounded, then we get some error.
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
        类型: 输入输出
        """

        self.PD[self.设备ID.储能端] = self.ports["储能端"] = self.储能端 = self.变量列表(
            "储能端", within=Reals
        )
        """
        类型: 输入输出
        """

        # 设备特有约束（变量）

        self.线路端_ = self.变量列表_带指示变量("线路端_")
        self.储能端_ = self.变量列表_带指示变量("储能端_")

        self.POSNEG_是否购买 = self.单表达式生成指示变量("POSNEG_是否购买", self.DeviceCount - 0.5)
        self.是否购买 = self.POSNEG_是否购买.b_pos

        if isinstance(self.DeviceCount, Var):  # 设备台数约束
            self.DeviceCount.setlb(self.MinDeviceCount)
            self.DeviceCount.setub(self.MaxDeviceCount)

    def constraints_register(self):
        super().constraints_register()
        # 设备特有约束（非变量）

        # 输出输入功率约束

        self.RangeConstraint(self.线路端_.x, self.线路端, lambda x, y: x == y)
        self.RangeConstraint(self.储能端_.x, self.储能端, lambda x, y: x == y)

        self.DisjunctiveRangeConstraint(
            self.线路端,
            self.储能端,
            expression=lambda x, y: [
                [x >= 0, y <= 0, x == -y * self.Efficiency],
                [x <= 0, y >= 0, x * self.Efficiency == -y],
            ],
        )

        # wrong! negative is input.

        # 计算年化
        # unit: one
        Life = self.Life
        self.年化率 = 计算年化率(self.计算参数.贴现率, Life)

        self.总采购成本 = self.CostPerKilowatt * (self.DeviceCount * self.RatedPower)
        self.总固定维护成本 = self.CostPerYearPerKilowatt * (
            self.DeviceCount * self.RatedPower
        )
        self.总建设费用 = (
            self.BuildCostPerKilowatt * (self.DeviceCount * self.RatedPower)
            + self.BuildBaseCost
        )

        self.总固定成本年化 = (self.总采购成本 + self.总建设费用) * self.年化率 + self.总固定维护成本

        self.总可变维护成本年化 = (
            (
                ((self.SumRange(self.储能端_.x_neg) + self.SumRange(self.线路端_.x_neg)))
                / self.计算参数.迭代步数
            )
            * 每年小时数
            * self.VariationalCostPerWork
        )
        # avg_power * 8760 = annual_work

        self.总成本年化 = self.总固定成本年化 + self.总可变维护成本年化

        self.处理最终财务输出(self)

        return self.总成本年化


class 传输线模型(设备模型):
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 传输线ID, 设备信息: 传输线信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        # params added later
        self.U = self.设备信息.toStandard("U")
        self.Rho = self.设备信息.toStandard("Rho")
        self.GivenAveragePower = self.设备信息.toStandard("GivenAveragePower")
        self.GivenMaxPower = self.设备信息.toStandard("GivenMaxPower")
        self.Pwire_Asec_Pr = self.设备信息.toStandard("Pwire_Asec_Pr")
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
            # BUG: if unbounded, then we get some error.
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
            "电输出", within=Reals
        )
        """
        类型: 输入输出
        """

        self.PD[self.设备ID.电输入] = self.ports["电输入"] = self.电输入 = self.变量列表(
            "电输入", within=Reals
        )
        """
        类型: 输入输出
        """

        # 设备特有约束（变量）

        self.PowerInput_ = self.变量列表_带指示变量("PowerInput_")
        self.PowerOutput_ = self.变量列表_带指示变量("PowerOutput_")

        self.RangeConstraint(
            self.电输入, self.PowerInput_.x, expression=lambda x, y: x == y
        )
        self.RangeConstraint(
            self.电输出, self.PowerOutput_.x, expression=lambda x, y: x == y
        )

        self.RangeConstraint(
            self.PowerInput_.b_pos,
            self.PowerOutput_.b_pos,
            expression=lambda x, y: x + y <= 1,
        )
        self.RangeConstraint(
            self.PowerInput_.b_neg,
            self.PowerOutput_.b_neg,
            expression=lambda x, y: x + y <= 1,
        )

        # TODO: use Disjunction instead of Piecewise
        self.Pwire_Asec_Pr.sort(key=lambda x: x[0])
        self.Pwire_arr = [e[0] for e in self.Pwire_Asec_Pr]
        self.Asec_arr = [e[1] for e in self.Pwire_Asec_Pr]
        self.Pr_arr = [e[2] for e in self.Pwire_Asec_Pr]

        if self.设备信息.Optimize:
            self.Pwire = self.单变量("Pwire", within=NonNegativeReals)

            self.RangeConstraintMulti(
                self.PowerInput_.x_neg,
                self.PowerOutput_.x_neg,
                expression=lambda x, y: x + y <= self.Pwire,
            )

            self.Asec = self.单变量("Asec", within=NonNegativeReals)
            self.Asec_inv = self.单变量("Asec_inv", within=NonNegativeReals)

            self.DisjunctivePair(
                x_var=self.Pwire,
                y_var=self.Asec,
                x_vals=self.Pwire_arr,
                y_vals=self.Asec_arr,
            )
            self.DisjunctivePair(
                x_var=self.Pwire,
                y_var=self.Asec_inv,
                x_vals=self.Pwire_arr,
                y_vals=[1 / e for e in self.Asec_arr],
            )

            self.Pr = self.单变量("Pr", within=NonNegativeReals)

            self.DisjunctivePair(
                x_var=self.Pwire,
                y_var=self.Pr,
                x_vals=self.Pwire_arr,
                y_vals=self.Pr_arr,
            )
        else:
            self.Pwire = self.GivenMaxPower
            ind = -1
            dis = -1
            for _ind, val in enumerate(self.Pwire_arr):
                _dis = val - self.GivenMaxPower
                if _dis >= 0:
                    if dis < 0 or dis > _dis:
                        dis = _dis
                        ind = _ind
            if ind == -1:
                raise Exception(
                    f"No valid Pwire found!\nGivenMaxPower: {self.GivenMaxPower}\nPwire_arr: {self.Pwire_arr}"
                )
            else:
                self.Pwire = self.Pwire_arr[ind]
                self.Asec = self.Asec_arr[ind]
                self.Asec_inv = 1 / self.Asec
                self.Pr = self.Pr_arr[ind]
        self.R = (self.Rho * self.Length) * self.Asec_inv
        """
        传输线电阻
        """
        self.Ploss = self.R * ((self.GivenAveragePower / self.U) ** 2)

        # unit please?
        # overriding passed parameters.
        # let's preserve this.
        self.CostPerKilometer = self.Pr

        self.inputIndicators = self.变量列表_带指示变量("inputIndicators")
        self.outputIndicators = self.变量列表_带指示变量("outputIndicators")

    def constraints_register(self):
        super().constraints_register()
        # 设备特有约束（非变量）

        # 输出输入功率约束

        self.RangeConstraint(
            self.电输入,
            self.inputIndicators.x,
            expression=lambda x, y: x == y - self.Ploss,
        )

        self.RangeConstraint(
            self.电输出,
            self.outputIndicators.x,
            expression=lambda x, y: x == y - self.Ploss,
        )

        self.RangeConstraintMulti(
            self.PowerOutput_.x_pos,
            self.inputIndicators.x_neg,
            expression=lambda x, y: x == y,
        )
        self.RangeConstraintMulti(
            self.PowerInput_.x_pos,
            self.outputIndicators.x_neg,
            expression=lambda x, y: x == y,
        )

        self.RangeConstraint(
            self.PowerInput_.b_pos,
            self.PowerOutput_.b_pos,
            expression=lambda x, y: x + y <= 1,
        )
        self.RangeConstraint(
            self.PowerInput_.b_neg,
            self.PowerOutput_.b_neg,
            expression=lambda x, y: x + y <= 1,
        )

        # 计算年化
        # unit: one
        Life = self.Life
        self.年化率 = 计算年化率(self.计算参数.贴现率, Life)

        self.总采购成本 = self.CostPerKilometer * (self.Length)
        self.总固定维护成本 = self.CostPerYearPerKilometer * (self.Length)
        self.总建设费用 = self.BuildCostPerKilometer * (self.Length) + self.BuildBaseCost

        self.总固定成本年化 = (self.总采购成本 + self.总建设费用) * self.年化率 + self.总固定维护成本

        self.总成本年化 = self.总固定成本年化

        return self.总成本年化


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
            "电接口", within=NonPositiveReals
        )
        """
        类型: 输入
        """

        assert len(self.设备信息.EnergyConsumption) == self.计算参数.迭代步数
        self.Pmin = self.设备信息.toStandard("Pmin")
        self.Pmax = self.设备信息.toStandard("Pmax")
        self.PunishmentRate = self.设备信息.toStandard("PunishmentRate")
        self.EnergyConsumption = self.设备信息.toStandard("EnergyConsumption")
        # deal with MaxEnergyConsumption & PriceModel separately

        if self.设备信息.LoadType == 负荷类型.Punished:
            self.UnsatisfiedEnergyConsumption = self.变量列表(
                "UnsatisfiedEnergyConsumption", within=NonNegativeReals
            )

        if 负荷类型.Interruptable in self.设备信息.LoadType:
            self.Interrupted = self.变量列表("Interrupted", within=Boolean)
            # Binary is ok.

        MaxEnergyConsumptionDefault = max(self.EnergyConsumption)

        if self.设备信息.MaxEnergyConsumption is None:
            self.MaxEnergyConsumption = MaxEnergyConsumptionDefault
        else:
            assert self.设备信息.MaxEnergyConsumption >= MaxEnergyConsumptionDefault
            self.MaxEnergyConsumption = self.设备信息.toStandard("MaxEnergyConsumption")

        self.IncomeRates = ...
        self.punishRate = 0
        self.PriceModel = self.设备信息.PriceModel

    def constraints_register(self):
        super().constraints_register()
        # TODO: 典型日的分时分月电价取每天同一小时的平均，在电价模型内实现
        getTimeInDay = (
            lambda index: index
            if self.计算参数.计算步长 == "小时"
            else self.计算参数.分时计价开始时间点
            + 每天小时数 * convertMonthToDays(self.计算参数.分时计价开始月份)
            + (index / 每小时秒数)
        )

        self.IncomeRates = [
            self.PriceModel.getFee(power, getTimeInDay(index))
            for index, power in enumerate(self.电接口.values())
        ]  # negative, means income
        punishmentRates = [0]

        if self.设备信息.LoadType == 负荷类型.Normal:
            self.RangeConstraint(self.电接口, self.EnergyConsumption, lambda x, y: x == -y)
        elif self.设备信息.LoadType == 负荷类型.Punished:
            self.RangeConstraintMulti(
                self.电接口,
                self.UnsatisfiedEnergyConsumption,
                self.EnergyConsumption,
                expression=lambda x, y, z: x == -(z - y),
            )
            punishmentRates = [
                v * self.PunishmentRate
                for v in self.UnsatisfiedEnergyConsumption.values()
            ]
        elif self.设备信息.LoadType == 负荷类型.Flexible:
            self.RangeConstraintMulti(self.电接口, expression=lambda x: -x >= self.Pmin)
            self.RangeConstraintMulti(self.电接口, expression=lambda x: -x <= self.Pmax)
        elif self.设备信息.LoadType == 负荷类型.Interruptable:
            self.RangeConstraintMulti(
                self.电接口,
                self.Interrupted,
                expression=lambda x, y: -x == self.Pmax * (1 - y),
            )
        elif self.设备信息.LoadType == 负荷类型.InterruptableAndFlexible:
            self.RangeConstraintMulti(
                self.电接口,
                self.Interrupted,
                expression=lambda x, y: -x >= self.Pmin * (1 - y),
            )
            self.RangeConstraintMulti(
                self.电接口,
                self.Interrupted,
                expression=lambda x, y: -x <= self.Pmax * (1 - y),
            )
        else:
            raise Exception("不合理的负荷类型:", self.设备信息.LoadType)

        if self.设备信息.LoadType == 负荷类型.Punished:
            年化费用 = 0
            self.punishRate = quicksum_indexed_var(punishmentRates) / self.计算参数.迭代步数
        else:
            年化费用 = (quicksum_indexed_var(self.IncomeRates) / self.计算参数.迭代步数) * 每年小时数
        # 已经是负数了

        self.总成本年化 = self.总可变维护成本年化 = 年化费用
        return 年化费用


class 氢负荷模型(设备模型):
    def __init__(
        self, PD: dict, mw: ModelWrapper, 计算参数实例: 计算参数, 设备ID: 氢负荷ID, 设备信息: 氢负荷信息
    ):
        super().__init__(PD=PD, mw=mw, 计算参数实例=计算参数实例, ID=设备ID.ID)
        self.设备ID = 设备ID
        self.设备信息 = 设备信息

        ##### PORT VARIABLE DEFINITION ####

        self.ports = {}

        self.PD[self.设备ID.氢气接口] = self.ports["氢气接口"] = self.氢气接口 = self.变量列表(
            "氢气接口", within=NonPositiveReals
        )
        """
        类型: 输入
        """

        assert len(self.设备信息.EnergyConsumption) == self.计算参数.迭代步数
        self.Pmin = self.设备信息.toStandard("Pmin")
        self.Pmax = self.设备信息.toStandard("Pmax")
        self.PunishmentRate = self.设备信息.toStandard("PunishmentRate")
        self.EnergyConsumption = self.设备信息.toStandard("EnergyConsumption")
        # deal with MaxEnergyConsumption & PriceModel separately

        if self.设备信息.LoadType == 负荷类型.Punished:
            self.UnsatisfiedEnergyConsumption = self.变量列表(
                "UnsatisfiedEnergyConsumption", within=NonNegativeReals
            )

        if 负荷类型.Interruptable in self.设备信息.LoadType:
            self.Interrupted = self.变量列表("Interrupted", within=Boolean)
            # Binary is ok.

        self.IncomeRates = ...
        self.punishRate = 0
        self.PriceModel = self.设备信息.PriceModel

    def constraints_register(self):
        super().constraints_register()
        # TODO: 典型日的分时分月电价取每天同一小时的平均，在电价模型内实现
        getTimeInDay = (
            lambda index: index
            if self.计算参数.计算步长 == "小时"
            else self.计算参数.分时计价开始时间点
            + 每天小时数 * convertMonthToDays(self.计算参数.分时计价开始月份)
            + (index / 每小时秒数)
        )

        self.IncomeRates = [
            self.PriceModel.getFee(power, getTimeInDay(index))
            for index, power in enumerate(self.氢气接口.values())
        ]  # negative, means income
        punishmentRates = [0]

        if self.设备信息.LoadType == 负荷类型.Normal:
            self.RangeConstraint(
                self.氢气接口, self.EnergyConsumption, lambda x, y: x == -y
            )
        elif self.设备信息.LoadType == 负荷类型.Punished:
            self.RangeConstraintMulti(
                self.氢气接口,
                self.UnsatisfiedEnergyConsumption,
                self.EnergyConsumption,
                expression=lambda x, y, z: x == -(z - y),
            )
            punishmentRates = [
                v * self.PunishmentRate
                for v in self.UnsatisfiedEnergyConsumption.values()
            ]
        elif self.设备信息.LoadType == 负荷类型.Flexible:
            self.RangeConstraintMulti(self.氢气接口, expression=lambda x: -x >= self.Pmin)
            self.RangeConstraintMulti(self.氢气接口, expression=lambda x: -x <= self.Pmax)
        elif self.设备信息.LoadType == 负荷类型.Interruptable:
            self.RangeConstraintMulti(
                self.氢气接口,
                self.Interrupted,
                expression=lambda x, y: -x == self.Pmax * (1 - y),
            )
        elif self.设备信息.LoadType == 负荷类型.InterruptableAndFlexible:
            self.RangeConstraintMulti(
                self.氢气接口,
                self.Interrupted,
                expression=lambda x, y: -x >= self.Pmin * (1 - y),
            )
            self.RangeConstraintMulti(
                self.氢气接口,
                self.Interrupted,
                expression=lambda x, y: -x <= self.Pmax * (1 - y),
            )
        else:
            raise Exception("不合理的负荷类型:", self.设备信息.LoadType)

        if self.设备信息.LoadType == 负荷类型.Punished:
            年化费用 = 0
            self.punishRate = quicksum_indexed_var(punishmentRates) / self.计算参数.迭代步数
        else:
            年化费用 = (quicksum_indexed_var(self.IncomeRates) / self.计算参数.迭代步数) * 每年小时数
        # 已经是负数了

        self.总成本年化 = self.总可变维护成本年化 = 年化费用
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
        类型: 输出
        """

        class _Units(BaseModel):
            Price: str
            热值: str
            CO2: str
            NOX: str
            SO2: str

        UnitsDict = {}

        ## PROCESSING: Price
        ### UNIT COMPATIBILITY CHECK ###
        default_unit = self.设备信息.DefaultUnits.Price
        val_unit = self.设备信息.Price[1]

        has_exception, _ = getSingleUnitConverted(
            default_unit=default_unit, val_unit=val_unit
        )

        if has_exception:
            raise Exception(
                f"Unit '{val_unit}' is not compatible with default unit '{default_unit}'"
            )
        ### UNIT COMPATIBILITY CHECK ###

        ### UNIT CONVERSION ###
        ConversionRate, StandardUnit = unitFactorCalculator(
            ureg, standard_units, val_unit
        )
        ### UNIT CONVERSION ###

        self.Price = self.设备信息.Price[0] * ConversionRate
        """
        单位: 标准单位 <- 现用单位
        """
        UnitsDict.update(dict(Price=str(StandardUnit)))
        ## PROCESSING: 热值
        ### UNIT COMPATIBILITY CHECK ###
        default_unit = self.设备信息.DefaultUnits.热值
        val_unit = self.设备信息.热值[1]

        has_exception, _ = getSingleUnitConverted(
            default_unit=default_unit, val_unit=val_unit
        )

        if has_exception:
            raise Exception(
                f"Unit '{val_unit}' is not compatible with default unit '{default_unit}'"
            )
        ### UNIT COMPATIBILITY CHECK ###

        ### UNIT CONVERSION ###
        ConversionRate, StandardUnit = unitFactorCalculator(
            ureg, standard_units, val_unit
        )
        ### UNIT CONVERSION ###

        self.热值 = self.设备信息.热值[0] * ConversionRate
        """
        单位: 标准单位 <- 现用单位
        """
        UnitsDict.update(dict(热值=str(StandardUnit)))
        ## PROCESSING: CO2
        ### UNIT COMPATIBILITY CHECK ###
        default_unit = self.设备信息.DefaultUnits.CO2
        val_unit = self.设备信息.CO2[1]

        has_exception, _ = getSingleUnitConverted(
            default_unit=default_unit, val_unit=val_unit
        )

        if has_exception:
            raise Exception(
                f"Unit '{val_unit}' is not compatible with default unit '{default_unit}'"
            )
        ### UNIT COMPATIBILITY CHECK ###

        ### UNIT CONVERSION ###
        ConversionRate, StandardUnit = unitFactorCalculator(
            ureg, standard_units, val_unit
        )
        ### UNIT CONVERSION ###

        self.CO2 = self.设备信息.CO2[0] * ConversionRate
        """
        单位: 标准单位 <- 现用单位
        """
        UnitsDict.update(dict(CO2=str(StandardUnit)))
        ## PROCESSING: NOX
        ### UNIT COMPATIBILITY CHECK ###
        default_unit = self.设备信息.DefaultUnits.NOX
        val_unit = self.设备信息.NOX[1]

        has_exception, _ = getSingleUnitConverted(
            default_unit=default_unit, val_unit=val_unit
        )

        if has_exception:
            raise Exception(
                f"Unit '{val_unit}' is not compatible with default unit '{default_unit}'"
            )
        ### UNIT COMPATIBILITY CHECK ###

        ### UNIT CONVERSION ###
        ConversionRate, StandardUnit = unitFactorCalculator(
            ureg, standard_units, val_unit
        )
        ### UNIT CONVERSION ###

        self.NOX = self.设备信息.NOX[0] * ConversionRate
        """
        单位: 标准单位 <- 现用单位
        """
        UnitsDict.update(dict(NOX=str(StandardUnit)))
        ## PROCESSING: SO2
        ### UNIT COMPATIBILITY CHECK ###
        default_unit = self.设备信息.DefaultUnits.SO2
        val_unit = self.设备信息.SO2[1]

        has_exception, _ = getSingleUnitConverted(
            default_unit=default_unit, val_unit=val_unit
        )

        if has_exception:
            raise Exception(
                f"Unit '{val_unit}' is not compatible with default unit '{default_unit}'"
            )
        ### UNIT COMPATIBILITY CHECK ###

        ### UNIT CONVERSION ###
        ConversionRate, StandardUnit = unitFactorCalculator(
            ureg, standard_units, val_unit
        )
        ### UNIT CONVERSION ###

        self.SO2 = self.设备信息.SO2[0] * ConversionRate
        """
        单位: 标准单位 <- 现用单位
        """
        UnitsDict.update(dict(SO2=str(StandardUnit)))

        self.Units = _Units.parse_obj(UnitsDict)

    def constraints_register(self):
        super().constraints_register()
        平均消耗率 = self.SumRange(self.燃料接口) / self.计算参数.迭代步数

        年化费用 = 平均消耗率 * self.Price * 每年小时数

        self.总成本年化 = self.总可变维护成本年化 = 年化费用
        return 年化费用


class ModelWrapperContext:
    def __init__(self, inputParams: InputParams):
        mw = ModelWrapper()
        self.mw = mw
        self.mw.inputParams = deepcopy(inputParams)

    def __enter__(self):
        logger_print("ENTER MODEL WRAPPER CONTEXT")
        return self.mw

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # we don't have to take care of this.
        if exc_type == None:
            logger_print("NO ERROR IN MODEL WRAPPER CONTEXT")
        else:
            logger_print("ERROR IN MODEL WRAPPER CONTEXT")
        del self.mw
        logger_print("EXITING MODEL WRAPPER CONTEXT")


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
    "氢负荷": 氢负荷模型,
    "电解槽": 电解槽模型,
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
    "氢负荷": 氢负荷ID,
    "电解槽": 电解槽ID,
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
    "氢负荷": 氢负荷信息,
    "电解槽": 电解槽信息,
}  # type: ignore


def iterate_input_output_limit(attr, indexs, G, devInstDict):
    m_limit_list = []
    for m_id in indexs:
        m_anchor = G.nodes[m_id]
        m_node_id = m_anchor["device_id"]
        m_devInst = devInstDict[m_node_id]
        m_limit_list.append(getattr(m_devInst, attr))
    io_limit = sum(m_limit_list)
    return io_limit


# export all these data with no dependency on calculation type.


def getSchemaFromDataModel(dataModel: BaseModel):
    schema = dataModel.schema()
    return schema


def getRequiredKeysSetFromDataModel(dataModel: BaseModel):
    schema = getSchemaFromDataModel(dataModel)
    requiredKeys = schema["required"]
    return set(requiredKeys)


def getDuplicatedSchemaKeysSetFromDataModels(
    dataModel_0: BaseModel, dataModel_1: BaseModel
):
    requiredKeysSet_0 = getRequiredKeysSetFromDataModel(dataModel_0)
    requiredKeysSet_1 = getRequiredKeysSetFromDataModel(dataModel_1)
    duplicatedSchemaKeysSet = requiredKeysSet_0.intersection(requiredKeysSet_1)
    return duplicatedSchemaKeysSet


class 仿真结果(BaseModel):
    name: str = Field(title="元件名称")

    type: str = Field(title="元件类型")

    modelNumber: str = Field(title="设备型号")

    equiCounts: float = Field(title="设备台数")

    coolingCapacity: float = Field(title="产冷量")

    coolingLoad: float = Field(title="冷负荷")

    electricSupply: float = Field(title="产电量")

    electricLoad: float = Field(title="电负荷")

    heatingLoad: float = Field(title="产热量")

    heatLoad: float = Field(title="热负荷")

    steamProduction: float = Field(title="蒸汽产量")

    steamLoad: float = Field(title="蒸汽负荷")

    hydrogenProduction: float = Field(title="氢气产量")

    hydrogenConsumption: float = Field(title="氢气消耗量")

    dieselConsumption: float = Field(title="柴油消耗量")

    dieselConsumptionCosts: float = Field(title="柴油消耗费用")

    naturalGasConsumption: float = Field(title="天然气消耗量")

    naturalGasConsumptionCosts: float = Field(title="天然气消耗费用")

    averageEfficiency: float = Field(title="平均效率/平均COP")

    equipmentMaintenanceCosts: float = Field(title="设备维护费用")

    coldIncome: float = Field(title="冷收入")

    hotIncome: float = Field(title="热收入")

    eletricIncome: float = Field(title="电收入")

    steamIncome: float = Field(title="蒸汽收入")

    hydrogenIncome: float = Field(title="氢气收入")

    waterConsumption: float = Field(title="自来水消耗量")

    waterConsumptionCosts: float = Field(title="自来水消耗费用")


class 设备模型协议(Protocol):
    设备信息: 设备信息


class 规划结果详情_翻译(BaseModel):
    deviceName: str = Field(title="deviceName", description="对应字段: 元件名称")
    """
    对应字段: 元件名称
    """

    deviceModel: str = Field(title="deviceModel", description="对应字段: 型号")
    """
    对应字段: 型号
    """

    deviceCount: int = Field(title="deviceCount", description="对应字段: 数量")
    """
    对应字段: 数量
    """

    COP: float = Field(title="COP", description="对应字段: 平均效率_平均COP")
    """
    对应字段: 平均效率_平均COP
    """

    purchasingCost: float = Field(
        title="purchasingCost", description="单位: 万元\n对应字段: 设备采购成本"
    )
    """
    单位: 万元
    对应字段: 设备采购成本
    """

    maintenanceFee: float = Field(
        title="maintenanceFee", description="单位: 万元\n对应字段: 设备年维护费"
    )
    """
    单位: 万元
    对应字段: 设备年维护费
    """

    CO2Emission: float = Field(title="CO2Emission", description="单位: 吨\n对应字段: 年碳排放")
    """
    单位: 吨
    对应字段: 年碳排放
    """

    NOXEmission: float = Field(title="NOXEmission", description="单位: 吨\n对应字段: 年NOX排放")
    """
    单位: 吨
    对应字段: 年NOX排放
    """

    SO2Emission: float = Field(title="SO2Emission", description="单位: 吨\n对应字段: 年SO2排放")
    """
    单位: 吨
    对应字段: 年SO2排放
    """


class 规划结果详情(BaseModel):
    元件名称: str = Field(title="元件名称", description="对应字段: deviceName")
    """
    对应字段: deviceName
    """

    型号: str = Field(title="型号", description="对应字段: deviceModel")
    """
    对应字段: deviceModel
    """

    数量: int = Field(title="数量", description="对应字段: deviceCount")
    """
    对应字段: deviceCount
    """

    平均效率_平均COP: float = Field(title="平均效率_平均COP", description="对应字段: COP")
    """
    对应字段: COP
    """

    设备采购成本: float = Field(title="设备采购成本", description="单位: 万元\n对应字段: purchasingCost")
    """
    单位: 万元
    对应字段: purchasingCost
    """

    设备年维护费: float = Field(title="设备年维护费", description="单位: 万元\n对应字段: maintenanceFee")
    """
    单位: 万元
    对应字段: maintenanceFee
    """

    年碳排放: float = Field(title="年碳排放", description="单位: 吨\n对应字段: CO2Emission")
    """
    单位: 吨
    对应字段: CO2Emission
    """

    年NOX排放: float = Field(title="年NOX排放", description="单位: 吨\n对应字段: NOXEmission")
    """
    单位: 吨
    对应字段: NOXEmission
    """

    年SO2排放: float = Field(title="年SO2排放", description="单位: 吨\n对应字段: SO2Emission")
    """
    单位: 吨
    对应字段: SO2Emission
    """

    class Units:
        设备采购成本 = "万元"
        设备年维护费 = "万元"
        年碳排放 = "吨"
        年NOX排放 = "吨"
        年SO2排放 = "吨"

    def translate(self):
        paramDict = self.dict()
        TT = self.get_translation_table()
        params = {TT[k]: v for k, v in paramDict.items()}
        return 规划结果详情_翻译(**params)

    @classmethod
    def get_translation_table(cls) -> Dict[str, str]:
        schema = cls.schema()
        required_keys = schema["required"]
        properties = schema["properties"]
        translation_table = {}
        for rk in required_keys:
            prop = properties[rk]
            desc = prop["description"]
            parse_result = parse.parse(
                "对应字段: {englishTranslation}", desc.split("\n")[-1]
            )
            et = parse_result["englishTranslation"]
            translation_table[rk] = et
        return translation_table

    @classmethod
    # 此处的仿真结果是每个典型日的仿真结果，不是合并之后的仿真结果表格
    # 出来的也是每个典型日对应的规划详情，需要根据设备ID进行合并
    def export(cls, deviceModel: 设备模型协议, deviceSimulationResult, timeParam: float):
        params = {}
        params["元件名称"] = deviceModel.设备信息.设备名称
        params["型号"] = getattr(deviceModel.设备信息, "设备型号", "")
        params["数量"] = value(
            getattr_with_ellipsis_fallback(deviceModel, "DeviceCount", 0)
        )
        params["平均效率_平均COP"] = getattr_with_ellipsis_fallback(
            deviceSimulationResult, "averageEfficiency", cmath.nan
        )
        params["设备采购成本"] = value(deviceModel.总采购成本) * (timeParam / 每年小时数)

        params["机组年启动次数"] = value(
            getattr_with_ellipsis_fallback(deviceModel, "机组年启动次数", cmath.nan)
        )
        params["机组年运行时间"] = value(
            getattr_with_ellipsis_fallback(deviceModel, "机组年运行时间", cmath.nan)
        )
        params["设备年维护费"] = getattr_with_ellipsis_fallback(
            deviceSimulationResult, "设备维护费用", cmath.nan
        )  # 乘过时间参数就不用乘了
        for attrName in ["年碳排放", "年NOX排放", "年SO2排放"]:
            gasType = attrName.strip("年").strip("排放") if "碳" not in attrName else "CO2"

            # fuel instances. we cannot allow diesel engines for this, since this will introduce errors in summation.
            if isinstance(deviceModel, 柴油模型):  # fuel unit: L
                # L * (kg/L)
                modelBaseName = deviceModel.__class__.__name__.strip("模型")
                dieselConsumptionUnit = getattr(
                    globals().get(f"{modelBaseName}仿真结果导出单位"), f"{modelBaseName}消耗量"
                )
                val_raw, val_unit = multiplyWithUnit(
                    (deviceSimulationResult.柴油消耗量, dieselConsumptionUnit),
                    getattr(deviceModel.设备信息, gasType),
                )  # [数值，单位]
                # gas emission unit: kg
                # now you may want to convert this by acquiring units elsewhere...
                target_unit = getattr(规划结果详情.Units, attrName)
                val_quantity = val_raw * ureg.Unit(val_unit)
                val_quantity_target = val_quantity.to(target_unit)
                val = val_quantity_target.magnitude
                # kg -> t (standard)
            else:
                val = cmath.nan
            params[attrName] = val

        return cls(**params)


class 规划方案概览_翻译(BaseModel):
    planType: str = Field(title="planType", description="对应字段: 方案类型")
    """
    对应字段: 方案类型
    """

    annualizedCost: float = Field(
        title="annualizedCost", description="单位: 万元\n对应字段: 年化费用"
    )
    """
    单位: 万元
    对应字段: 年化费用
    """

    purchasingCost: float = Field(
        title="purchasingCost", description="单位: 万元\n对应字段: 设备采购成本"
    )
    """
    单位: 万元
    对应字段: 设备采购成本
    """

    maintenanceFee: float = Field(
        title="maintenanceFee", description="单位: 万元\n对应字段: 设备年维护费"
    )
    """
    单位: 万元
    对应字段: 设备年维护费
    """

    CO2Emission: float = Field(title="CO2Emission", description="单位: 吨\n对应字段: 年碳排放")
    """
    单位: 吨
    对应字段: 年碳排放
    """

    NOXEmission: float = Field(title="NOXEmission", description="单位: 吨\n对应字段: 年NOX排放")
    """
    单位: 吨
    对应字段: 年NOX排放
    """

    SO2Emission: float = Field(title="SO2Emission", description="单位: 吨\n对应字段: 年SO2排放")
    """
    单位: 吨
    对应字段: 年SO2排放
    """

    coldLoad: float = Field(title="coldLoad", description="单位: kWh\n对应字段: 年冷负荷")
    """
    单位: kWh
    对应字段: 年冷负荷
    """

    hotLoad: float = Field(title="hotLoad", description="单位: kWh\n对应字段: 年热负荷")
    """
    单位: kWh
    对应字段: 年热负荷
    """

    eleLoad: float = Field(title="eleLoad", description="单位: kWh\n对应字段: 年电负荷")
    """
    单位: kWh
    对应字段: 年电负荷
    """

    steamLoad: float = Field(title="steamLoad", description="单位: t\n对应字段: 年蒸汽负荷")
    """
    单位: t
    对应字段: 年蒸汽负荷
    """

    hydrogenLoad: float = Field(
        title="hydrogenLoad", description="单位: Nm³\n对应字段: 年氢气负荷"
    )
    """
    单位: Nm³
    对应字段: 年氢气负荷
    """


class 规划方案概览(BaseModel):
    方案类型: str = Field(title="方案类型", description="对应字段: planType")
    """
    对应字段: planType
    """

    年化费用: float = Field(title="年化费用", description="单位: 万元\n对应字段: annualizedCost")
    """
    单位: 万元
    对应字段: annualizedCost
    """

    设备采购成本: float = Field(title="设备采购成本", description="单位: 万元\n对应字段: purchasingCost")
    """
    单位: 万元
    对应字段: purchasingCost
    """

    设备年维护费: float = Field(title="设备年维护费", description="单位: 万元\n对应字段: maintenanceFee")
    """
    单位: 万元
    对应字段: maintenanceFee
    """

    年碳排放: float = Field(title="年碳排放", description="单位: 吨\n对应字段: CO2Emission")
    """
    单位: 吨
    对应字段: CO2Emission
    """

    年NOX排放: float = Field(title="年NOX排放", description="单位: 吨\n对应字段: NOXEmission")
    """
    单位: 吨
    对应字段: NOXEmission
    """

    年SO2排放: float = Field(title="年SO2排放", description="单位: 吨\n对应字段: SO2Emission")
    """
    单位: 吨
    对应字段: SO2Emission
    """

    年冷负荷: float = Field(title="年冷负荷", description="单位: kWh\n对应字段: coldLoad")
    """
    单位: kWh
    对应字段: coldLoad
    """

    年热负荷: float = Field(title="年热负荷", description="单位: kWh\n对应字段: hotLoad")
    """
    单位: kWh
    对应字段: hotLoad
    """

    年电负荷: float = Field(title="年电负荷", description="单位: kWh\n对应字段: eleLoad")
    """
    单位: kWh
    对应字段: eleLoad
    """

    年蒸汽负荷: float = Field(title="年蒸汽负荷", description="单位: t\n对应字段: steamLoad")
    """
    单位: t
    对应字段: steamLoad
    """

    年氢气负荷: float = Field(title="年氢气负荷", description="单位: Nm³\n对应字段: hydrogenLoad")
    """
    单位: Nm³
    对应字段: hydrogenLoad
    """

    class Units:
        年化费用 = "万元"
        设备采购成本 = "万元"
        设备年维护费 = "万元"
        年碳排放 = "吨"
        年NOX排放 = "吨"
        年SO2排放 = "吨"
        年冷负荷 = "kWh"
        年热负荷 = "kWh"
        年电负荷 = "kWh"
        年蒸汽负荷 = "t"
        年氢气负荷 = "Nm³"

    def translate(self):
        paramDict = self.dict()
        TT = self.get_translation_table()
        params = {TT[k]: v for k, v in paramDict.items()}
        return 规划方案概览_翻译(**params)

    @classmethod
    def get_translation_table(cls) -> Dict[str, str]:
        schema = cls.schema()
        required_keys = schema["required"]
        properties = schema["properties"]
        translation_table = {}
        for rk in required_keys:
            prop = properties[rk]
            desc = prop["description"]
            parse_result = parse.parse(
                "对应字段: {englishTranslation}", desc.split("\n")[-1]
            )
            et = parse_result["englishTranslation"]
            translation_table[rk] = et
        return translation_table

    @classmethod
    def export(
        cls,
        planningResultList: List[规划结果详情],
        simulationResultList: List[仿真结果],
        FSPT: Dict[str, str],
        totalAnnualFee: float,
        planType: str,
    ):  # totalAnnualFee is equivalent to our "financial" objective
        params = dict(年化费用=totalAnnualFee, 方案类型=planType)

        def updateParam(k, v):
            params[k] = params.get(k, 0) + (v if not np.isnan(v) else 0)

        duplicate_params_planning_keys = getDuplicatedSchemaKeysSetFromDataModels(
            规划方案概览, 规划结果详情
        )

        for planningResult in planningResultList:
            for duplicatedKey in duplicate_params_planning_keys:
                val = getattr(planningResult, duplicatedKey)
                updateParam(duplicatedKey, val)

        remainedKeys = getRequiredKeysSetFromDataModel(cls).difference(
            set(params.keys())
        )

        for simulationResult in simulationResultList:
            for remainedKey in remainedKeys:  # '年热负荷', '年电负荷', '年冷负荷', '年蒸汽负荷', '年氢气负荷'
                keyBase = remainedKey.strip("年").strip("负荷").strip("消耗量")
                for keySuffix in ["负荷", "消耗量"]:
                    attemptKey = f"{keyBase}{keySuffix}"
                    if (
                        val := getattr(
                            simulationResult,
                            FSPT.get(attemptKey, "NO_TRANSLATION"),
                            ...,
                        )
                    ) is not ...:
                        updateParam(remainedKey, val)
                    break
        remainedKeys = getRequiredKeysSetFromDataModel(cls).difference(
            set(params.keys())
        )
        for rk in remainedKeys:
            params[rk] = cmath.nan
        return cls(**params)


class 节点基类(BaseModel):
    subtype: constr(min_length=1) = Field(title="节点次类型")
    id: int = Field(title="节点ID")


class 连线节点(节点基类):
    type: Literal["连接线", "合并线"]


class 锚点节点(节点基类):
    type: Literal["锚点"]
    port_name: constr(min_length=1) = Field(title="锚点名称")
    device_id: conint(ge=0) = Field(title="锚点所对应设备ID")


class 母线节点(节点基类):
    type: Literal["母线"]
    conn: conlist(constr(min_length=1), min_items=2) = Field(
        title="母线连接线类型列表", description="包括连接到母线上的连接线和合并线类型"
    )  # connection/merge types to literal.


class 设备接口映射(BaseModel):
    subtype: constr(min_length=1) = Field(title="接口类型")
    id: conint(ge=0) = Field(title="接口ID", description="拓扑图上与设备、母线、连接线的ID相比较具有唯一性的ID")


class 设备节点基类(节点基类):
    type: Literal["设备"]
    ports: Dict[constr(min_length=1), 设备接口映射] = Field(
        title="设备接口映射", description="描述设备所对应接口的类型和接口ID"
    )


deviceSubtypeAlias = dict(变流器=["单向变流器"], 变压器="双向变压器")
DSAToDS = {e: k for k, v in deviceSubtypeAlias.items() for e in v}


class 柴油节点(设备节点基类):
    subtype: Literal["柴油", *deviceSubtypeAlias.get("柴油", [])] = Field(title="节点次类型")
    param: 柴油信息 = Field(title="设备信息", description="柴油信息")


class 电负荷节点(设备节点基类):
    subtype: Literal["电负荷", *deviceSubtypeAlias.get("电负荷", [])] = Field(title="节点次类型")
    param: 电负荷信息 = Field(title="设备信息", description="电负荷信息")


class 光伏发电节点(设备节点基类):
    subtype: Literal["光伏发电", *deviceSubtypeAlias.get("光伏发电", [])] = Field(title="节点次类型")
    param: 光伏发电信息 = Field(title="设备信息", description="光伏发电信息")


class 风力发电节点(设备节点基类):
    subtype: Literal["风力发电", *deviceSubtypeAlias.get("风力发电", [])] = Field(title="节点次类型")
    param: 风力发电信息 = Field(title="设备信息", description="风力发电信息")


class 柴油发电节点(设备节点基类):
    subtype: Literal["柴油发电", *deviceSubtypeAlias.get("柴油发电", [])] = Field(title="节点次类型")
    param: 柴油发电信息 = Field(title="设备信息", description="柴油发电信息")


class 锂电池节点(设备节点基类):
    subtype: Literal["锂电池", *deviceSubtypeAlias.get("锂电池", [])] = Field(title="节点次类型")
    param: 锂电池信息 = Field(title="设备信息", description="锂电池信息")


class 变压器节点(设备节点基类):
    subtype: Literal["变压器", *deviceSubtypeAlias.get("变压器", [])] = Field(title="节点次类型")
    param: 变压器信息 = Field(title="设备信息", description="变压器信息")


class 变流器节点(设备节点基类):
    subtype: Literal["变流器", *deviceSubtypeAlias.get("变流器", [])] = Field(title="节点次类型")
    param: 变流器信息 = Field(title="设备信息", description="变流器信息")


class 双向变流器节点(设备节点基类):
    subtype: Literal["双向变流器", *deviceSubtypeAlias.get("双向变流器", [])] = Field(
        title="节点次类型"
    )
    param: 双向变流器信息 = Field(title="设备信息", description="双向变流器信息")


class 传输线节点(设备节点基类):
    subtype: Literal["传输线", *deviceSubtypeAlias.get("传输线", [])] = Field(title="节点次类型")
    param: 传输线信息 = Field(title="设备信息", description="传输线信息")


class 氢负荷节点(设备节点基类):
    subtype: Literal["氢负荷", *deviceSubtypeAlias.get("氢负荷", [])] = Field(title="节点次类型")
    param: 氢负荷信息 = Field(title="设备信息", description="氢负荷信息")


class 电解槽节点(设备节点基类):
    subtype: Literal["电解槽", *deviceSubtypeAlias.get("电解槽", [])] = Field(title="节点次类型")
    param: 电解槽信息 = Field(title="设备信息", description="电解槽信息")


class mDict(BaseModel):
    directed: bool = Field(default=False, title="保留字段")
    multigraph: bool = Field(default=False, title="保留字段")
    graph: 计算参数 = Field(
        title="能流拓扑图的附加属性",
        description="仿真和优化所需的模型参数字典",
        example={
            "计算步长": "小时",
            "典型日": False,
            "典型日代表的日期": [],
            "计算类型": "设计规划",
            "风速": [],
            "光照": [],
            "气温": [],
            "年利率": 0.1,
        },
    )
    nodes: conlist(
        Union[
            锚点节点,
            柴油节点,
            电负荷节点,
            光伏发电节点,
            风力发电节点,
            柴油发电节点,
            锂电池节点,
            变压器节点,
            变流器节点,
            双向变流器节点,
            传输线节点,
            氢负荷节点,
            电解槽节点,
            母线节点,
            连线节点,
        ],
        min_items=5,
    ) = Field(
        title="节点",
        description="由所有节点ID和属性字典组成的列表",
        example=[
            {
                "type": "锚点",
                "port_name": "电接口",
                "subtype": "供电端输出",
                "device_id": 2,
                "id": 3,
            }
        ],
    )
    links: conlist(Dict[Literal["source", "target"], int], min_items=4) = Field(
        title="边",
        description="由能流图中节点互相连接的边组成的列表",
        example=[{"source": 0, "target": 1}, {"source": 1, "target": 31}],
    )


# TODO: 增加单典型日判断类型或者字段


class EnergyFlowGraph(BaseModel):
    mDictList: List[mDict]
    residualEquipmentLife: confloat(ge=0) = Field(
        default=0, title="辅助设备寿命", description="默认为0，年化率返回为1\n单位：年\n用于计算辅助设备年化系数"
    )


from networkx import Graph
from failsafe_utils import failsafe_suppress_exception


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

    typicalDayIndex = algoParam.典型日ID

    devInstDict = {}

    for dev in devs:
        with failsafe_suppress_exception():
            __devSubtype = dev["subtype"]
            devSubtype = DSAToDS.get(__devSubtype, __devSubtype)
            devParam = dev["param"]
            devPorts = dev["ports"]

            devID_int = dev["id"]

            devIDClass = devIDClassMap[devSubtype]

            devIDInstInit = {"ID": devID_int}
            for port_name, port_info in devPorts.items():
                with failsafe_suppress_exception():
                    port_id = port_info["id"]
                    devIDInstInit.update({port_name: port_id})
            devIDInst = devIDClass.parse_obj(devIDInstInit)

            devInfoInstInit = devParam
            devInfoClass = devInfoClassMap[devSubtype]
            devInfoInst = devInfoClass.parse_obj(devInfoInstInit)

            devInstClass = devInstClassMap[devSubtype]
            devInst = devInstClass(PD=PD, mw=mw, 计算参数实例=algoParam, 设备ID=devIDInst, 设备信息=devInfoInst)  # type: ignore

            devInstDict.update({devID_int: devInst})

    adder_index_error_mapping = {}
    adder_error_total = {}
    adder_index_error_sum_mapping = {}

    # positive for too much input
    # negative for insufficient input
    # you may activate both

    adder_positive_error_total = 0
    adder_negative_error_total = 0
    adder_combined_error_total = 0

    for adder_index, adder in adders.items():
        adder_error_mapping = {}
        adder_current_positive_error = 0
        adder_current_negative_error = 0
        adder_current_combined_error = 0

        with failsafe_suppress_exception():
            input_indexs, output_indexs, io_indexs = (
                adder["input"],
                adder["output"],
                adder["IO"],
            )
            logger_print(f"adder #{adder_index}:", adder)

            # fill in missing params
            with failsafe_suppress_exception():
                if len(input_indexs) >= 1:
                    first_port_info = G.nodes[input_indexs[0]]
                    if first_port_info["port_name"] == "燃料接口":
                        assert len(input_indexs) == 1, "燃料元件只能一对多连接"
                        diesel_node_id = G.nodes[input_indexs[0]]["device_id"]
                        热值 = devInstDict[diesel_node_id].热值
                        for output_index in output_indexs:
                            output_node_index = G.nodes[output_index]["device_id"]
                            devInstDict[output_node_index].燃料热值 = 热值
            # add them all.

            logger_print("_" * 20)
            display_var_names = lambda indexs: "\n    ".join(
                [str(PD[i]) for i in indexs]
            )
            logger_print(f"INPUTS:{display_var_names(input_indexs)}")
            logger_print()
            logger_print(f"OUTPUTS:{display_var_names(output_indexs)}")
            logger_print()
            logger_print(f"IO:{display_var_names(io_indexs)}")
            logger_print("_" * 20)

            adder_index_repr = str(adder_index).replace("_", "-").replace("-", "N")

            for j in range(algoParam.迭代步数):
                seqsum = sum(
                    [PD[i][j] for i in input_indexs + output_indexs + io_indexs]
                )

                # TODO: 消纳率约束
                positive_error = mw.Var(
                    name=f"TD_{typicalDayIndex}_AD_{adder_index_repr}_PE_{j}",
                    within=NonNegativeReals,
                )
                if not (
                    "positive" in ies_env.ADDER_ERROR_COMPENSATION
                    or ies_env.ADDER_ERROR_COMPENSATION == "combined"
                ):
                    positive_error.fix(0)
                negative_error = mw.Var(
                    name=f"TD_{typicalDayIndex}_AD_{adder_index_repr}_NE_{j}",
                    within=NonNegativeReals,
                )
                if not (
                    "negative" in ies_env.ADDER_ERROR_COMPENSATION
                    or ies_env.ADDER_ERROR_COMPENSATION == "combined"
                ):
                    negative_error.fix(0)

                combined_error = positive_error + negative_error

                adder_error_mapping[j] = dict(
                    positive_error=positive_error,
                    negative_error=negative_error,
                    combined_error=combined_error,
                )
                adder_current_positive_error += positive_error
                adder_current_negative_error += negative_error
                adder_current_combined_error += combined_error

                mw.Constraint(seqsum == positive_error - negative_error)
            adder_index_error_mapping[adder_index] = adder_error_mapping
            adder_index_error_sum_mapping[adder_index] = dict(
                positive_error=adder_current_positive_error,
                negative_error=adder_current_negative_error,
                combined_error=adder_current_combined_error,
            )
            adder_positive_error_total += adder_current_positive_error
            adder_negative_error_total += adder_current_negative_error
            adder_combined_error_total += adder_current_combined_error
            with failsafe_suppress_exception():
                if algoParam.计算类型 == "设计规划":
                    cnt = 0
                    if len(input_indexs) == 0:
                        continue
                    input_anchor_0 = G.nodes[input_indexs[0]]
                    if input_anchor_0["subtype"] == "变压器输出":
                        logger_print(f"Building Converter Constraint #{cnt}")
                        cnt += 1
                        assert io_indexs == []

                        input_limit = iterate_input_output_limit(
                            "最大允许的负载总功率", input_indexs, G, devInstDict
                        )
                        output_limit = iterate_input_output_limit(
                            "MaxEnergyConsumption", output_indexs, G, devInstDict
                        )

                        mw.Constraint(input_limit + output_limit >= 0)

    adder_error_total = dict(
        positive_error=adder_positive_error_total,
        negative_error=adder_negative_error_total,
        combined_error=adder_combined_error_total,
    )
    financial_obj_expr = 0

    checkIfIsLoadClassInstance = lambda inst: "负荷" in inst.__class__.__name__

    for e in devInstDict.values():
        with failsafe_suppress_exception():
            val = e.constraints_register()
            financial_obj_expr += val if not checkIfIsLoadClassInstance(e) else 0
            financial_obj_expr = addPunishRateToFinancialTarget(
                financial_obj_expr, devInst
            )

    financial_dyn_obj_expr = 0

    for e in devInstDict.values():
        with failsafe_suppress_exception():
            val = e.总可变维护成本年化
            financial_dyn_obj_expr += val if not checkIfIsLoadClassInstance(e) else 0
            financial_dyn_obj_expr = addPunishRateToFinancialTarget(
                financial_obj_expr, devInst
            )

    environment_obj_exprs = []  # annual CO2 emission

    for e in devInstDict.values():
        if isinstance(e, 柴油模型):
            environment_obj_exprs.append(
                (sum(e.燃料接口.values()) / e.计算参数.迭代步数) * 每年小时数 * e.CO2
            )

    environment_obj_expr = sum(environment_obj_exprs)

    obj_exprs = (
        financial_obj_expr,
        financial_dyn_obj_expr,
        environment_obj_expr,
    )
    # TODO: return 'adder_index_error_mapping'
    extra_data = dict(
        adder_index_error_mapping=adder_index_error_mapping,
        adder_error_total=adder_error_total,
        adder_index_error_sum_mapping=adder_index_error_sum_mapping,
    )
    return obj_exprs, devInstDict, PD, extra_data
    # always minimize the objective.


def addValueToTarget(target, devInst, attrName: str, iterCount: int):
    if hasattr(devInst, attrName):
        target += getattr(devInst, attrName) * iterCount
    return target


def addNewRateToAnnualTarget(target, devInst, attrName: str):
    target = addValueToTarget(target, devInst, attrName, 每年小时数)
    return target


def addPunishRateToFinancialTarget(target, devInst):
    target = addNewRateToAnnualTarget(target, devInst, "punishRate")
    return target
