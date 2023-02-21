# coding: utf-8
# 整理完所有缩写的全称之后,绘制拓扑图
# 可以把代码转化成图

"""
模块简介:


"""

# chinese display issue
import matplotlib
import os

# os.system("chcp 65001") # not working?

matplotlib.rc("font", family="YouYuan")

from docplex.mp.solution import SolveSolution

# import docplex  # modeling with ibm cplex
from docplex.mp.model import Model
from typing import Union

# import pandas as pd
import numpy as np
import time
import os.path
import math

from typing import Iterable

# from docplex.mp.conflict_refiner import ConflictRefiner
import matplotlib.pyplot as plt

# from matplotlib import style
from result_processlib import Value  # ?
from docplex.mp.dvar import Var
from typing import List

from docplex.mp.vartype import (
    VarType,
    BinaryVarType,
    IntegerVarType,
    ContinuousVarType,
    SemiContinuousVarType,
    SemiIntegerVarType,
)

# we prefer not to plot this.
# from plot_arr import IGESPlot as IntegratedEnergySystemPlot

localtime1 = time.time()

# create main model
model1 = Model(name="buses")


# ma = 0  # not using? moving average?

debug = 1
"""
作用:如果设置为1,将把num_hour0乘以year(year的默认值是1)
"""

run = 0
year = 1

day_node = 24
"""
一天24小时
"""

node = day_node * 1 * 1
if debug == 0:
    num_hour0 = node
else:
    num_hour0 = node * year

# a big number
bigNumber = 10e10
"""
设置一个大的数,默认值为10的10次
"""
# total simulation rounds?
simulationTime = 3600

# every hour of one day?
intensityOfIllumination = np.ones(num_hour0)
"""
24小时光照强度数组,数组形状为`(num_hour0,)`,所有元素初始化为1
"""
# what is this "ha"? just sunlight stats per hour in a day?


# another name for IES?
class IntegratedEnergySystem(object):
    """
    综合能源系统基类
    """

    device_count: int = 0  # what is this "SET"? device?

    def __init__(self, device_name: str):
        """
        新建一个综合能源系统基类,设置设备名称,设备编号加一,打印设备名称和编号
        """
        self.device_name = device_name
        IntegratedEnergySystem.device_count += 1
        print(
            "IntegratedEnergySystem Define a device named:",
            device_name,
            ", total device count/device number is:",
            IntegratedEnergySystem.device_count,
        )


class PhotoVoltaic(IntegratedEnergySystem):  # Photovoltaic
    """
    光伏类,适用于光伏及平板式光热
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        photoVoltaic_device_max: float,
        device_price: float,  # float?
        intensityOfIllumination0: np.ndarray,
        efficiency: float,  # efficiency
        device_name: str = "PhotoVoltaic",
    ):
        """
        新建一个光伏类

        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            photoVoltaic_device_max (float): 光伏设备机组最大装机量
            device_price (float): 设备单价
            intensityOfIllumination0 (np.ndarray): 24小时光照强度
            efficiency (float): 设备运行效率
            device_name (str): 光伏机组名称,默认为"PhotoVoltaic"
        """
        IntegratedEnergySystem(device_name)
        PhotoVoltaic.index += (
            1  # increase the index whenever another PhotoVoltaic system is created.
        )

        self.photoVoltaic_device: ContinuousVarType = model.continuous_var(
            name="photoVoltaic_device{0}".format(PhotoVoltaic.index)
        )
        """
        光伏机组等效单位设备数 大于零的实数
        """
        self.power_photoVoltaic: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, num_hour)],
            name="power_photoVoltaic{0}".format(PhotoVoltaic.index),
        )
        """
        初始化每个小时内光伏机组发电量 大于零的实数 一共`num_hour`个变量
        """
        self.photoVoltaic_device_max = photoVoltaic_device_max
        self.device_price = device_price
        self.num_hour = num_hour
        # intensityOfIllumination
        self.intensityOfIllumination = intensityOfIllumination0
        self.efficiency = efficiency
        self.annualized: ContinuousVarType = model.continuous_var(
            name="photoVoltaic_annualized{0}".format(PhotoVoltaic.index)
        )
        """
        每年消耗的运维成本 大于零的实数
        """

    def constraints_register(self, model: Model):
        """
        定义机组内部约束

        1. 机组设备总数不得大于最大装机量
        2. 机组设备数大于等于0
        3. 每个小时内,输出发电量小于等于机组等效单位设备数*效率*光照强度
        4. 每年消耗的运维成本 = 机组等效单位设备数*单位设备价格/15

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        model.add_constraint(
            self.photoVoltaic_device <= self.photoVoltaic_device_max
        )  # 最大装机量
        model.add_constraint(self.photoVoltaic_device >= 0)
        model.add_constraints(
            self.power_photoVoltaic[i]  # 输出发电量不得超过最大发电量
            <= self.photoVoltaic_device
            * self.efficiency
            * self.intensityOfIllumination[i]
            for i in range(self.num_hour)
        )
        model.add_constraint(
            self.annualized == self.photoVoltaic_device * self.device_price / 15
        )  # 每年维护费用？折价？回收成本？利润？

    def total_cost(self, solution: SolveSolution) -> float:  # 购买设备总费用
        """
        Args:
            solution (docplex.mp.solution.SolveSolution): 求解模型的求解结果

        Return:
            购买设备总费用 = 机组等效单位设备数*单位设备价格
        """
        return solution.get_value(self.photoVoltaic_device) * self.device_price


# LiBr制冷
class LiBrRefrigeration(IntegratedEnergySystem):
    """
    溴化锂制冷类,适用于制冷机组
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        LiBr_device_max: float,
        device_price: float,  # what is this device?
        efficiency: float,
        device_name: str = "LiBrRefrigeration",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            LiBr_device_max (float): 溴化锂制冷设备机组最大装机量
            device_price (float): 设备单价
            efficiency (float): 设备运行效率
            device_name (str): 溴化锂制冷机组名称,默认为"LiBrRefrigeration"
        """
        IntegratedEnergySystem(device_name)
        LiBrRefrigeration.index += 1
        self.num_hour = num_hour
        self.LiBr_device: ContinuousVarType = model.continuous_var(
            name="LiBr_device{0}".format(LiBrRefrigeration.index)
        )
        """
        溴化锂制冷机组等效单位设备数 大于零的实数
        """

        self.heat_LiBr_from: List[
            ContinuousVarType
        ] = model.continuous_var_list(  # iterate through hours in a day?
            [i for i in range(0, self.num_hour)],
            name="heat_LiBr_from{0}".format(LiBrRefrigeration.index),
        )
        """
        初始化每个小时内溴化锂机组制热设备 大于零的实数 一共`num_hour`个变量
        """

        self.cool_LiBr: List[
            ContinuousVarType
        ] = model.continuous_var_list(  # the same?
            [i for i in range(0, self.num_hour)],
            name="heat_LiBr{0}".format(LiBrRefrigeration.index),
        )
        """
        初始化每个小时内溴化锂机组制冷设备 大于零的实数 一共`num_hour`个变量
        """

        self.LiBr_device_max = LiBr_device_max
        self.device_price = device_price
        self.efficiency = efficiency
        self.annualized: ContinuousVarType = model.continuous_var(
            name="LiBr_annualized{0}".format(LiBrRefrigeration.index)
        )
        """
        每年消耗的运维成本 大于零的实数
        """

    def constraints_register(self, model: Model):
        """
        定义机组内部约束

        1. 机组设备数大于等于0
        2. 机组设备总数不得大于最大装机量
        3. 每个小时内,制热设备大于等于0,且不超过溴化锂机组设备数
        4. 每个小时内,制冷量 = 制热等效单位设备数/效率
        5. 每年消耗的运维成本 = 机组等效单位设备数*单位设备价格/15

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        # register constraints
        hourRange = range(0, self.num_hour)
        model.add_constraint(self.LiBr_device >= 0)
        model.add_constraint(self.LiBr_device <= self.LiBr_device_max)
        model.add_constraints(
            self.heat_LiBr_from[h] >= 0 for h in hourRange
        )  # adding multiple constraints, passed as arguments
        model.add_constraints(
            self.heat_LiBr_from[h] <= self.LiBr_device for h in hourRange
        )  # avaliable/active device count?
        model.add_constraints(
            self.cool_LiBr[h] == self.heat_LiBr_from[h] / self.efficiency
            for h in hourRange  # how does this work out? what is the meaning of this?
        )
        model.add_constraint(
            self.annualized == self.LiBr_device * self.device_price / 15
        )


# 柴油发电机
class DieselEngine(IntegratedEnergySystem):
    """
    柴油发电机类,适用于发电机组
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        dieselEngine_device_max: int,
        device_price: int,
        run_price: int,
        device_name="dieselEngine",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            dieselEngine_device_max (float): 柴油发电机设备机组最大装机量
            device_price (float): 设备单价
            run_price (float): 运维价格
            device_name (str): 柴油发电机机组名称,默认为"DieselEngine"
        """
        IntegratedEnergySystem(device_name)
        DieselEngine.index += 1
        self.num_hour = num_hour
        self.dieselEngine_device: ContinuousVarType = model.continuous_var(
            name="dieselEngine_device{0}".format(DieselEngine.index)
        )
        """
        柴油发电机机组等效单位设备数 大于零的实数
        """
        self.power_dieselEngine: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],  # keys, not values.
            name="power_dieselEngine{0}".format(DieselEngine.index),
        )
        """
        初始化每个小时内柴油发电机机组发电量 大于零的实数 一共`num_hour`个变量
        """
        self.dieselEngine_device_max = dieselEngine_device_max
        self.device_price = device_price
        self.run_price = run_price
        self.power_sum = model.sum(
            self.power_dieselEngine[i] for i in range(0, self.num_hour)
        )
        """
        柴油发电机总发电量
        """
        self.annualized: ContinuousVarType = model.continuous_var(
            name="dieselEngine_annualized{0}".format(DieselEngine.index)
        )
        """
        每年消耗的运维成本 大于零的实数
        """

    def constraints_register(self, model: Model):
        """
        定义机组内部约束

        1. 机组设备数大于等于0
        2. 机组设备总数不得大于最大装机量
        3. 每个小时内,设备发电量小于等于装机设备实际值
        4. 每年消耗的运维成本 = 机组等效单位设备数*单位设备价格/15+设备总发电量*设备运行价格*8760/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        model.add_constraint(self.dieselEngine_device <= self.dieselEngine_device_max)
        model.add_constraint(self.dieselEngine_device >= 0)
        model.add_constraints(
            self.power_dieselEngine[i]
            <= self.dieselEngine_device  # does this make sense? again active device count per hour?
            for i in range(0, self.num_hour)
        )
        model.add_constraint(
            self.annualized  # 年运行成本?
            == self.dieselEngine_device * self.device_price / 15
            + self.power_sum * self.run_price * 8760 / self.num_hour
        )

    def total_cost(self, solution: SolveSolution) -> float:
        """
        Args:
            solution (docplex.mp.solution.SolveSolution): 求解模型的求解结果

        Return:
            购买设备总费用 = 机组等效单位设备数*单位设备价格
        """
        # energyStorageSystem you will have it?
        return solution.get_value(self.dieselEngine_device) * self.device_price


# 储能系统基类
class EnergyStorageSystem(IntegratedEnergySystem):
    """
    储能系统基类,适用于储能机组
    """

    index: int = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        energyStorageSystem_device_max: float,
        energyStorageSystem_price: float,
        powerConversionSystem_price: float,
        conversion_rate_max: float,
        efficiency: float,
        energyStorageSystem_init: int,
        stateOfCharge_min: float,
        stateOfCharge_max: float,
        device_name: str = "energyStorageSystem",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            energyStorageSystem_device_max (float): 储能系统设备机组最大装机量
            energyStorageSystem_price (float):储能装置的购置价格。
            powerConversionSystem_price (float):储能装置与电网之间的 PCS 转换价格。
            eff (float):储能装置的充放电效率。
            conversion_rate_max (float):储能装置的最大倍率。
            energyStorageSystem_init (int):储能装置的初始能量。
            stateOfCharge_min (float):储能装置的最小储能量百分比。
            stateOfCharge_max (float):储能装置的最大储能量百分比。
            device_name (str): 储能系统机组名称,默认为"energyStorageSystem"
        """
        IntegratedEnergySystem(device_name)
        EnergyStorageSystem.index += 1

        self.energyStorageSystem_device: ContinuousVarType = model.continuous_var(
            name="energyStorageSystem_device{0}".format(EnergyStorageSystem.index)
        )
        """
        储能系统机组等效单位设备数 大于零的实数
        """
        self.power_energyStorageSystem: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, num_hour)],
            lb=-bigNumber,
            name="power_energyStorageSystem{0}".format(EnergyStorageSystem.index),
        )
        """
        模型中的连续变量列表,长度为 num_hour,表示每小时储能装置的充放电功率
        """
        # 充电功率
        self.power_energyStorageSystem_charge: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, num_hour)],
            name="power_energyStorageSystem_charge{0}".format(
                EnergyStorageSystem.index
            ),
        )
        """
        模型中的连续变量列表,长度为 num_hour,表示每小时储能装置的充电功率
        """
        # 放电功率
        self.power_energyStorageSystem_discharge: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, num_hour)],
            name="power_energyStorageSystem_discharge{0}".format(
                EnergyStorageSystem.index
            ),
        )
        """
        模型中的连续变量列表,长度为 num_hour,表示每小时储能装置的放电功率
        """
        # 能量
        self.energyStorageSystem: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, num_hour)],
            name="energyStorageSystem{0}".format(EnergyStorageSystem.index),
        )
        """
        模型中的连续变量列表,长度为 num_hour,表示每小时储能装置的能量
        """
        self.energyStorageSystem_device_max = energyStorageSystem_device_max
        self.energyStorageSystem_price = energyStorageSystem_price
        self.powerConversionSystem_price = powerConversionSystem_price  # powerConversionSystem? power conversion system?
        self.num_hour = num_hour
        self.powerConversionSystem_device: ContinuousVarType = model.continuous_var(
            name="powerConversionSystem_device{0}".format(EnergyStorageSystem.index)
        )  # powerConversionSystem
        """
        模型中的连续变量,表示 PCS 的容量。
        """
        self.charge_flag: List[BinaryVarType] = model.binary_var_list(  # is charging?
            [i for i in range(0, num_hour)],
            name="batteryEnergyStorageSystem_charge_flag{0}".format(
                EnergyStorageSystem.index
            ),
        )  # 充电
        """
        模型中的二元变量列表,长度为`num_hour`,表示每小时储能装置是否处于充电状态。
        """
        self.discharge_flag: List[BinaryVarType] = model.binary_var_list(
            [i for i in range(0, num_hour)],
            name="batteryEnergyStorageSystem_discharge_flag{0}".format(
                EnergyStorageSystem.index
            ),
        )  # 放电
        """
        模型中的二元变量列表,长度为`num_hour`,表示每小时储能装置是否处于放电状态。
        """
        # 效率
        self.efficiency = efficiency
        self.conversion_rate_max = conversion_rate_max  # rate of change/charge?
        self.energyStorageSystem_init = energyStorageSystem_init
        self.stateOfCharge_min = stateOfCharge_min
        self.stateOfCharge_max = stateOfCharge_max
        self.annualized: ContinuousVarType = model.continuous_var(
            name="energyStorageSystem_annualized{0}".format(EnergyStorageSystem.index)
        )
        """
        每年消耗的运维成本 大于零的实数
        """

    def constraints_register(
        self, model: Model, register_period_constraints=1, day_node=24
    ):
        """
        定义机组内部约束

        1. 机组设备数大于等于0
        2. 机组设备总数不得大于最大装机量
        3. 储能装置功率转化率约束:储能系统设备*储能装置的最大倍率大于等于功率转化系统设备,且功率转化系统设备大于等于0
        4. 充电功率和放电功率之间的关系:储能系统功率=-充电功率+放电功率
        5. 充电功率约束:充电功率大于等于0,小于等于功率转化系统设备,小于等于充电电状态*bigNumber
        6. 放电功率约束:放电功率大于等于0,于等于功率转化系统设备,小于等于放电状态*bigNumber
        7. 充电功率和放电功率二选一
        8. 储能量守恒约束:储能系统能量=上一时段储能量+(当前时段充电*效率-当前时段放电/效率)*simulationTime/3600
        9. 最大和最小储能量约束:储能设备数*储能装置的最小储能量百分比≦储能系统能量≦储能设备数*储能装置的最大储能量百分比
        10. 每年消耗的运维成本 = (储能设备数*储能设备价格+功率转化系统设备数*功率转化系统价格)/15
        11. 如果regester_period_constraints参数为1,表示将两天之间的储能量连接约束为切断;如果regester_period_constraints参数不为1,表示将两天之间的储能量连接约束为连续。(这里搞不懂啥意思)


        Args:
            model (docplex.mp.model.Model): 求解模型实例
            register_period_constraints (int): 注册周期约束为1
            day_node (int): 一天时间节点为24
        """
        bigNumber = 1e10
        irange = range(0, self.num_hour)
        model.add_constraint(
            self.energyStorageSystem_device <= self.energyStorageSystem_device_max
        )
        model.add_constraint(self.energyStorageSystem_device >= 0)
        model.add_constraint(
            self.energyStorageSystem_device * self.conversion_rate_max
            >= self.powerConversionSystem_device  # satisfying the need of power conversion system? power per unit?
        )
        model.add_constraint(self.powerConversionSystem_device >= 0)
        # 功率拆分
        model.add_constraints(
            self.power_energyStorageSystem[i]
            == -self.power_energyStorageSystem_charge[i]
            + self.power_energyStorageSystem_discharge[i]
            for i in irange
        )

        model.add_constraints(
            self.power_energyStorageSystem_charge[i] >= 0 for i in irange
        )
        model.add_constraints(
            self.power_energyStorageSystem_charge[i]
            <= self.charge_flag[i] * bigNumber  # smaller than infinity?
            for i in irange
        )
        model.add_constraints(
            self.power_energyStorageSystem_charge[i]
            <= self.powerConversionSystem_device
            for i in irange
        )

        model.add_constraints(
            self.power_energyStorageSystem_discharge[i] >= 0 for i in irange
        )
        model.add_constraints(
            self.power_energyStorageSystem_discharge[i]
            <= self.discharge_flag[i] * bigNumber
            for i in irange
        )
        model.add_constraints(
            self.power_energyStorageSystem_discharge[i]
            <= self.powerConversionSystem_device
            for i in irange
        )

        model.add_constraints(
            self.charge_flag[i] + self.discharge_flag[i] == 1 for i in irange
        )
        # 节点必须是24的倍数
        # day_node=24
        for day in range(1, int(self.num_hour / day_node) + 1):
            model.add_constraints(
                self.energyStorageSystem[i]
                == self.energyStorageSystem[
                    i - 1
                ]  # previous state, previous level/state of charge
                + (
                    self.power_energyStorageSystem_charge[i] * self.efficiency
                    - self.power_energyStorageSystem_discharge[i] / self.efficiency
                )
                * simulationTime
                / 3600
                for i in range(1 + day_node * (day - 1), day_node * day)
            )

        model.add_constraints(
            self.energyStorageSystem[i]
            <= self.energyStorageSystem_device * self.stateOfCharge_max
            for i in range(1, self.num_hour)
        )
        model.add_constraints(
            self.energyStorageSystem[i]
            >= self.energyStorageSystem_device * self.stateOfCharge_min
            for i in range(1, self.num_hour)
        )
        model.add_constraint(
            self.annualized
            == (
                self.energyStorageSystem_device * self.energyStorageSystem_price
                + self.powerConversionSystem_device * self.powerConversionSystem_price
            )
            / 15
        )

        # 两天之间直接割裂,没有啥关系
        if register_period_constraints == 1:  # this is a flag, not a numeric value
            model.add_constraints(
                self.energyStorageSystem[i]
                == self.energyStorageSystem[i - (day_node - 1)]  # 1+i-day_node
                for i in range(
                    day_node - 1, self.num_hour, day_node
                )  # what is the day_node? # start, stop, step (23, 24, 24)?
            )
        else:  # what else?
            # 初始值
            model.add_constraint(
                self.energyStorageSystem[0]
                == self.energyStorageSystem_init * self.energyStorageSystem_device
            )
            # 两天之间的连接
            model.add_constraints(
                self.energyStorageSystem[i]
                == self.energyStorageSystem[i - 1]
                + (
                    self.power_energyStorageSystem_charge[i] * self.efficiency
                    - self.power_energyStorageSystem_discharge[i] / self.efficiency
                )
                * simulationTime
                / 3600
                for i in range(day_node, self.num_hour, day_node)
            )

    def total_cost(self, solution: SolveSolution) -> float:
        """
        Args:
            solution (docplex.mp.solution.SolveSolution): 求解模型的求解结果

        Return:
            购买设备总费用 = 储能系统设备数*储能设备设备价格+功率转化设备数*功率转化设备价格
        """
        return (
            solution.get_value(self.energyStorageSystem_device)
            * self.energyStorageSystem_price
            + solution.get_value(self.powerConversionSystem_device)
            * self.powerConversionSystem_price
        )


# 可变容量储能
class EnergyStorageSystemVariable(IntegratedEnergySystem):
    """
    可变容量储能类,适用于储能机组
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        energyStorageSystem_device_max: float,
        energyStorageSystem_price: float,
        powerConversionSystem_price: float,
        conversion_rate_max: float,
        efficiency: float,
        energyStorageSystem_init: float,
        stateOfCharge_min: float,
        stateOfCharge_max: float,
        device_name: str = "energyStorageSystem_variable",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            energyStorageSystem_device_max (float): 储能系统设备机组最大装机量
            energyStorageSystem_price (float): 储能装置的购置价格。
            powerConversionSystem_price (float): 储能装置与电网之间的 PCS 转换价格。
            eff (float):储能装置的充放电效率。
            conversion_rate_max (float): 储能装置的最大倍率。
            energyStorageSystem_init (float): 储能装置的初始能量。
            stateOfCharge_min (float):储能装置的最小储能量百分比。
            stateOfCharge_max (float):储能装置的最大储能量百分比。
            device_name (str): 可变容量储能系统机组名称,默认为"energyStorageSystem_variable"
        """
        IntegratedEnergySystem(device_name)
        EnergyStorageSystemVariable.index += 1

        self.energyStorageSystem_device: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, num_hour)],
            name="energyStorageSystemVariable_device{0}".format(
                EnergyStorageSystemVariable.index
            ),
        )
        """
        可变容量储能系统机组等效单位设备数 大于零的实数
        """
        self.power_energyStorageSystem: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, num_hour)],
            lb=-bigNumber,
            name="power_energyStorageSystemVariable{0}".format(
                EnergyStorageSystemVariable.index
            ),
        )
        """
        模型中的连续变量列表,长度为 num_hour,表示每小时储能装置的充放电功率
        """
        # 充电功率
        self.power_energyStorageSystem_charge: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, num_hour)],
            name="power_energyStorageSystemVariable_charge{0}".format(
                EnergyStorageSystemVariable.index
            ),
        )
        """
        模型中的连续变量列表,长度为 num_hour,表示每小时储能装置的充电功率
        """
        # 放电功率
        self.power_energyStorageSystem_discharge: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, num_hour)],
            name="power_energyStorageSystemVariable_discharge{0}".format(
                EnergyStorageSystemVariable.index
            ),
        )
        """
        模型中的连续变量列表,长度为 num_hour,表示每小时储能装置的放电功率
        """
        # 能量
        self.energyStorageSystem: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, num_hour)],
            name="energyStorageSystemVariable{0}".format(
                EnergyStorageSystemVariable.index
            ),
        )
        """
        模型中的连续变量列表,长度为 num_hour,表示每小时储能装置的能量
        """
        self.energyStorageSystem_device_max = energyStorageSystem_device_max
        self.energyStorageSystem_price = energyStorageSystem_price
        self.powerConversionSystem_price = powerConversionSystem_price
        self.num_hour = num_hour
        self.powerConversionSystem_device: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, num_hour)],
            name="powerConversionSystem_deviceVariable{0}".format(
                EnergyStorageSystemVariable.index
            ),
        )  # powerConversionSystem
        """
        模型中的连续变量,表示 PCS 的容量
        """
        # paradox? redundancy? both charge and discharge?
        self.charge_flag: List[BinaryVarType] = model.binary_var_list(
            [i for i in range(0, num_hour)],
            name="batteryEnergyStorageSystemVariable_charge_flag{0}".format(
                EnergyStorageSystemVariable.index
            ),
        )  # 充电
        """
        模型中的二元变量列表,长度为 num_h,表示每小时储能装置是否处于充电状态。
        """
        self.discharge_flag: List[BinaryVarType] = model.binary_var_list(
            [i for i in range(0, num_hour)],
            name="batteryEnergyStorageSystemVariable_discharge_flag{0}".format(
                EnergyStorageSystemVariable.index
            ),
        )  # 放电
        """
        模型中的二元变量列表,长度为 num_h,表示每小时储能装置是否处于放电状态。
        """
        # 效率
        self.efficiency = efficiency
        self.conversion_rate_max = conversion_rate_max  # conversion rate? charge rate?
        self.energyStorageSystem_init = energyStorageSystem_init
        self.stateOfCharge_min = stateOfCharge_min
        self.stateOfCharge_max = stateOfCharge_max

    def constraints_register(
        self, model: Model, register_period_constraints=1, day_node=24
    ):
        """
        定义机组内部约束

        1. 机组设备数大于等于0
        2. 机组设备总数不得大于最大装机量
        3. 可变容量储能装置功率转化率约束:储能系统设备*储能装置的最大倍率大于等于功率转化系统设备,且功率转化系统设备大于等于0
        4. 充电功率和放电功率之间的关系:储能系统功率=-充电功率+放电功率
        5. 充电功率约束:充电功率大于等于0,小于等于功率转化系统设备,小于等于充电电状态*bigNumber
        6. 放电功率约束:放电功率大于等于0,于等于功率转化系统设备,小于等于放电状态*bigNumber
        7. 充电功率和放电功率二选一
        8. 储能量守恒约束:储能系统能量=上一时段储能量+(当前时段充电*效率-当前时段放电/效率)*simulationTime/3600
        9. 最大和最小储能量约束:储能设备数*储能装置的最小储能量百分比≦储能系统能量≦储能设备数*储能装置的最大储能量百分比
        10. 如果regester_period_constraints参数为1,表示将两天之间的储能量连接约束为切断;如果regester_period_constraints参数不为1,表示将两天之间的储能量连接约束为连续。(这里搞不懂啥意思)
        11. 这里面有两个初始化搞不懂


        Args:
            model (docplex.mp.model.Model): 求解模型实例
            register_period_constraints (int):注册周期约束为1
            day_node (int):一天时间节点为24
        """
        bigNumber = 1e10
        irange = range(0, self.num_hour)
        model.add_constraints(
            self.energyStorageSystem_device[i] <= self.energyStorageSystem_device_max
            for i in irange
        )
        model.add_constraints(self.energyStorageSystem_device[i] >= 0 for i in irange)
        model.add_constraints(
            self.energyStorageSystem_device[i] * self.conversion_rate_max
            >= self.powerConversionSystem_device[i]
            for i in irange
        )
        model.add_constraints(self.powerConversionSystem_device[i] >= 0 for i in irange)
        # 功率拆分
        model.add_constraints(
            self.power_energyStorageSystem[i]
            == -self.power_energyStorageSystem_charge[i]
            + self.power_energyStorageSystem_discharge[i]
            for i in irange
        )

        model.add_constraints(
            self.power_energyStorageSystem_charge[i] >= 0 for i in irange
        )
        model.add_constraints(
            self.power_energyStorageSystem_charge[i] <= self.charge_flag[i] * bigNumber
            for i in irange
        )
        model.add_constraints(
            self.power_energyStorageSystem_charge[i]
            <= self.powerConversionSystem_device[i]
            for i in irange
        )

        model.add_constraints(
            self.power_energyStorageSystem_discharge[i] >= 0 for i in irange
        )
        model.add_constraints(
            self.power_energyStorageSystem_discharge[i]
            <= self.discharge_flag[i] * bigNumber
            for i in irange
        )
        model.add_constraints(
            self.power_energyStorageSystem_discharge[i]
            <= self.powerConversionSystem_device[i]
            for i in irange
        )

        model.add_constraints(
            self.charge_flag[i] + self.discharge_flag[i] == 1 for i in irange
        )
        for day in range(1, int(self.num_hour / day_node) + 1):
            model.add_constraints(
                self.energyStorageSystem[i]
                == self.energyStorageSystem[i - 1]
                + (
                    self.power_energyStorageSystem_charge[i] * self.efficiency
                    - self.power_energyStorageSystem_discharge[i] / self.efficiency
                )
                * simulationTime
                / 3600
                for i in range(1 + day_node * (day - 1), day_node * day)
            )
        model.add_constraints(
            self.energyStorageSystem[0]
            == self.energyStorageSystem_init * self.energyStorageSystem_device[i]
            for i in range(1, self.num_hour)
        )

        model.add_constraints(
            self.energyStorageSystem[i]
            <= self.energyStorageSystem_device[i] * self.stateOfCharge_max
            for i in range(1, self.num_hour)
        )
        model.add_constraints(
            self.energyStorageSystem[i]
            >= self.energyStorageSystem_device[i] * self.stateOfCharge_min
            for i in range(1, self.num_hour)
        )

        # 两天之间直接割裂,没有啥关系
        if register_period_constraints == 1:  # register??
            model.add_constraints(
                self.energyStorageSystem[i]
                == self.energyStorageSystem[i - (day_node - 1)]
                for i in range(day_node - 1, self.num_hour, day_node)
            )
        else:
            # 初始值
            model.add_constraint(
                self.energyStorageSystem[0]
                == self.energyStorageSystem_init * self.energyStorageSystem_device
            )
            # 两天之间的连接
            model.add_constraints(
                self.energyStorageSystem[i]
                == self.energyStorageSystem[i - 1]
                + (
                    self.power_energyStorageSystem_charge[i] * self.efficiency
                    - self.power_energyStorageSystem_discharge[i] / self.efficiency
                )
                * simulationTime
                / 3600
                for i in range(day_node, self.num_hour, day_node)
            )


# troughPhotoThermal
class TroughPhotoThermal(IntegratedEnergySystem):
    """
    槽式光热类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        troughPhotoThermal_device_max,
        troughPhotoThermal_price,
        troughPhotoThermalSolidHeatStorage_price,  # (csgrgtxr是啥)
        intensityOfIllumination0 np.ndarray,
        efficiency: float,
        device_name="troughPhotoThermal",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            troughPhotoThermal_device_max(float): 槽式光热设备机组最大装机量
            troughPhotoThermal_price(float): 槽式光热设备的购置价格。
            troughPhotoThermalSolidHeatStorage_price(float): 槽式光热储能设备价格
            intensityOfIllumination0 np.ndarray:24小时光照强度
            eff(float):效率
            device_name (str): 槽式光热机组名称,默认为"troughPhotoThermal"
        """
        IntegratedEnergySystem(device_name)
        TroughPhotoThermal.index += 1
        self.num_hour = num_hour
        self.troughPhotoThermal_device: ContinuousVarType = model.continuous_var(
            name="troughPhotoThermal_device{0}".format(TroughPhotoThermal.index)
        )
        self.power_troughPhotoThermal: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_troughPhotoThermal{0}".format(TroughPhotoThermal.index),
        )
        self.power_troughPhotoThermal_steam: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_troughPhotoThermal_steam{0}".format(TroughPhotoThermal.index),
        )
        self.troughPhotoThermal_device_max = troughPhotoThermal_device_max
        self.troughPhotoThermalSolidHeatStorage_device_max = (
            troughPhotoThermal_device_max * 6
        )
        self.troughPhotoThermal_price = troughPhotoThermal_price
        self.troughPhotoThermalSolidHeatStorage_price = (
            troughPhotoThermalSolidHeatStorage_price
        )
        self.intensityOfIllumination = (
            intensityOfIllumination0  # intensityOfIllumination
        )
        self.annualized: ContinuousVarType = model.continuous_var(
            name="troughPhotoThermal_annualized{0}".format(TroughPhotoThermal.index)
        )
        self.efficiency = efficiency

        self.troughPhotoThermalSolidHeatStorage_device = EnergyStorageSystem(
            num_hour,
            model,
            self.troughPhotoThermalSolidHeatStorage_device_max,
            self.troughPhotoThermalSolidHeatStorage_price,
            powerConversionSystem_price=100,
            conversion_rate_max=2,  # change?
            efficiency=0.9,
            energyStorageSystem_init=1,
            stateOfCharge_min=0,
            stateOfCharge_max=1,
        )

    def constraints_register(self, model: Model):
        hourRange = range(0, self.num_hour)
        self.troughPhotoThermalSolidHeatStorage_device.constraints_register(model)
        model.add_constraint(self.troughPhotoThermal_device >= 0)
        model.add_constraint(
            self.troughPhotoThermal_device <= self.troughPhotoThermal_device_max
        )
        model.add_constraints(self.power_troughPhotoThermal[h] >= 0 for h in hourRange)
        model.add_constraints(
            self.power_troughPhotoThermal[h]
            <= self.troughPhotoThermal_device
            * self.intensityOfIllumination[h]
            * self.efficiency
            for h in hourRange
        )  # 与天气相关
        model.add_constraints(
            self.power_troughPhotoThermal[h]
            + self.troughPhotoThermalSolidHeatStorage_device.power_energyStorageSystem[
                h
            ]
            == self.power_troughPhotoThermal_steam[h]
            for h in hourRange
        )  # troughPhotoThermal系统产生的highTemperature
        model.add_constraints(
            0 <= self.power_troughPhotoThermal_steam[h] for h in hourRange
        )  # 约束能量不能倒流
        model.add_constraint(
            self.annualized
            == self.troughPhotoThermal_device * self.troughPhotoThermal_price / 15
            + self.troughPhotoThermalSolidHeatStorage_device.annualized
        )


# CombinedHeatAndPower设备
# 输入:
# TODO: fix the name issue of CHP devices
class CombinedHeatAndPower(IntegratedEnergySystem):
    """
    燃气轮机类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        combinedHeatAndPower_num_max,
        combinedHeatAndPower_price,
        gas_price,
        combinedHeatAndPower_single_device,
        power_to_heat_ratio,  # drratio?
        device_name="combinedHeatAndPower",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            combinedHeatAndPower_num_max (int):表示燃气轮机的最大数量。
            combinedHeatAndPower_price (float):表示燃气轮机的单价。
            gas_price (float):表示燃气的单价。
            combinedHeatAndPower_single_set (float):表示每台燃气轮机的装机容量。
            drratio (float):表示燃气轮机的热电比。
            device_name (str): 燃气轮机机组名称,默认为"combinedHeatAndPower"
        """
        IntegratedEnergySystem(device_name)
        CombinedHeatAndPower.index += 1
        self.num_hour = num_hour
        self.combinedHeatAndPower_device: ContinuousVarType = model.continuous_var(
            name="combinedHeatAndPower_device{0}".format(CombinedHeatAndPower.index)
        )
        """
        实数型,表示燃气轮机的总装机容量
        """
        self.power_combinedHeatAndPower: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_combinedHeatAndPower{0}".format(CombinedHeatAndPower.index),
        )
        """
        实数型列表,表示燃气轮机在每个时段的发电量
        """
        self.heat_combinedHeatAndPower: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="heat_combinedHeatAndPower{0}".format(CombinedHeatAndPower.index),
        )
        """
        实数型列表,表示燃气轮机在每个时段的供暖热水量
        """
        self.gas_combinedHeatAndPower: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="gas_combinedHeatAndPower{0}".format(CombinedHeatAndPower.index),
        )  # 时时耗气量? 时时是什么意思 实时？
        """
        实数型列表,表示燃气轮机在每个时段的耗气量
        """
        self.combinedHeatAndPower_price = combinedHeatAndPower_price
        self.gas_price = gas_price
        self.combinedHeatAndPower_open_flag: List[
            BinaryVarType
        ] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="combinedHeatAndPower_open_flag{0}".format(CombinedHeatAndPower.index),
        )
        """
        二元变量列表,表示燃气轮机在每个时段是否启动
        """
        self.wasteGasAndHeat_water_flag: BinaryVarType = model.binary_var(
            name="wasteGasAndHeat_water_flag{0}".format(CombinedHeatAndPower.index)
        )
        """
        二元变量,表示燃气轮机是否用于供暖热水
        """
        self.wasteGasAndHeat_steam_flag: BinaryVarType = model.binary_var(
            name="wasteGasAndHeat_steam_flag{0}".format(CombinedHeatAndPower.index)
        )
        """
        二元变量,表示燃气轮机是否用于供热蒸汽
        """
        # 机组数量
        self.combinedHeatAndPower_run_num: List[
            IntegerVarType
        ] = model.integer_var_list(
            [i for i in range(0, self.num_hour)],
            name="combinedHeatAndPower_run_num{0}".format(CombinedHeatAndPower.index),
        )
        """
        整数型列表,表示每个时段启动的燃气轮机数量
        """
        self.combinedHeatAndPower_num: IntegerVarType = model.integer_var(
            name="combinedHeatAndPower_num{0}".format(CombinedHeatAndPower.index)
        )
        """
        整数型,表示燃气轮机数量
        """
        self.annualized: ContinuousVarType = model.continuous_var(
            name="combinedHeatAndPower_annualized{0}".format(CombinedHeatAndPower.index)
        )
        """
        实数型,表示燃气轮机年化投资成本
        """
        self.gas_cost: ContinuousVarType = model.continuous_var(
            name="CombinedHeatAndPower_gas_cost{0}".format(CombinedHeatAndPower.index)
        )  # 燃气费用统计
        """
        实数型,表示燃气费用
        """
        self.combinedHeatAndPower_num_max = combinedHeatAndPower_num_max
        self.combinedHeatAndPower_single_device = combinedHeatAndPower_single_device
        self.combinedHeatAndPower_limit_down_ratio = (
            0.2  # ? devices cannot be turned down more than 20% ? what is this?
        )

        self.power_to_heat_ratio = power_to_heat_ratio

        # arbitrary settings
        self.gasTurbineSystem_device = Exchanger(
            self.num_hour,
            model,
            self.combinedHeatAndPower_device * 0.5,
            device_price=300,
            k=0,
        )
        """
        方法内部还创建了三个 "Exchanger" 对象,分别用于模拟燃气轮机的三种应用方式（供暖热水、供暖蒸汽、烟气余热回收）。这些对象的定义在类内部,它们的参数包括时间步数、数学模型实例、可用的设备数量、设备单价和换热系数等。
        """

        self.wasteGasAndHeat_water_device = Exchanger(
            self.num_hour,
            model,
            self.combinedHeatAndPower_device * 0.5,
            device_price=300,
            k=0,
        )

        self.wasteGasAndHeat_steam_device = Exchanger(
            self.num_hour,
            model,
            self.combinedHeatAndPower_device * 0.5,
            device_price=300,
            k=0,
        )

    def constraints_register(self, model: Model):
        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 燃气轮机装机量=燃气轮机机组数*燃气轮机的装机容量
        3. 每个燃气轮机的热功率必须大于等于燃气轮机的最小热功率
        4. 每个燃气轮机的热功率必须小于等于燃气轮机的总热功率
        5. 每个燃气轮机的热功率必须小于等于燃气轮机开启时的热功率
        6. 确定每个时段燃气轮机开启的台数,并且每个时段燃气轮机开启的总功率必须等于燃气轮机的总热功率
        7. 燃气轮机的运行台数必须在0到总台数之间
        8. 燃气轮机的热功率必须等于燃气轮机的电功率乘以热电比
        9. 燃气轮机的燃气消耗量必须等于燃气轮机的总热功率除以燃气发电机组的热效率 3.5
        10. 所有时间段的天燃气消费和天燃气价格的乘积相加来计算总的天燃气成本
        11. 确保了与余气余热系统的热交换只使用一种类型(热水或蒸汽)
        12. 根据二元决策变量wasteGasAndHeat_water_flag和一个大常数bigM来设定与余气余热系统的最大热交换能力。如果wasteGasAndHeat_water_flag为0,该约束就会失去作用。
        13. 根据二元决策变量wasteGasAndHeat_steam_flag和一个大常数bigM来设定蒸汽与余气余热系统的最大热交换能力。如果wasteGasAndHeat_steam_flag为0,该约束就会失去作用。
        14. GTS系统的最大热交换能力限制在所有时间段内热电联产机组额定热输出的50%
        15. 余气余热热水系统的最大换热量限制为所有时段热电联产机组额定热出力的50%
        16. 余气余热蒸汽系统的最大换热能力限制为所有时段热电联产机组额定热出力的50%
        17. 计算年总成本,包括运行CHP机组、GTS系统和YQYR系统的成本以及燃气成本。计算的依据是CHP机组的数量、其额定功率出力、CHP的单位成本、一年中的小时数等相关参数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """

        hourRange = range(0, self.num_hour)
        model.add_constraint(self.combinedHeatAndPower_num >= 0)
        model.add_constraint(
            self.combinedHeatAndPower_num <= self.combinedHeatAndPower_num_max
        )

        model.add_constraint(
            self.combinedHeatAndPower_device
            == self.combinedHeatAndPower_num * self.combinedHeatAndPower_single_device
        )
        model.add_constraints(
            self.combinedHeatAndPower_open_flag[h]
            * self.combinedHeatAndPower_single_device
            * self.combinedHeatAndPower_limit_down_ratio
            <= self.power_combinedHeatAndPower[h]
            for h in hourRange
        )
        # power_combinedHeatAndPower(1, h) <= combinedHeatAndPower_device * combinedHeatAndPower_open_flag(1, h) % combinedHeatAndPower功率限制, 采用线性化约束,有以下等效:
        model.add_constraints(
            self.power_combinedHeatAndPower[h] <= self.combinedHeatAndPower_device
            for h in hourRange
        )

        model.add_constraints(
            self.power_combinedHeatAndPower[h]
            <= self.combinedHeatAndPower_open_flag[h] * bigNumber
            for h in hourRange
        )
        # power_combinedHeatAndPower[h]>= 0
        # power_combinedHeatAndPower(1, h) >= combinedHeatAndPower_device - (1 - combinedHeatAndPower_open_flag[h]) * bigNumber
        model.add_constraints(
            self.combinedHeatAndPower_run_num[h]
            * self.combinedHeatAndPower_single_device
            >= self.power_combinedHeatAndPower[h]
            for h in hourRange
        )  # 确定CombinedHeatAndPower开启台数
        model.add_constraints(
            self.combinedHeatAndPower_run_num[h]
            * self.combinedHeatAndPower_single_device
            <= self.power_combinedHeatAndPower[h]
            + self.combinedHeatAndPower_single_device
            + 1
            for h in hourRange
        )  # 确定CombinedHeatAndPower开启台数
        model.add_constraints(
            0 <= self.combinedHeatAndPower_run_num[h] for h in hourRange
        )
        model.add_constraints(
            self.combinedHeatAndPower_run_num[h] <= self.combinedHeatAndPower_num
            for h in hourRange
        )
        model.add_constraints(
            self.power_combinedHeatAndPower[h]
            * self.power_to_heat_ratio  # power * power_to_heat_coefficient = heat
            == self.heat_combinedHeatAndPower[h]
            for h in hourRange
        )
        model.add_constraints(
            self.gas_combinedHeatAndPower[h] == self.power_combinedHeatAndPower[h] / 3.5
            for h in hourRange
        )

        self.gas_cost = model.sum(
            self.gas_combinedHeatAndPower[h] * self.gas_price[h] for h in hourRange
        )  # 统计燃气费用
        #
        model.add_constraint(
            self.wasteGasAndHeat_water_flag + self.wasteGasAndHeat_steam_flag == 1
        )
        model.add_constraint(
            self.wasteGasAndHeat_water_device.exchanger_device
            <= self.wasteGasAndHeat_water_flag * bigNumber
        )
        model.add_constraint(
            self.wasteGasAndHeat_steam_device.exchanger_device
            <= self.wasteGasAndHeat_steam_flag * bigNumber
        )
        model.add_constraints(
            self.gasTurbineSystem_device.heat_exchange[h]
            <= self.heat_combinedHeatAndPower[h] * 0.5
            for h in hourRange
        )
        model.add_constraints(
            self.wasteGasAndHeat_water_device.heat_exchange[h]
            <= self.heat_combinedHeatAndPower[h] * 0.5
            for h in hourRange
        )
        model.add_constraints(
            self.wasteGasAndHeat_steam_device.heat_exchange[h]
            <= self.heat_combinedHeatAndPower[h] * 0.5
            for h in hourRange
        )

        model.add_constraint(
            self.annualized
            == self.combinedHeatAndPower_num
            * self.combinedHeatAndPower_single_device
            * self.combinedHeatAndPower_price
            / 15
            + self.gasTurbineSystem_device.annualized
            + self.wasteGasAndHeat_water_device.annualized
            + self.wasteGasAndHeat_steam_device.annualized
            + self.gas_cost * 8760 / self.num_hour
        )


# 燃气锅炉:蒸汽,hotWater
class GasBoiler(IntegratedEnergySystem):
    """
    燃气锅炉类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        gasBoiler_device_max:float,
        gasBoiler_price:float,
        gas_price:np.ndarray,
        efficiency: float,
        device_name:str="gasBoiler",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            gasBoiler_device_max (float): 表示燃气锅炉的最大数量。
            gasBoiler_price (float): 表示燃气锅炉的单价。
            gas_price (np.ndarray): 表示燃气的单价。
            efficiency (float): 燃气锅炉的热效率
            device_name (str): 燃气锅炉机组名称,默认为"gasBoiler"
        """
        IntegratedEnergySystem(device_name)
        GasBoiler.index += 1
        self.num_hour = num_hour
        self.gasBoiler_device: ContinuousVarType = model.continuous_var(
            name="gasBoiler_device{0}".format(GasBoiler.index)
        )
        """
        燃气锅炉机组等效单位设备数 大于零的实数
        """
        self.heat_gasBoiler: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="heat_gasBoiler{0}".format(GasBoiler.index),
        )
        """
        连续变量列表,表示燃气锅炉在每个时段的热功率
        """
        self.gas_gasBoiler: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="gas_gasBoiler{0}".format(GasBoiler.index),
        )  # 时时耗气量
        """
        连续变量列表,表示燃气锅炉在每个时段的燃气消耗量
        """
        self.gasBoiler_device_max = gasBoiler_device_max
        self.gasBoiler_price = gasBoiler_price
        self.gas_price = gas_price
        self.efficiency = efficiency
        self.gas_cost: ContinuousVarType = model.continuous_var(
            name="gasBoiler_gas_cost{0}".format(GasBoiler.index)
        )
        """
        连续变量,表示燃气费用
        """
        self.annualized: ContinuousVarType = model.continuous_var(
            name="gasBoiler_annualized{0}".format(GasBoiler.index)
        )
        """
        连续变量,表示燃气锅炉的年化费用
        """

    def constraints_register(self, model: Model):
        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦燃气锅炉的热功率≦燃气锅炉运行量
        3. 燃气锅炉的燃气消耗量等于热功率除以热效率乘以一个常数（这个常数是热功率和燃气消耗量之间的转化系数）
        4. 燃气锅炉的总燃气成本等于燃气消耗量乘以燃气价格之和
        5. 燃气锅炉的总年化成本等于投资成本和燃气成本之和

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        hourRange = range(0, self.num_hour)
        model.add_constraint(self.gasBoiler_device >= 0)
        model.add_constraint(self.gasBoiler_device <= self.gasBoiler_device_max)
        model.add_constraints(self.heat_gasBoiler[h] >= 0 for h in hourRange)
        model.add_constraints(
            self.heat_gasBoiler[h] <= self.gasBoiler_device for h in hourRange
        )  # 天燃气蒸汽锅炉
        model.add_constraints(
            self.gas_gasBoiler[h] == self.heat_gasBoiler[h] / (10 * self.efficiency)
            for h in hourRange
        )
        self.gas_cost = model.sum(
            self.gas_gasBoiler[h] * self.gas_price[h] for h in hourRange
        )
        model.add_constraint(
            self.annualized
            == self.gasBoiler_device * self.gasBoiler_price / 15
            + self.gas_cost * 8760 / self.num_hour
        )


# electricBoiler
class ElectricBoiler(IntegratedEnergySystem):
    """
    电锅炉类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        electricBoiler_device_max:float,
        electricBoiler_price:float,
        electricity_price:np.ndarray,
        efficiency: float,
        device_name:str="electricBoiler",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            electricBoiler_device_max (float): 表示电锅炉的最大数量。
            electricBoiler_price (float): 表示电锅炉的单价。
            electricity_price (np.ndarray): 表示电的单价。
            efficiency (float): 电锅炉的热效率
            device_name (str): 电锅炉机组名称,默认为"electricBoiler"
        """
        IntegratedEnergySystem(device_name)
        ElectricBoiler.index += 1
        self.num_hour = num_hour
        self.electricBoiler_device: ContinuousVarType = model.continuous_var(
            name="electricBoiler_device{0}".format(ElectricBoiler.index)
        )
        """
        电锅炉机组等效单位设备数 大于零的实数
        """
        self.heat_electricBoiler: List[
            ContinuousVarType
        ] = model.continuous_var_list(  # h? heat?
            [i for i in range(0, self.num_hour)],
            name="heat_electricBoiler{0}".format(ElectricBoiler.index),
        )
        """
        连续变量列表,表示电锅炉在每个时段的热功率
        """
        self.electricity_electricBoiler: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="electricity_electricBoiler{0}".format(ElectricBoiler.index),
        )  # 时时耗气量
        """
        连续变量列表,表示电锅炉在每个时段的电消耗量
        """
        self.gas_device_max = electricBoiler_device_max
        self.electricBoiler_price = electricBoiler_price
        self.electricity_price = electricity_price
        self.efficiency = efficiency
        self.electricity_cost: ContinuousVarType = model.continuous_var(
            name="electricity_cost{0}".format(ElectricBoiler.index)
        )
        """
        连续变量,表示用电费用
        """
        self.annualized: ContinuousVarType = model.continuous_var(
            name="electricBoiler_annualized{0}".format(ElectricBoiler.index)
        )
        """
        连续变量,表示电锅炉的年化费用
        """

    def constraints_register(self, model: Model):
        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦电锅炉的热功率≦电锅炉运行量
        3. 燃气锅炉的电消耗量等于热功率除以热效率
        4. 燃气锅炉的总耗电成本等于电消耗量乘以电价格之和
        5. 燃气锅炉的总年化成本等于投资成本和用电成本之和

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        hourRange = range(0, self.num_hour)
        model.add_constraint(self.electricBoiler_device >= 0)
        model.add_constraint(self.electricBoiler_device <= self.gas_device_max)
        model.add_constraints(self.heat_electricBoiler[h] >= 0 for h in hourRange)
        model.add_constraints(
            self.heat_electricBoiler[h] <= self.electricBoiler_device for h in hourRange
        )  # 天燃气蒸汽锅炉
        model.add_constraints(
            self.electricity_electricBoiler[h]
            == self.heat_electricBoiler[h] / self.efficiency
            for h in hourRange
        )
        self.electricity_cost = model.sum(
            self.electricity_electricBoiler[h] * self.electricity_price[h]
            for h in hourRange
        )
        model.add_constraint(
            self.annualized
            == self.electricBoiler_device * self.electricBoiler_price / 15
            + self.electricity_cost * 8760 / self.num_hour
        )


class Exchanger(IntegratedEnergySystem):
    """
    热交换器类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_max:float,
        device_price:float,
        k:float,  # 传热系数
        device_name:str="exchanger",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_max (float): 表示热交换器的最大数量。
            device_price (float): 表示热交换器的单价。
            k (float): 传热系数
            device_name (str): 热交换器机组名称,默认为"exchanger"
        """
        IntegratedEnergySystem(device_name)
        # k 传热系数
        Exchanger.index += 1
        self.num_hour = num_hour
        self.exchanger_device: ContinuousVarType = model.continuous_var(
            name="exchanger_device{0}".format(Exchanger.index)
        )
        """
        热交换器机组等效单位设备数 大于零的实数
        """
        self.annualized: ContinuousVarType = model.continuous_var(
            name="exchanger_annualized{0}".format(Exchanger.index)
        )
        """
        连续变量,表示热交换器的年化费用
        """
        self.device_price = device_price
        self.exchanger_device_max = device_max
        self.heat_exchange: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="heat_exchanger{0}".format(Exchanger.index),
        )
        """
        连续变量列表,表示热交换器的每小时热交换量
        """

    def constraints_register(self, model: Model):
        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦热交换器的热功率≦热交换器运行量
        3. 热交换器的总年化成本等于热交换器设备数*设备价格/15

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        hourRange = range(0, self.num_hour)
        model.add_constraint(self.exchanger_device >= 0)
        model.add_constraint(self.exchanger_device <= self.exchanger_device_max)
        model.add_constraints(self.heat_exchange[h] >= 0 for h in hourRange)
        model.add_constraints(
            self.heat_exchange[h] <= self.exchanger_device for h in hourRange
        )  # 天燃气蒸汽锅炉
        model.add_constraint(
            self.annualized == self.exchanger_device * self.device_price / 15
        )


class AirHeatPump(IntegratedEnergySystem):
    """
    热泵类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_max:float,
        device_price:float,
        electricity_price:np.array,
        device_name="air_heat_pump",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_max (float): 表示热泵的最大数量。
            device_price (float): 表示热泵的单价。
            electricity_price (np.array): 电价
            device_name (str): 热泵机组名称,默认为"air_heat_pump"
        """
        IntegratedEnergySystem(device_name)
        self.num_hour = num_hour
        AirHeatPump.index += 1
        self.electricity_price = electricity_price
        self.heatPump_device: ContinuousVarType = model.continuous_var(
            name="heatPump_device{0}".format(AirHeatPump.index)
        )
        """
        热泵机组等效单位设备数 大于零的实数
        """
        self.annualized: ContinuousVarType = model.continuous_var(
            name="AirHeatPumpower_annualized{0}".format(AirHeatPump.index)
        )
        """
        连续变量,表示热泵的年化费用
        """
        self.electricity_cost: ContinuousVarType = model.continuous_var(
            name="AirHeatPumpower_electricity_cost{0}".format(AirHeatPump.index)
        )
        """
        连续变量,表示热泵的电价成本
        """
        self.device_price = device_price
        self.device_max = device_max
        self.power_heatPump_cool: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_heatPump_cool{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示热泵在每个时段的制冷功率
        """
        self.cool_heatPump_out: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="cool_heatPump_out{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示热泵在每个时段的制冷出口温度
        """
        self.heatPump_cool_flag: List[BinaryVarType] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="heatPump_cool_flag{0}".format(AirHeatPump.index),
        )
        """
        二元变量列表,表示热泵在每个时段的制冷状态
        """

        self.power_heatPump_xcool: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_heatPump_xcool{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示热泵在每个时段的除湿功率
        """
        self.xcool_heatPump_out: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="xcool_heatPump_out{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示热泵在每个时段的除湿出口温度
        """

        self.heatPump_xcool_flag: List[BinaryVarType] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="heatPump_xcool_flag{0}".format(AirHeatPump.index),
        )
        """
        二元变量列表,表示热泵在每个时段的除湿状态
        """
        self.power_heatPump_heat: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_heatPump_heat{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示热泵在每个时段的制热功率
        """
        self.heat_heatPump_out: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="heat_heatPump_out{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示热泵在每个时段的制热出口温度
        """
        self.heatPump_heat_flag: List[BinaryVarType] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="heatPump_heat_flag{0}".format(AirHeatPump.index),
        )
        """
        二元变量列表,表示热泵在每个时段的制热状态
        """
        self.power_heatPump_xheat: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_heatPump_xheat{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示热泵在每个时段的加湿功率
        """
        self.xheat_heatPump_out: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="xheat_heatPump_out{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示热泵在每个时段的加湿出口温度
        """
        self.heatPump_xheat_flag: List[BinaryVarType] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="heatPump_xheat_flag{0}".format(AirHeatPump.index),
        )
        """
        二元变量列表,表示热泵在每个时段的加湿状态
        """
        self.electricity_heatPump: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="electricity_heatPump{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示热泵在每个时段的用电量
        """
        self.power_heatPump: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_heatPump{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示热泵在每个时段的总功率
        """

        # TODO: unclear meaning of "xcool" and "xheat"
        self.coefficientOfPerformance_heatPump_cool = 3  # 表示该组件制冷时的性能系数
        self.coefficientOfPerformance_heatPump_xcool = 3  # 表示该组件除湿时的性能系数
        self.coefficientOfPerformance_heatPump_heat = 3  # 表示该组件供热时的性能系数
        self.coefficientOfPerformance_heatPump_xheat = 3  # 表示该组件加湿时的性能系数

    def constraints_register(self, model: Model):
        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦热泵的制冷功率≦热泵制冷出口温度*热泵设备数/100,0≦热泵的制冷功率≦热泵制冷状态*bigNumber
        3. 0≦热泵的除湿功率≦热泵除湿出口温度*热泵设备数/100,0≦热泵的除湿功率≦热泵除湿状态*bigNumber
        4. 0≦热泵的制热功率≦热泵制热出口温度*热泵设备数/100,0≦热泵的制热功率≦热泵制热状态*bigNumber
        5. 0≦热泵的加湿功率≦热泵加湿出口温度*热泵设备数/100,0≦热泵的加湿功率≦热泵加湿状态*bigNumber
        6. 制冷状态+除湿状态+制热状态+加湿状态=1
        7. 热泵用电量=设备制冷功率/制冷性能系数+设备除湿功率/除湿性能系数+设备制热功率/制热性能系数+设备加湿功率/加湿性能系数
        8. 热泵总功率=制冷功率+除湿功率+制热功率+加湿功率
        9. 用电成本=每个时刻(设备用电量*电价)的总和
        10. 热泵的总年化成本=热泵设备数*设备价格/15+用电成本*8760/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        hourRange = range(0, self.num_hour)
        model.add_constraint(0 <= self.heatPump_device)
        model.add_constraint(self.heatPump_device <= self.device_max)

        model.add_constraints(0 <= self.power_heatPump_cool[h] for h in hourRange)
        model.add_constraints(
            self.power_heatPump_cool[h]
            <= self.cool_heatPump_out[h] * self.heatPump_device / 100
            for h in hourRange
        )
        model.add_constraints(
            self.power_heatPump_cool[h] <= bigNumber * self.heatPump_cool_flag[h]
            for h in hourRange
        )

        model.add_constraints(0 <= self.power_heatPump_xcool[h] for h in hourRange)
        model.add_constraints(
            self.power_heatPump_xcool[h]
            <= self.xcool_heatPump_out[h] * self.heatPump_device / 100
            for h in hourRange
        )
        model.add_constraints(
            self.power_heatPump_xcool[h] <= bigNumber * self.heatPump_xcool_flag[h]
            for h in hourRange
        )

        model.add_constraints(0 <= self.power_heatPump_heat[h] for h in hourRange)
        model.add_constraints(
            self.power_heatPump_heat[h]
            <= self.heat_heatPump_out[h] * self.heatPump_device / 100
            for h in hourRange
        )
        model.add_constraints(
            self.power_heatPump_heat[h] <= bigNumber * self.heatPump_heat_flag[h]
            for h in hourRange
        )

        model.add_constraints(0 <= self.power_heatPump_xheat[h] for h in hourRange)
        model.add_constraints(
            self.power_heatPump_xheat[h]
            <= self.xheat_heatPump_out[h] * self.heatPump_device / 100
            for h in hourRange
        )
        model.add_constraints(
            self.power_heatPump_xheat[h] <= bigNumber * self.heatPump_xheat_flag[h]
            for h in hourRange
        )

        model.add_constraints(
            self.heatPump_cool_flag[h]
            + self.heatPump_xcool_flag[h]
            + self.heatPump_heat_flag[h]
            + self.heatPump_xheat_flag[h]
            == 1
            for h in hourRange
        )
        model.add_constraints(
            self.electricity_heatPump[h]
            # are you sure you want to subscribe?
            == self.power_heatPump_cool[h]
            / self.coefficientOfPerformance_heatPump_cool  # [h]
            + self.power_heatPump_xcool[h]
            / self.coefficientOfPerformance_heatPump_xcool  # [h]
            + self.power_heatPump_heat[h]
            / self.coefficientOfPerformance_heatPump_heat  # [h]
            + self.power_heatPump_xheat[h]
            / self.coefficientOfPerformance_heatPump_xheat  # [h]
            for h in hourRange
        )
        model.add_constraints(
            self.power_heatPump[h]
            == self.power_heatPump_cool[h]
            + self.power_heatPump_xcool[h]
            + self.power_heatPump_heat[h]
            + self.power_heatPump_xheat[h]
            for h in hourRange
        )

        self.electricity_cost = model.sum(
            self.electricity_heatPump[h] * self.electricity_price[h] for h in hourRange
        )
        # 年化
        model.add_constraint(
            self.annualized
            == self.heatPump_device * self.device_price / 15
            + self.electricity_cost * 8760 / self.num_hour
        )


# waterSourceHeatPumps
class WaterHeatPump(IntegratedEnergySystem):
    """
    水源热泵类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_max,
        device_price,
        electricity_price,
        case_ratio,
        device_name="water_heat_pump",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_max (float): 表示水源热泵的最大数量。
            device_price (float): 表示水源热泵的单价。
            electricity_price (float): 电价
            case_ratio: 不同工况下制热量和制冷量的比值
            device_name (str): 水源热泵机组名称,默认为"water_heat_pump"
        """
        IntegratedEnergySystem(device_name)
        # case_ratio 不同工况下制热量/制冷量的比值
        self.num_hour = num_hour
        WaterHeatPump.index += 1
        self.electricity_price = electricity_price
        self.waterSourceHeatPumps_device: ContinuousVarType = model.continuous_var(
            name="waterSourceHeatPumps_device{0}".format(WaterHeatPump.index)
        )
        """
        水源热泵机组等效单位设备数 大于零的实数
        """
        self.annualized: ContinuousVarType = model.continuous_var(
            name="WaterHeatPumpower_annualized{0}".format(WaterHeatPump.index)
        )
        """
        连续变量,表示水源热泵的年化费用
        """
        self.electricity_cost: ContinuousVarType = model.continuous_var(
            name="WaterHeatPumpower_electricity_sum{0}".format(WaterHeatPump.index)
        )
        """
        连续变量,表示水源热泵的用电成本
        """
        self.device_price = device_price
        self.device_max = device_max
        self.case_ratio = case_ratio

        self.power_waterSourceHeatPumps_cool: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterSourceHeatPumps_cool{0}".format(WaterHeatPump.index),
        )
        """
        连续变量列表,表示每个时刻水源热泵制冷功率
        """

        self.waterSourceHeatPumps_cool_flag: List[
            BinaryVarType
        ] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterSourceHeatPumps_cool_flag{0}".format(WaterHeatPump.index),
        )
        """
        二元变量列表,表示每个时刻水源热泵制冷状态
        """

        self.power_waterSourceHeatPumps_xcool: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterSourceHeatPumps_xcool{0}".format(WaterHeatPump.index),
        )
        """
        连续变量列表,表示每个时刻水源热泵额外制冷功率
        """
        self.waterSourceHeatPumps_xcool_flag: List[
            BinaryVarType
        ] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterSourceHeatPumps_xcool_flag{0}".format(WaterHeatPump.index),
        )
        """
        二元变量列表,表示每个时刻水源热泵额外制冷状态
        """
        self.power_waterSourceHeatPumps_heat: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterSourceHeatPumps_heat{0}".format(WaterHeatPump.index),
        )
        """
        连续变量列表,表示每个时刻水源热泵制热功率
        """
        self.waterSourceHeatPumps_heat_flag: List[
            BinaryVarType
        ] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterSourceHeatPumps_heat_flag{0}".format(WaterHeatPump.index),
        )
        """
        二元变量列表,表示每个时刻水源热泵制热状态
        """
        self.power_waterSourceHeatPumps_xheat: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterSourceHeatPumps_xheat{0}".format(WaterHeatPump.index),
        )
        """
        连续变量列表,表示每个时刻水源热泵额外制热功率
        """
        self.waterSourceHeatPumps_xheat_flag: List[
            BinaryVarType
        ] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterSourceHeatPumps_xheat_flag{0}".format(WaterHeatPump.index),
        )
        """
        二元变量列表,表示每个时刻水源热泵额外制热状态
        """
        self.electricity_waterSourceHeatPumps: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="electricity_waterSourceHeatPumps{0}".format(WaterHeatPump.index),
        )
        """
        连续变量列表,表示每个时刻水源热泵用电量
        """
        self.power_waterSourceHeatPumps: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterSourceHeatPumps{0}".format(WaterHeatPump.index),
        )
        """
        连续变量列表,表示每个时刻水源热泵总功率
        """
        self.coefficientOfPerformance_waterSourceHeatPumps_cool = 5 #制冷性能系数
        self.coefficientOfPerformance_waterSourceHeatPumps_xcool = 5 #额外制冷性能系数
        self.coefficientOfPerformance_waterSourceHeatPumps_heat = 5 #制热性能系数
        self.coefficientOfPerformance_waterSourceHeatPumps_xheat = 5 #额外制热性能系数

    def constraints_register(self, model: Model):
        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦水源热泵的制冷功率≦水源热泵设备数* (况1)制热量/制冷量,0≦水源热泵的制冷功率≦水源热泵制冷状态*bigNumber
        3. 0≦水源热泵的额外制冷功率≦水源热泵设备数* (况2)制热量/制冷量,0≦水源热泵的额外制冷功率≦水源热泵额外制冷状态*bigNumber
        4. 0≦水源热泵的制热功率≦水源热泵设备数* (况3)制热量/制冷量,0≦水源热泵的制热功率≦水源热泵制热状态*bigNumber
        5. 0≦水源热泵的额外制热功率≦水源热泵设备数* (况4)制热量/制冷量,0≦水源热泵的额外制热功率≦水源热泵额外制热状态*bigNumber
        6. 制冷状态+额外制冷状态+制热状态+额外制热状态=1
        7. 水源热泵用电量=设备制冷功率/制冷性能系数+设备额外制冷功率/额外制冷性能系数+设备制热功率/制热性能系数+设备额外制热功率/额外制热性能系数
        8. 热泵总功率=制冷功率+额外制冷功率+制热功率+额外制热功率
        9. 用电成本=每个时刻(设备用电量*电价)的总和
        10. 水源热泵的总年化成本=水源热泵设备数*设备价格/15+用电成本*8760/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        hourRange = range(0, self.num_hour)
        model.add_constraint(0 <= self.waterSourceHeatPumps_device)
        model.add_constraint(self.waterSourceHeatPumps_device <= self.device_max)

        model.add_constraints(
            0 <= self.power_waterSourceHeatPumps_cool[h] for h in hourRange
        )
        model.add_constraints(
            self.power_waterSourceHeatPumps_cool[h]
            <= self.waterSourceHeatPumps_device * self.case_ratio[0]
            for h in hourRange
        )
        model.add_constraints(
            self.power_waterSourceHeatPumps_cool[h]
            <= bigNumber * self.waterSourceHeatPumps_cool_flag[h]
            for h in hourRange
        )

        model.add_constraints(
            0 <= self.power_waterSourceHeatPumps_xcool[h] for h in hourRange
        )
        model.add_constraints(
            self.power_waterSourceHeatPumps_xcool[h]
            <= self.waterSourceHeatPumps_device * self.case_ratio[1]
            for h in hourRange
        )
        model.add_constraints(
            self.power_waterSourceHeatPumps_xcool[h]
            <= bigNumber * self.waterSourceHeatPumps_xcool_flag[h]
            for h in hourRange
        )

        model.add_constraints(
            0 <= self.power_waterSourceHeatPumps_heat[h] for h in hourRange
        )
        model.add_constraints(
            self.power_waterSourceHeatPumps_heat[h]
            <= self.waterSourceHeatPumps_device * self.case_ratio[2]
            for h in hourRange
        )
        model.add_constraints(
            self.power_waterSourceHeatPumps_heat[h]
            <= bigNumber * self.waterSourceHeatPumps_heat_flag[h]
            for h in hourRange
        )

        model.add_constraints(
            0 <= self.power_waterSourceHeatPumps_xheat[h] for h in hourRange
        )
        model.add_constraints(
            self.power_waterSourceHeatPumps_xheat[h]
            <= self.waterSourceHeatPumps_device * self.case_ratio[3]
            for h in hourRange
        )
        model.add_constraints(
            self.power_waterSourceHeatPumps_xheat[h]
            <= bigNumber * self.waterSourceHeatPumps_xheat_flag[h]
            for h in hourRange
        )

        model.add_constraints(
            self.waterSourceHeatPumps_cool_flag[h]
            + self.waterSourceHeatPumps_xcool_flag[h]
            + self.waterSourceHeatPumps_heat_flag[h]
            + self.waterSourceHeatPumps_xheat_flag[h]
            == 1
            for h in hourRange
        )
        model.add_constraints(
            self.electricity_waterSourceHeatPumps[h]
            == self.power_waterSourceHeatPumps_cool[h]
            / self.coefficientOfPerformance_waterSourceHeatPumps_cool
            + self.power_waterSourceHeatPumps_xcool[h]
            / self.coefficientOfPerformance_waterSourceHeatPumps_xcool
            + self.power_waterSourceHeatPumps_heat[h]
            / self.coefficientOfPerformance_waterSourceHeatPumps_heat
            + self.power_waterSourceHeatPumps_xheat[h]
            / self.coefficientOfPerformance_waterSourceHeatPumps_xheat
            for h in hourRange
        )
        model.add_constraints(
            self.power_waterSourceHeatPumps[h]
            == self.power_waterSourceHeatPumps_cool[h]
            + self.power_waterSourceHeatPumps_xcool[h]
            + self.power_waterSourceHeatPumps_heat[h]
            + self.power_waterSourceHeatPumps_xheat[h]
            for h in hourRange
        )

        self.electricity_cost = model.sum(
            self.electricity_waterSourceHeatPumps[h] * self.electricity_price[h]
            for h in hourRange
        )
        # 年化
        model.add_constraint(
            self.annualized
            == self.waterSourceHeatPumps_device * self.device_price / 15
            + self.electricity_cost * 8760 / self.num_hour
        )


# waterCooledScrewMachine
class WaterCooledScrew(IntegratedEnergySystem):
    """
    水冷螺旋机 
    """
    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_max,
        device_price,
        electricity_price,
        case_ratio,
        device_name="water_cooled_screw",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_max (int): 表示水冷螺旋机的最大数量。
            device_price (float): 表示水冷螺旋机的单价。
            electricity_price (float): 电价
            case_ratio: 不同工况下制热量和制冷量的比值
            device_name (str): 水冷螺旋机机组名称,默认为"water_cooled_screw"
        """
        IntegratedEnergySystem(device_name)
        self.num_hour = num_hour
        WaterCooledScrew.index += 1
        self.electricity_price = electricity_price
        self.waterCooledScrewMachine_device: ContinuousVarType = model.continuous_var(
            name="waterCooledScrewMachine_device{0}".format(WaterCooledScrew.index)
        )
        """
        水冷螺旋机机组等效单位设备数 大于零的实数
        """
        self.annualized: ContinuousVarType = model.continuous_var(
            name="WaterCooledScrew_annualized{0}".format(WaterCooledScrew.index)
        )
        """
        连续变量,表示水冷螺旋机的年化费用
        """
        self.electricity_cost: ContinuousVarType = model.continuous_var(
            name="WaterCooledScrew_electricity_sum{0}".format(WaterCooledScrew.index)
        )
        """
        连续变量,表示水冷螺旋机的用电成本
        """
        self.device_price = device_price
        self.device_max = device_max
        self.case_ratio = case_ratio
        self.power_waterCooledScrewMachine_cool: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterCooledScrewMachine_cool{0}".format(WaterCooledScrew.index),
        )
        """
        连续变量列表,表示水冷螺旋机的制冷功率
        """
        self.waterCooledScrewMachine_cool_flag: List[
            BinaryVarType
        ] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterCooledScrewMachine_cool_flag{0}".format(WaterCooledScrew.index),
        )
        """
        二元变量列表,表示水冷螺旋机的制冷制冷状态
        """

        self.power_waterCooledScrewMachine_xcool: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterCooledScrewMachine_xcool{0}".format(
                WaterCooledScrew.index
            ),
        )
        """
        连续变量列表,表示水冷螺旋机的额外制冷功率
        """

        self.waterCooledScrewMachine_xcool_flag: List[
            BinaryVarType
        ] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterCooledScrewMachine_xcool_flag{0}".format(WaterCooledScrew.index),
        )
        """
        二元变量列表,表示水冷螺旋机的额外制冷制冷状态
        """

        self.electricity_waterCooledScrewMachine: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="electricity_waterCooledScrewMachine{0}".format(
                WaterCooledScrew.index
            ),
        )
        """
        连续变量列表,表示水冷螺旋机的用电量
        """
        self.power_waterCooledScrewMachine: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterCooledScrewMachine{0}".format(WaterCooledScrew.index),
        )
        """
        连续变量列表,表示水冷螺旋机的功率
        """
        self.coefficientOfPerformance_waterCooledScrewMachine_cool = 5
        self.coefficientOfPerformance_waterCooledScrewMachine_xcool = 5

    def constraints_register(self, model: Model):
        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦水冷螺旋机的制冷功率≦水冷螺旋机设备数* (况1)制热量/制冷量,0≦水冷螺旋机的制冷功率≦水冷螺旋机制冷状态*bigNumber
        3. 0≦水冷螺旋机的额外制冷功率≦水冷螺旋机设备数* (况2)制热量/制冷量,0≦水冷螺旋机的额外制冷功率≦水冷螺旋机额外制冷状态*bigNumber
        4. 制冷状态+额外制冷状态=1
        5. 水冷螺旋机用电量=设备制冷功率/制冷性能系数+设备额外制冷功率/额外制冷性能系数
        6. 热泵总功率=制冷功率+额外制冷功率
        7. 用电成本=每个时刻(设备用电量*电价)的总和
        8. 水冷螺旋机的总年化成本=水源热泵设备数*设备价格/15+用电成本*8760/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        hourRange = range(0, self.num_hour)
        model.add_constraint(0 <= self.waterCooledScrewMachine_device)
        model.add_constraint(self.waterCooledScrewMachine_device <= self.device_max)

        model.add_constraints(
            0 <= self.power_waterCooledScrewMachine_cool[h] for h in hourRange
        )
        model.add_constraints(
            self.power_waterCooledScrewMachine_cool[h]
            <= self.waterCooledScrewMachine_device * self.case_ratio[0]
            for h in hourRange
        )
        model.add_constraints(
            self.power_waterCooledScrewMachine_cool[h]
            <= bigNumber * self.waterCooledScrewMachine_cool_flag[h]
            for h in hourRange
        )

        model.add_constraints(
            0 <= self.power_waterCooledScrewMachine_xcool[h] for h in hourRange
        )
        model.add_constraints(
            self.power_waterCooledScrewMachine_xcool[h]
            <= self.waterCooledScrewMachine_device * self.case_ratio[1]
            for h in hourRange
        )
        model.add_constraints(
            self.power_waterCooledScrewMachine_xcool[h]
            <= bigNumber * self.waterCooledScrewMachine_xcool_flag[h]
            for h in hourRange
        )

        model.add_constraints(
            self.waterCooledScrewMachine_cool_flag[h]
            + self.waterCooledScrewMachine_xcool_flag[h]
            == 1
            for h in hourRange
        )
        model.add_constraints(
            self.electricity_waterCooledScrewMachine[h]
            == self.power_waterCooledScrewMachine_cool[h]
            / self.coefficientOfPerformance_waterCooledScrewMachine_cool
            + self.power_waterCooledScrewMachine_xcool[h]
            / self.coefficientOfPerformance_waterCooledScrewMachine_xcool
            for h in hourRange
        )
        model.add_constraints(
            self.power_waterCooledScrewMachine[h]
            == self.power_waterCooledScrewMachine_cool[h]
            + self.power_waterCooledScrewMachine_xcool[h]
            for h in hourRange
        )

        self.electricity_cost = model.sum(
            self.electricity_waterCooledScrewMachine[h] * self.electricity_price[h]
            for h in hourRange
        )
        # 年化
        model.add_constraint(
            self.annualized
            == self.waterCooledScrewMachine_device * self.device_price / 15
            + self.electricity_cost * 8760 / self.num_hour
        )


# 双工况机组
class DoubleWorkingConditionUnit(IntegratedEnergySystem):
    """
    双工况机组类
    """
    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_max,
        device_price,
        electricity_price,
        case_ratio,
        device_name="doubleWorkingConditionUnit",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_max (float): 表示双工况机组的最大数量。
            device_price (float): 表示双工况机组的单价。
            electricity_price (float): 电价
            case_ratio: 不同工况下制冰量和制冷量的比值
            device_name (str): 双工况机组名称,默认为"doubleWorkingConditionUnit"
        """
        IntegratedEnergySystem(device_name)
        self.num_hour = num_hour
        DoubleWorkingConditionUnit.index += 1
        self.electricity_price = electricity_price
        self.doubleWorkingConditionUnit_device: ContinuousVarType = (
            model.continuous_var(
                name="doubleWorkingConditionUnit_device{0}".format(
                    DoubleWorkingConditionUnit.index
                )
            )
        )
        """
        双工况机组等效单位设备数 大于零的实数
        """
        self.annualized: ContinuousVarType = model.continuous_var(
            name="DoubleWorkingConditionUnit_annualized{0}".format(
                DoubleWorkingConditionUnit.index
            )
        )
        """
        连续变量，表示双工况机组的年化费用
        """
        self.electricity_cost: ContinuousVarType = model.continuous_var(
            name="DoubleWorkingConditionUnit_electricity_sum{0}".format(
                DoubleWorkingConditionUnit.index
            )
        )
        """
        连续变量，表示双工况机组的用电成本
        """
        self.device_price = device_price
        self.device_max = device_max
        self.case_ratio = case_ratio
        self.power_doubleWorkingConditionUnit_cool: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_doubleWorkingConditionUnit_cool{0}".format(
                DoubleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示双工况机组的制冷功率
        """

        self.doubleWorkingConditionUnit_cool_flag: List[
            BinaryVarType
        ] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="doubleWorkingConditionUnit_cool_flag{0}".format(
                DoubleWorkingConditionUnit.index
            ),
        )
        """
        二元变量列表,表示双工况机组的制冷状态
        """

        self.power_doubleWorkingConditionUnit_ice: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_doubleWorkingConditionUnit_ice{0}".format(
                DoubleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示双工况机组的制冰功率
        """

        self.doubleWorkingConditionUnit_ice_flag: List[
            BinaryVarType
        ] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="doubleWorkingConditionUnit_ice_flag{0}".format(
                DoubleWorkingConditionUnit.index
            ),
        )
        """
        二元变量列表,表示双工况机组的制冰状态
        """

        self.electricity_doubleWorkingConditionUnit: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="electricity_doubleWorkingConditionUnit{0}".format(
                DoubleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示双工况机组的用电量
        """
        self.power_doubleWorkingConditionUnit: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_doubleWorkingConditionUnit{0}".format(
                DoubleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示双工况机组的功率
        """
        self.coefficientOfPerformance_doubleWorkingConditionUnit_cool = 5
        self.coefficientOfPerformance_doubleWorkingConditionUnit_ice = 5

    # 三工况机组

    def constraints_register(self, model: Model):
        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦双工况机组的制冷功率≦双工况机组设备数* (况1)制冰量/制冷量,0≦双工况机组的制冷功率≦双工况机组制冷状态*bigNumber
        3. 0≦双工况机组的制冰功率≦双工况机组设备数* (况2)制冰量/制冷量,0≦双工况机组的制冰功率≦双工况机组制冰状态*bigNumber
        4. 制冷状态+制冰状态=1
        5. 双工况机组用电量=设备制冷功率/制冷性能系数+设备制冰功率/制冰性能系数
        6. 热泵总功率=制冷功率+制冰功率
        7. 用电成本=每个时刻(设备用电量*电价)的总和
        8. 双工况机组的总年化成本=双工况机组设备数*设备价格/15+用电成本*8760/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        hourRange = range(0, self.num_hour)
        model.add_constraint(0 <= self.doubleWorkingConditionUnit_device)
        model.add_constraint(self.doubleWorkingConditionUnit_device <= self.device_max)

        model.add_constraints(
            0 <= self.power_doubleWorkingConditionUnit_cool[h] for h in hourRange
        )
        model.add_constraints(
            self.power_doubleWorkingConditionUnit_cool[h]
            <= self.doubleWorkingConditionUnit_device * self.case_ratio[0]
            for h in hourRange
        )
        model.add_constraints(
            self.power_doubleWorkingConditionUnit_cool[h]
            <= bigNumber * self.doubleWorkingConditionUnit_cool_flag[h]
            for h in hourRange
        )

        model.add_constraints(
            0 <= self.power_doubleWorkingConditionUnit_ice[h] for h in hourRange
        )
        model.add_constraints(
            self.power_doubleWorkingConditionUnit_ice[h]
            <= self.doubleWorkingConditionUnit_device * self.case_ratio[1]
            for h in hourRange
        )
        model.add_constraints(
            self.power_doubleWorkingConditionUnit_ice[h]
            <= bigNumber * self.doubleWorkingConditionUnit_ice_flag[h]
            for h in hourRange
        )

        model.add_constraints(
            self.doubleWorkingConditionUnit_cool_flag[h]
            + self.doubleWorkingConditionUnit_ice_flag[h]
            == 1
            for h in hourRange
        )
        model.add_constraints(
            self.electricity_doubleWorkingConditionUnit[h]
            == self.power_doubleWorkingConditionUnit_cool[h]
            / self.coefficientOfPerformance_doubleWorkingConditionUnit_cool
            + self.power_doubleWorkingConditionUnit_ice[h]
            / self.coefficientOfPerformance_doubleWorkingConditionUnit_ice
            for h in hourRange
        )
        model.add_constraints(
            self.power_doubleWorkingConditionUnit[h]
            == self.power_doubleWorkingConditionUnit_cool[h]
            + self.power_doubleWorkingConditionUnit_ice[h]
            for h in hourRange
        )

        self.electricity_cost = model.sum(
            self.electricity_doubleWorkingConditionUnit[h] * self.electricity_price[h]
            for h in hourRange
        )
        # 年化
        model.add_constraint(
            self.annualized
            == self.doubleWorkingConditionUnit_device * self.device_price / 15
            + self.electricity_cost * 8760 / self.num_hour
        )


class TripleWorkingConditionUnit(IntegratedEnergySystem):
    """
    三工况机组类
    """
    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_max,
        device_price,
        electricity_price,
        case_ratio,
        device_name="tripleWorkingConditionUnit",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_max (float): 表示三工况机组的最大数量
            device_price (float): 表示三工况机组的单价
            electricity_price (float): 电价
            case_ratio: 不同工况下制热量和制冷量的比值
            device_name (str): 三工况机组名称,默认为"tripleWorkingConditionUnit"
        """
        IntegratedEnergySystem(device_name)
        self.num_hour = num_hour

        TripleWorkingConditionUnit.index += 1
        self.electricity_price = electricity_price
        self.tripleWorkingConditionUnit_device: ContinuousVarType = (
            model.continuous_var(
                name="tripleWorkingConditionUnit_device{0}".format(
                    TripleWorkingConditionUnit.index
                )
            )
        )
        """
        三工况机组等效单位设备数 大于零的实数
        """
        self.annualized: ContinuousVarType = model.continuous_var(
            name="TripleWorkingConditionUnit_annualized{0}".format(
                TripleWorkingConditionUnit.index
            )
        )
        """
        连续变量,表示三工况机组的年化费用
        """
        self.electricity_cost: ContinuousVarType = model.continuous_var(
            name="TripleWorkingConditionUnit_electricity_sum{0}".format(
                TripleWorkingConditionUnit.index
            )
        )
        """
        连续变量,表示三工况机组的用电成本
        """
        self.device_price = device_price
        self.device_max = device_max
        self.case_ratio = case_ratio
        self.power_tripleWorkingConditionUnit_cool: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_tripleWorkingConditionUnit_cool{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示三工况机组的制冷功率
        """

        self.tripleWorkingConditionUnit_cool_flag: List[
            BinaryVarType
        ] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="tripleWorkingConditionUnit_cool_flag{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        二元变量列表,表示三工况机组的制冷状态
        """

        self.power_tripleWorkingConditionUnit_ice: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_tripleWorkingConditionUnit_ice{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示三工况机组的制冰功率
        """

        self.tripleWorkingConditionUnit_ice_flag: List[
            BinaryVarType
        ] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="tripleWorkingConditionUnit_ice_flag{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        二元变量列表,表示三工况机组的制冰状态
        """

        self.power_tripleWorkingConditionUnit_heat: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_tripleWorkingConditionUnit_heat{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示三工况机组的制热功率
        """

        self.tripleWorkingConditionUnit_heat_flag: List[
            BinaryVarType
        ] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="tripleWorkingConditionUnit_heat_flag{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        二元变量列表,表示三工况机组的制热状态
        """

        self.electricity_tripleWorkingConditionUnit: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="electricity_tripleWorkingConditionUnit{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示三工况机组的用电量
        """
        self.power_tripleWorkingConditionUnit: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_tripleWorkingConditionUnit{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示三工况机组的功率
        """
        self.coefficientOfPerformance_tripleWorkingConditionUnit_cool = 5
        self.coefficientOfPerformance_tripleWorkingConditionUnit_ice = 4
        self.coefficientOfPerformance_tripleWorkingConditionUnit_heat = 5

    def constraints_register(self, model: Model):
        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦三工况机组的制冷功率≦三工况机组设备数* (况1)制热量/制冷量,0≦三工况机组的制冷功率≦三工况机组制冷状态*bigNumber
        3. 0≦三工况机组的制冰功率≦三工况机组设备数* (况2)制热量/制冷量,0≦三工况机组的制冰功率≦三工况机组制冰状态*bigNumber
        4. 制冷状态+制冰状态=1
        5. 双工况机组用电量=设备制冷功率/制冷性能系数+设备制冰功率/制冰性能系数
        6. 热泵总功率=制冷功率+制冰功率
        7. 用电成本=每个时刻(设备用电量*电价)的总和
        8. 双工况机组的总年化成本=双工况机组设备数*设备价格/15+用电成本*8760/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        hourRange = range(0, self.num_hour)
        model.add_constraint(0 <= self.tripleWorkingConditionUnit_device)
        model.add_constraint(self.tripleWorkingConditionUnit_device <= self.device_max)

        model.add_constraints(
            0 <= self.power_tripleWorkingConditionUnit_cool[h] for h in hourRange
        )
        model.add_constraints(
            self.power_tripleWorkingConditionUnit_cool[h]
            <= self.tripleWorkingConditionUnit_device * self.case_ratio[0]
            for h in hourRange
        )
        model.add_constraints(
            self.power_tripleWorkingConditionUnit_cool[h]
            <= bigNumber * self.tripleWorkingConditionUnit_cool_flag[h]
            for h in hourRange
        )

        model.add_constraints(
            0 <= self.power_tripleWorkingConditionUnit_ice[h] for h in hourRange
        )
        model.add_constraints(
            self.power_tripleWorkingConditionUnit_ice[h]
            <= self.tripleWorkingConditionUnit_device * self.case_ratio[1]
            for h in hourRange
        )
        model.add_constraints(
            self.power_tripleWorkingConditionUnit_ice[h]
            <= bigNumber * self.tripleWorkingConditionUnit_ice_flag[h]
            for h in hourRange
        )

        model.add_constraints(
            0 <= self.power_tripleWorkingConditionUnit_heat[h] for h in hourRange
        )
        model.add_constraints(
            self.power_tripleWorkingConditionUnit_heat[h]
            <= self.tripleWorkingConditionUnit_device * self.case_ratio[2]
            for h in hourRange
        )
        model.add_constraints(
            self.power_tripleWorkingConditionUnit_heat[h]
            <= bigNumber * self.tripleWorkingConditionUnit_heat_flag[h]
            for h in hourRange
        )

        model.add_constraints(
            self.tripleWorkingConditionUnit_cool_flag[h]
            + self.tripleWorkingConditionUnit_ice_flag[h]
            + self.tripleWorkingConditionUnit_heat_flag[h]
            == 1
            for h in hourRange
        )
        model.add_constraints(
            self.electricity_tripleWorkingConditionUnit[h]
            == self.power_tripleWorkingConditionUnit_cool[h]
            / self.coefficientOfPerformance_tripleWorkingConditionUnit_cool
            + self.power_tripleWorkingConditionUnit_ice[h]
            / self.coefficientOfPerformance_tripleWorkingConditionUnit_ice
            + self.power_tripleWorkingConditionUnit_heat[h]
            / self.coefficientOfPerformance_tripleWorkingConditionUnit_heat
            for h in hourRange
        )
        model.add_constraints(
            self.power_tripleWorkingConditionUnit[h]
            == self.power_tripleWorkingConditionUnit_cool[h]
            + self.power_tripleWorkingConditionUnit_ice[h]
            + self.power_tripleWorkingConditionUnit_heat[h]
            for h in hourRange
        )

        self.electricity_cost = model.sum(
            self.electricity_tripleWorkingConditionUnit[h] * self.electricity_price[h]
            for h in hourRange
        )
        # 年化
        model.add_constraint(
            self.annualized
            == self.tripleWorkingConditionUnit_device * self.device_price / 15
            + self.electricity_cost * 8760 / self.num_hour
        )


class GeothermalHeatPump(IntegratedEnergySystem):
    """地源热泵类"""

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_max:float,
        device_price:float,
        electricity_price:np.ndarray,
        device_name:str="geothermal_heat_pump",
    ):
        """新建一个地源热泵类
        
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_max (float): 地源热泵机组最大装机量
            device_price (float): 设备单价
            electricity_price (np.ndarray): 24小时用电价格
            device_name (str): 地源热泵机组名称,默认为"geothermal_heat_pump"
        """
        IntegratedEnergySystem(device_name)
        self.num_hour = num_hour
        GeothermalHeatPump.index += 1
        self.electricity_price = electricity_price
        self.groundSourceHeatPump_device: ContinuousVarType = model.continuous_var(
            name="groundSourceHeatPump_device{0}".format(GeothermalHeatPump.index)
        )
        """
        地源热泵机组设备数量
        """
        self.annualized: ContinuousVarType = model.continuous_var(
            name="GeothermalHeatPumpower_annualized{0}".format(GeothermalHeatPump.index)
        )
        """
        地源热泵机组年运维成本
        """
        self.electricity_cost: ContinuousVarType = model.continuous_var(
            name="GeothermalHeatPumpower_electricity_sum{0}".format(
                GeothermalHeatPump.index
            )
        )
        """
        地源热泵每小时耗电费用
        """
        self.device_price = device_price
        self.device_max = device_max

        self.electricity_groundSourceHeatPump: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="electricity_groundSourceHeatPump{0}".format(GeothermalHeatPump.index),
        )
        """
        地源热泵每小时耗电量
        """
        self.power_groundSourceHeatPump: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_groundSourceHeatPump{0}".format(GeothermalHeatPump.index),
        )
        """
        地源热泵每小时输出功率
        """
        self.coefficientOfPerformance_groundSourceHeatPump = 5
        """
        地源热泵设备运行效率参数 默认为5
        """

    def constraints_register(self, model: Model):
        """
        定义地源热泵机组约束条件:
        
        1. 0 <= 机组设备数量 <= 最大装机量
        2. 0 <= 每小时输出功率 <= 机组设备数量
        3. 每小时耗电量 = 每小时输出功率 / 运行效率参数
        4. 机组一天用电费用 = sum(每小时耗电量 * 该小时用电价格)
        5. 机组年运维成本 = 机组设备数量 * 设备价格 / 15 + 机组一天用电费用 * 8760 / 一天小时数
        
        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        hourRange = range(0, self.num_hour)

        model.add_constraint(0 <= self.groundSourceHeatPump_device)
        model.add_constraint(self.groundSourceHeatPump_device <= self.device_max)

        model.add_constraints(
            0 <= self.power_groundSourceHeatPump[h] for h in hourRange
        )
        model.add_constraints(
            self.power_groundSourceHeatPump[h] <= self.groundSourceHeatPump_device
            for h in hourRange
        )

        model.add_constraints(
            self.electricity_groundSourceHeatPump[h]
            == self.power_groundSourceHeatPump[h]
            / self.coefficientOfPerformance_groundSourceHeatPump
            for h in hourRange
        )
        self.electricity_cost = model.sum(
            self.electricity_groundSourceHeatPump[h] * self.electricity_price[h]
            for h in hourRange
        )
        # 年化
        model.add_constraint(
            self.annualized
            == self.groundSourceHeatPump_device * self.device_price / 15
            + self.electricity_cost * 8760 / self.num_hour
        )


# 水蓄能,可蓄highTemperature,可以蓄低温
# waterStorageTank,可变容量的储能体
class WaterEnergyStorage(IntegratedEnergySystem):
    """
    水蓄能类
    """
    # index=0
    def __init__(
        self,
        num_hour: int,
        model: Model,
        waterStorageTank_Volume_max: float,  # V?
        volume_price: float,
        powerConversionSystem_price: float,
        conversion_rate_max: float,
        efficiency: float,
        energyStorageSystem_init:float,
        stateOfCharge_min: float,
        stateOfCharge_max: float,
        ratio_cool: float,
        ratio_heat: float,
        ratio_gheat: float,  # gheat? 工作热量？ geothermal heat?
        device_name: str = "water_energy_storage",
    ):
        """
        创建一个水蓄能类
        
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            waterStorageTank_Volume_max (float): 单个水罐的最大体积
            volume_price (float): 单位体积储水费用
            powerConversionSystem_price (float): 能源转换系统设备价格
            conversion_rate_max (float): 最大输入输出速率
            efficiency (float): 水罐储水效率参数
            energyStorageSystem_init (float): 储能装置的初始能量
            stateOfCharge_min (float): 最小储能量
            stateOfCharge_max (float): 最大储能量
            ratio_cool (float): 机组储藏冷量比例
            ratio_heat (float): 机组储藏热量比例
            ratio_gheat (float): 机组储藏温水比例
            device_name (str): 水蓄能机组名称,默认为"water_energy_storage",
        """
        IntegratedEnergySystem(device_name)
        self.num_hour = num_hour
        self.model = model
        # 对于水蓄能,优化的变量为水罐的体积
        self.waterStorageTank = EnergyStorageSystemVariable(
            num_hour,
            model,
            bigNumber,
            0,
            powerConversionSystem_price,
            conversion_rate_max,
            efficiency,
            energyStorageSystem_init,
            stateOfCharge_min,
            stateOfCharge_max,
        )
        """
        水蓄能罐，由可变储能设备`EnergyStorageSystemVariable`创建而来
        """
        self.index = EnergyStorageSystemVariable.index
        self.waterStorageTank_device_cool: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterStorageTank_device_cool{0}".format(self.index),
        )
        """
        每小时水蓄能机组储藏冷水量
        """
        self.waterStorageTank_device_heat: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterStorageTank_device_heat{0}".format(self.index),
        )
        """
        每小时水蓄能机组储藏热水量
        """
        self.waterStorageTank_device_gheat: List[ # generate?
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterStorageTank_device_gheat{0}".format(self.index),
        )
        """
        每小时水蓄能机组储藏温水量
        """
        self.volume_price = volume_price
        self.waterStorageTank_Volume_max = waterStorageTank_Volume_max
        self.waterStorageTank_Volume: ContinuousVarType = model.continuous_var(
            name="waterStorageTank_V{0}".format(self.index)
        )
        """
        水蓄能机组总体积
        """
        self.waterStorageTank_cool_flag: List[BinaryVarType] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterStorageTank_cool_flag{0}".format(self.index),
        )
        """
        每小时水蓄能设备储冷状态
        """
        self.waterStorageTank_heat_flag: List[BinaryVarType] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterStorageTank_heat_flag{0}".format(self.index),
        )
        """
        每小时水蓄能设备储热状态
        """
        self.waterStorageTank_gheat_flag: List[BinaryVarType] = model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterStorageTank_gheat_flag{0}".format(self.index),
        )
        """
        每小时水蓄能设备储温状态
        """
        self.ratio_cool = ratio_cool
        self.ratio_heat = ratio_heat
        self.ratio_gheat = ratio_gheat
        self.power_waterStorageTank_cool: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterStorageTank_cool{0}".format(self.index),
        )
        """
        每小时水蓄能设备储冷功率
        """
        self.power_waterStorageTank_heat: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterStorageTank_heat{0}".format(self.index),
        )
        """
        每小时水蓄能设备储热功率
        """
        self.power_waterStorageTank_gheat: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterStorageTank_gheat{0}".format(self.index),  # gheat?
        )
        """
        每小时水蓄能设备储温功率
        """
        self.annualized: ContinuousVarType = model.continuous_var(
            name="power_waterStorageTank_annualized{0}".format(self.index)
        )
        """
        水蓄能设备年运维费用
        """

    def constraints_register(self, model: Model, register_period_constraints, day_node):
        """
        定义水蓄能类的约束条件：
        
        1. 
        2. 
        3. 
        
        Args:
            model (docplex.mp.model.Model): 求解模型实例
            register_period_constraints ():
            day_node ():
        """
        bigNumber = 1e10
        hourRange = range(0, self.num_hour)
        self.waterStorageTank.constraints_register(
            model, register_period_constraints, day_node
        )
        # waterStorageTank_device[h] == waterStorageTank_cool_flag[h] * waterStorageTank_Volume * ratio_cool + waterStorageTank_heat_flag[h] * waterStorageTank_Volume * ratio_heat + waterStorageTank_gheat_flag[
        #   h] * waterStorageTank_Volume * ratio_gheat
        # 用下面的式子进行线性化
        model.add_constraint(
            self.waterStorageTank_Volume <= self.waterStorageTank_Volume_max
        )
        model.add_constraint(self.waterStorageTank_Volume >= 0)
        model.add_constraints(
            self.waterStorageTank.energyStorageSystem_device[h]
            == self.waterStorageTank_device_cool[h]
            + self.waterStorageTank_device_heat[h]
            + self.waterStorageTank_device_gheat[h]
            for h in hourRange
        )
        # (1)
        model.add_constraints(
            self.waterStorageTank_device_cool[h]
            <= self.waterStorageTank_Volume * self.ratio_cool
            for h in hourRange
        )
        model.add_constraints(
            self.waterStorageTank_device_cool[h]
            <= self.waterStorageTank_cool_flag[h] * bigNumber
            for h in hourRange
        )
        model.add_constraints(
            self.waterStorageTank_device_cool[h] >= 0 for h in hourRange
        )
        model.add_constraints(
            self.waterStorageTank_device_cool[h]
            >= self.waterStorageTank_Volume * self.ratio_cool
            - (1 - self.waterStorageTank_cool_flag[h]) * bigNumber
            for h in hourRange
        )
        # (2)
        model.add_constraints(
            self.waterStorageTank_device_heat[h]
            <= self.waterStorageTank_Volume * self.ratio_heat
            for h in hourRange
        )
        model.add_constraints(
            self.waterStorageTank_device_heat[h]
            <= self.waterStorageTank_heat_flag[h] * bigNumber
            for h in hourRange
        )
        model.add_constraints(
            self.waterStorageTank_device_heat[h] >= 0 for h in hourRange
        )
        model.add_constraints(
            self.waterStorageTank_device_heat[h]
            >= self.waterStorageTank_Volume * self.ratio_heat
            - (1 - self.waterStorageTank_heat_flag[h]) * bigNumber
            for h in hourRange
        )
        # (3)
        model.add_constraints(
            self.waterStorageTank_device_gheat[h]
            <= self.waterStorageTank_Volume * self.ratio_gheat
            for h in hourRange
        )
        model.add_constraints(
            self.waterStorageTank_device_gheat[h]
            <= self.waterStorageTank_gheat_flag[h] * bigNumber
            for h in hourRange
        )
        model.add_constraints(
            self.waterStorageTank_device_gheat[h] >= 0 for h in hourRange
        )
        model.add_constraints(
            self.waterStorageTank_device_gheat[h]
            >= self.waterStorageTank_Volume * self.ratio_gheat
            - (1 - self.waterStorageTank_gheat_flag[h]) * bigNumber
            for h in hourRange
        )
        # % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
        model.add_constraints(
            self.waterStorageTank_cool_flag[h]
            + self.waterStorageTank_heat_flag[h]
            + self.waterStorageTank_gheat_flag[h]
            == 1
            for h in hourRange
        )  # % 三个方面进行核算。
        # （1） power_waterStorageTank_cool[h] == power_waterStorageTank[h] * waterStorageTank_cool_flag[h]
        # （2）power_waterStorageTank_heat[h] == power_waterStorageTank[h] * waterStorageTank_heat_flag[h]
        # （3）power_waterStorageTank_gheat[h] == power_waterStorageTank[h] * waterStorageTank_gheat_flag[h]
        # 上面的公式进行线性化后,用下面的公式替代
        # (1)

        model.add_constraints(
            -bigNumber * self.waterStorageTank_cool_flag[h]
            <= self.power_waterStorageTank_cool[h]
            for h in hourRange
        )
        model.add_constraints(
            self.power_waterStorageTank_cool[h]
            <= bigNumber * self.waterStorageTank_cool_flag[h]
            for h in hourRange
        )
        model.add_constraints(
            self.waterStorageTank.power_energyStorageSystem[h]
            - (1 - self.waterStorageTank_cool_flag[h]) * bigNumber
            <= self.power_waterStorageTank_cool[h]
            for h in hourRange
        )
        model.add_constraints(
            self.power_waterStorageTank_cool[h]
            <= self.waterStorageTank.power_energyStorageSystem[h]
            + (1 - self.waterStorageTank_cool_flag[h]) * bigNumber
            for h in hourRange
        )
        # (2)
        model.add_constraints(
            -bigNumber * self.waterStorageTank_heat_flag[h]
            <= self.power_waterStorageTank_heat[h]
            for h in hourRange
        )
        model.add_constraints(
            self.power_waterStorageTank_heat[h]
            <= bigNumber * self.waterStorageTank_heat_flag[h]
            for h in hourRange
        )
        model.add_constraints(
            self.waterStorageTank.power_energyStorageSystem[h]
            - (1 - self.waterStorageTank_heat_flag[h]) * bigNumber
            <= self.power_waterStorageTank_heat[h]
            for h in hourRange
        )
        model.add_constraints(
            self.power_waterStorageTank_heat[h]
            <= self.waterStorageTank.power_energyStorageSystem[h]
            + (1 - self.waterStorageTank_heat_flag[h]) * bigNumber
            for h in hourRange
        )
        # (3)
        model.add_constraints(
            -bigNumber * self.waterStorageTank_gheat_flag[h]
            <= self.power_waterStorageTank_gheat[h]
            for h in hourRange
        )
        model.add_constraints(
            self.power_waterStorageTank_gheat[h]
            <= bigNumber * self.waterStorageTank_gheat_flag[h]
            for h in hourRange
        )
        model.add_constraints(
            self.waterStorageTank.power_energyStorageSystem[h]
            - (1 - self.waterStorageTank_gheat_flag[h]) * bigNumber
            <= self.power_waterStorageTank_gheat[h]
            for h in hourRange
        )
        model.add_constraints(
            self.power_waterStorageTank_gheat[h]
            <= self.waterStorageTank.power_energyStorageSystem[h]
            + (1 - self.waterStorageTank_gheat_flag[h]) * bigNumber
            for h in hourRange
        )
        model.add_constraint(
            self.annualized == self.waterStorageTank_Volume * self.volume_price / 20
        )


# groundSourceSteamGenerator
class GroundSourceSteamGenerator(IntegratedEnergySystem):
    """
    """
    
    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        groundSourceSteamGenerator_device_max,
        groundSourceSteamGenerator_price,
        groundSourceSteamGeneratorSolidHeatStorage_price,
        electricity_price,
        efficiency: float,
        device_name="groundSourceSteamGenerator",
    ):
        """
        """
        IntegratedEnergySystem(device_name)
        GroundSourceSteamGenerator.index += 1
        self.num_hour = num_hour
        self.groundSourceSteamGenerator_device: ContinuousVarType = (
            model.continuous_var(
                name="groundSourceSteamGenerator_device{0}".format(
                    GroundSourceSteamGenerator.index
                )
            )
        )
        
        """
        """
        self.power_groundSourceSteamGenerator: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_groundSourceSteamGenerator{0}".format(
                GroundSourceSteamGenerator.index
            ),
        )

        """
        """
        self.power_groundSourceSteamGenerator_steam: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_groundSourceSteamGenerator_steam{0}".format(
                TroughPhotoThermal.index
            ),
        )

        """
        """
        self.groundSourceSteamGenerator_device_max = (
            groundSourceSteamGenerator_device_max
        )
        self.groundSourceSteamGeneratorSolidHeatStorage_device_max = (
            groundSourceSteamGenerator_device_max * 6
        )
        
        """
        """
        self.groundSourceSteamGenerator_price = groundSourceSteamGenerator_price
        self.groundSourceSteamGeneratorSolidHeatStorage_price = (
            groundSourceSteamGeneratorSolidHeatStorage_price
        )
        self.electricity_price = electricity_price

        self.annualized: ContinuousVarType = model.continuous_var(
            name="GroundSourceSteamGenerator_annualized{0}".format(
                GroundSourceSteamGenerator.index
            )
        )
        
        """
        """
        self.efficiency = efficiency

        self.groundSourceSteamGeneratorSolidHeatStorage_device = EnergyStorageSystem(
            num_hour,
            model,
            self.groundSourceSteamGeneratorSolidHeatStorage_device_max,
            self.groundSourceSteamGeneratorSolidHeatStorage_price,
            powerConversionSystem_price=0,
            conversion_rate_max=2,
            efficiency=0.9,
            energyStorageSystem_init=1,
            stateOfCharge_min=0,
            stateOfCharge_max=1,
        )
        
        """
        """
        self.electricity_cost: ContinuousVarType = model.continuous_var(
            name="groundSourceSteamGenerator_electricity_cost{0}".format(
                GroundSourceSteamGenerator.index
            )
        )
        
        """
        """

    def constraints_register(self, model: Model):
        
        """
        """
        hourRange = range(0, self.num_hour)
        self.groundSourceSteamGeneratorSolidHeatStorage_device.constraints_register(
            model
        )
        model.add_constraint(self.groundSourceSteamGenerator_device >= 0)
        model.add_constraint(
            self.groundSourceSteamGenerator_device
            <= self.groundSourceSteamGenerator_device_max
        )
        model.add_constraints(
            self.power_groundSourceSteamGenerator[h] >= 0 for h in hourRange
        )
        model.add_constraints(
            self.power_groundSourceSteamGenerator[h]
            <= self.groundSourceSteamGenerator_device
            for h in hourRange
        )  # 与天气相关
        model.add_constraints(
            self.power_groundSourceSteamGenerator[h]
            + self.groundSourceSteamGeneratorSolidHeatStorage_device.power_energyStorageSystem[
                h
            ]
            == self.power_groundSourceSteamGenerator_steam[h]
            for h in hourRange
        )  # troughPhotoThermal系统产生的highTemperature
        model.add_constraints(
            0 <= self.power_groundSourceSteamGenerator_steam[h] for h in hourRange
        )  # 约束能量不能倒流
        model.add_constraints(
            self.electricity_cost
            == self.power_groundSourceSteamGenerator[h] * self.electricity_price[h]
            for h in hourRange
        )
        model.add_constraint(
            self.annualized
            == self.groundSourceSteamGenerator_device
            * self.groundSourceSteamGenerator_price
            / 15
            + self.groundSourceSteamGeneratorSolidHeatStorage_device.annualized
            + self.electricity_cost
        )


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


class Linear_absolute(object):  # absolute?
    """
    带绝对值的线性约束类
    """

    bigNumber0 = 1e10
    index = 0

    def __init__(self, model: Model, x: List[Var], irange: Iterable):  # irange?
        """
        初始化带绝对值的线性约束类

        Args:
            model (docplex.mp.model.Model): 求解模型实例
            x (List[Var]): 存放`xpositive`和`xnegitive`在区间`irange`内逐元素相减结果约束得到的变量组`x`
            irange (Iterable): 整数区间
        """
        Linearization.index += 1  # 要增加变量
        self.b_positive: List[BinaryVarType] = model.binary_var_list(
            [i for i in irange],
            name="b_positive_absolute{0}".format(Linear_absolute.index),
        )
        """
        一个二进制变量列表,长度为`len(irange)`
        
        对于`b_positive`和`b_negitive`,有:
        `b_positive[i] == 1`时,`b_negitive[i] == 0`
        `b_positive[i] == 0`时,`b_negitive[i] == 1`
        
        对于`b_positive`和`x_positive`,有:
        `b_positive[i]` == 1`时,`x_positive[i] >= 0`
        `b_positive[i]` == 0`时,`x_positive[i] == 0`
        """
        self.b_negitive: List[BinaryVarType] = model.binary_var_list(
            [i for i in irange],
            name="b_negitive_absolute{0}".format(Linear_absolute.index),
        )
        """
        一个二进制变量列表,长度为`len(irange)`
        
        对于`b_negitive`和`x_negitive`,有:
        `b_negitive[i]` == 1`时,`x_negitive[i] >= 0`
        `b_negitive[i]` == 0`时,`x_negitive[i] == 0`
        """
        self.x_positive: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in irange],
            name="x_positive_absolute{0}".format(Linear_absolute.index),
        )
        """
        一个实数变量列表,长度为`len(irange)`
        
        对于区间`irange`的每个数`i`,`x_positive[i]`是非负数,`x_positive[i]`和`x_negitive[i]`中必须有一个为0,另外一个大于0
        """
        self.x_negitive: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in irange],
            name="x_negitive_absolute{0}".format(Linear_absolute.index),
        )
        """
        一个实数变量列表,长度为`len(irange)`
        
        对于区间`irange`的每个数`i`,`x_negitive[i]`是非负数,`x_positive[i]`和`x_negitive[i]`中必须有一个为0,另外一个大于0
        """
        self.absolute_x: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in irange], name="absolute_x{0}".format(Linear_absolute.index)
        )
        """
        一个实数变量列表,长度为`len(irange)`
        
        对于`b_positive`、`absolute_x`、`x_positive`、`x_negitive`有:
        `b_positive[i] == 1`时,`absolute_x[i] == x_positive[i]`
        `b_positive[i] == 0`时,`absolute_x[i] == x_negitive[i]`
        """
        self.irange = irange
        self.x = x

    def absolute_add_constraints(self, model: Model):
        """
        对于区间`irange`的每个数`i`,`x_positive[i]`、`x_negitive[i]`是非负实数,`b_positive[i]`、`b_negitive[i]`是不同情况对应的二进制变量,约定以下两种情况有且只有一种出现:

        1. `bigNumber0 >= x_negitive[i] >= 0`,`x_positive[i] == 0`,此时`b_positive[i] == 0`,`b_negitive[i] == 1`,`x[i] == -x_negitive[i]`,`absolute_x[i] == x_negitive[i]`
        2. `bigNumber0 >= x_positive[i] >= 0`,`x_negative[i] == 0`,此时`b_positive[i] == 1`,`b_negitive[i] == 0`,`x[i] == x_positive[i]`,`absolute_x[i] == x_positive[i]`

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        model.add_constraints(
            self.b_positive[i] + self.b_negitive[i] == 1 for i in self.irange
        )
        # b_positive[i]==1时,b_negitive[i]==0
        # b_positive[i]==0时,b_negitive[i]==1
        model.add_constraints(
            self.x_positive[i] >= 0 for i in self.irange
        )  # x_positive[i]是非负数
        model.add_constraints(
            self.x_positive[i] <= self.bigNumber0 * self.b_positive[i]
            for i in self.irange
        )
        # 当b_positive[i]==1时,x_positive[i]>=0
        # 当b_positive[i]==0时,x_positive[i]==0

        model.add_constraints(self.x_negitive[i] >= 0 for i in self.irange)
        # x_negitive[i]是非负数
        model.add_constraints(
            self.x_negitive[i] <= self.bigNumber0 * self.b_negitive[i]
            for i in self.irange
        )

        # 当b_negitive[i]==1时,x_negitive[i]>=0
        # 当b_negitive[i]==0时,x_negitive[i]==0
        model.add_constraints(
            self.x[i] == self.x_positive[i] - self.x_negitive[i] for i in self.irange
        )
        # x[i] == x_positive[i] - x_negitive[i]
        # 也就是说,如果b_positive[i]==1,x[i] == x_positive[i]
        # 如果b_positive[i]==0,x[i] == -x_negitive[i]
        model.add_constraints(
            self.absolute_x[i] == self.x_positive[i] + self.x_negitive[i]
            for i in self.irange
        )

        # absolute_x[i] == x_positive[i] + x_negitive[i]
        # 也就是说,如果b_positive[i]==1,absolute_x[i] == x_positive[i]
        # 如果b_positive[i]==0,absolute_x[i] == x_negitive[i]


# 适用于municipalSteam,municipalHotWater
class CitySupply(IntegratedEnergySystem):
    """市政能源类,适用于市政蒸汽、市政热水"""

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        citySupplied_device_max,
        device_price,
        run_price,
        efficiency: float,
        device_name="city_supply",
    ):
        IntegratedEnergySystem(device_name)
        CitySupply.index += 1
        self.num_hour = num_hour  # hours in a day
        self.citySupplied_device: ContinuousVarType = model.continuous_var(
            name="citySupplied_device{0}".format(CitySupply.index)
        )

        self.heat_citySupplied: List[ContinuousVarType] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="heat_citySupplied{0}".format(CitySupply.index),
        )
        self.heat_citySupplied_from: List[
            ContinuousVarType
        ] = model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="heat_citySupplied_from{0}".format(CitySupply.index),
        )
        self.citySupplied_device_max = citySupplied_device_max
        self.run_price = run_price
        self.device_price = device_price

        self.efficiency = efficiency
        self.citySupplied_cost: ContinuousVarType = model.continuous_var(
            name="citySupplied_cost{0}".format(CitySupply.index)
        )
        self.annualized: ContinuousVarType = model.continuous_var(
            name="citySupplied_annualized{0}".format(CitySupply.index)
        )

    def constraints_register(self, model: Model):
        hourRange = range(0, self.num_hour)
        model.add_constraint(self.citySupplied_device >= 0)
        model.add_constraint(self.citySupplied_device <= self.citySupplied_device_max)
        model.add_constraints(self.heat_citySupplied[h] >= 0 for h in hourRange)
        model.add_constraints(
            self.heat_citySupplied[h] <= self.citySupplied_device for h in hourRange
        )
        model.add_constraints(
            self.heat_citySupplied[h]
            == self.heat_citySupplied_from[h] / self.efficiency
            for h in hourRange
        )
        self.citySupplied_cost = model.sum(
            self.heat_citySupplied_from[h] * self.run_price[h] for h in hourRange
        )
        model.add_constraint(
            self.annualized
            == self.citySupplied_device * self.device_price / 15
            + self.citySupplied_cost * 8760 / self.num_hour
        )


# 电网？
class GridNet(IntegratedEnergySystem):
    """
    电网类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        gridNet_device_max: float,
        device_price: float,
        electricity_price_from: np.ndarray,
        electricity_price_to: float,
        device_name: str = "grid_net",
    ):
        """
        新建一个电网类

        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            gridnet_device_max (float): 电网最大设备量
            device_price (float): 设备单价
            electricity_price_from (np.ndarray): 电力使用价格
            electricity_price_to (float): 电力生产报酬
            device_name (str): 电网名称,默认为"grid_net"
        """
        IntegratedEnergySystem(device_name)
        GridNet.index += 1
        self.num_hour = num_hour
        self.model = model
        self.gridNet_device: ContinuousVarType = model.continuous_var(
            name="gridNet_device{0}".format(GridNet.index)
        )
        """
        电网装机设备数 非负实数
        """

        self.gridNet_device_max = gridNet_device_max
        self.electricity_price_from = electricity_price_from
        self.electricity_price_to = electricity_price_to

        self.device_price = device_price

        self.gridNet_cost: ContinuousVarType = model.continuous_var(
            name="gridNet_cost{0}".format(GridNet.index)
        )
        """
        电网用电费用 非负实数
        """

        self.annualized: ContinuousVarType = model.continuous_var(
            name="gridNet_annualized{0}".format(GridNet.index)
        )
        """
        电网每年运维费用 非负实数
        """

        self.total_power = model1.continuous_var_list(
            [i for i in range(0, num_hour0)],
            lb=-bigNumber,  # lower bound
            name="total_power {0}".format(GridNet.index),
        )
        """
        电网逐小时净用电量 长度为`num_hour0`的实数列表 大于零时电网耗电 小于零时电网发电
        """

        self.powerFrom = model1.continuous_var_list(
            [i for i in range(0, num_hour0)], name="powerFrom{0}".format(GridNet.index)
        )
        """
        电网逐小时用电量 长度为`num_hour0`的非负实数列表
        """
        self.powerTo = model1.continuous_var_list(
            [i for i in range(0, num_hour0)], name="powerTo {0}".format(GridNet.index)
        )
        """
        电网逐小时发电量 长度为`num_hour0`的非负实数列表
        """
        self.powerPeak = model1.continuous_var(
            name="powerPeak{0}".format(GridNet.index)
        )
        """
        电网用电或者发电峰值 实数
        """
        self.baseCost = model1.continuous_var(name="baseCost{0}".format(GridNet.index))
        """
        电网基础费用 实数
        """
        self.powerFrom_max = model1.continuous_var(
            name="powerFrom_max{0}".format(GridNet.index)
        )
        """
        电网用电峰值 实数
        """
        self.powerTo_max = model1.continuous_var(
            name="powerTo_max{0}".format(GridNet.index)
        )
        """
        电网发电峰值 实数
        """

    def constraints_register(self, model: Model, powerPeak_pre:float=2000):
        """
        创建电网的约束条件到模型中
        
        1. 电网要么发电 要么用电 用电时发电量为0 发电时用电量为0 净用电量=用电量-发电量
        2. 电网最大设备数 >= 电网设备数 >= 0
        3. 每小时用电量小于电网设备数
        4. 每小时电网发电量小于电网设备数
        5. 电网一天基础消费 = min( max(用电或者发电峰值, 预估用电峰值) * 31, 电网设备数 * 22)
        6. 电网一天总消费 = sum(每小时用电量 * 用电电价 + 每小时发电量 * 发电消费) + 电网基础消费
        7. 电网年运行成本 = 电网设备数量 * 设备单价 / 15 + 电网一天总消费 * 8760 / 一天小时数
        
        Args:
            model (docplex.mp.model.Model): 求解模型实例
            powerPeak_pre (float): 预估用电峰值
        """
        hourRange = range(0, self.num_hour)
        linearization = Linearization()
        linearization.positive_negitive_constraints_register(
            self.num_hour, model, self.total_power, self.powerFrom, self.powerTo
        )
        model.add_constraint(self.gridNet_device >= 0)
        model.add_constraint(self.gridNet_device <= self.gridNet_device_max)
        model.add_constraints(
            self.powerFrom[h] <= self.gridNet_device for h in hourRange
        )
        model.add_constraints(self.powerTo[h] <= self.gridNet_device for h in hourRange)

        # these are always true, not constraints.
        model.add_constraints(self.powerFrom[h] <= self.powerPeak for h in hourRange) 
        model.add_constraints(self.powerTo[h] <= self.powerPeak for h in hourRange)
        self.powerFrom_max = model1.max(self.powerFrom)
        self.powerTo_max = model1.max(self.powerFrom)
        self.powerPeak = model1.max(self.powerFrom_max, self.powerTo_max)
        
        self.baseCost = (
            model1.min(
                model.max([self.powerPeak, powerPeak_pre]) * 31,
                self.gridNet_device * 22,  # pre?
            )
            * 12
        )

        self.gridNet_cost = (
            model.sum(
                self.powerFrom[h] * self.electricity_price_from[h]
                + self.powerTo[h] * self.electricity_price_to
                for h in hourRange
            )
            + self.baseCost
        )
        model.add_constraint(
            self.annualized
            == self.gridNet_device * self.device_price / 15
            + self.gridNet_cost * 8760 / self.num_hour
        )


class Linearization(object):
    """
    线性化约束类
    """

    bigNumber0 = 1e10
    """
    一个非常大的数,默认为10的10次方
    """
    index: int = 0
    """
    线性约束条件编号
    """

    # bin?
    # never used.

    def product_var_bin(self, model: Model, var_bin: Var, var: Var, bin: BinaryVarType):
        """
        通过二进制变量`bin`的控制,当`bin == 1`,则`var_bin == var`；当`bin == 0`,则`var_bin == 0`

        其中`var`是一个大于0的实数

        每添加一个约束组,编号加一

        Args:
            model (docplex.mp.model.Model): 求解模型实例
            var_bin (Var): 受控变量
            var (Var): 原变量
            bin (BinaryVarType): 控制变量
        """
        Linearization.index += 1
        model.add_constraint(var_bin >= 0)
        # var_bin 大于等于 0
        model.add_constraint(var_bin >= var - (1 - bin) * self.bigNumber0)
        # 如果bin == 0, var_bin 大于等于 (var - 1*bigNumber0)
        # 如果bin == 1, var_bin 大于等于 var
        model.add_constraint(var_bin <= var)  # var_bin 小于等于 var
        model.add_constraint(var_bin <= bin * self.bigNumber0)
        # 如果bin == 0, var_bin 小于等于 0
        # 如果bin == 1, var_bin 小于等于 1*bigNumber0

    def product_var_bins(
        self,
        model: Model,
        var_bin: List[Var],
        var: List[Var],
        bin0: List[BinaryVarType],
        irange: Iterable,
    ):  # bins?
        """
        对于区间`irange`的每个数`i`,通过二进制变量`bin[i]`的控制,当`bin[i] == 1`,则`var_bin[i] == var[i]`；当`bin[i] == 0`,则`var_bin[i] == 0`

        其中`var[i]`是一个大于0的实数

        每添加一个约束组,编号加一

        Args:
            model (docplex.mp.model.Model): 求解模型实例
            var_bin (List[Var]): 受控变量组
            var (List[Var]): 原变量组
            bin (List[BinaryVarType]): 控制变量组
            irange (Iterable): 整数区间
        """
        Linearization.index += 1
        model.add_constraints(var_bin[i] >= 0 for i in irange)
        model.add_constraints(
            var_bin[i] >= var[i] - (1 - bin0[i]) * self.bigNumber0 for i in irange
        )
        model.add_constraints(var_bin[i] <= var[i] for i in irange)
        model.add_constraints(var_bin[i] <= bin0[i] * self.bigNumber0 for i in irange)

    def product_var_back_bins(
        self,
        model: Model,
        var_bin: List[Var],
        var: List[Var],
        bin0: List[BinaryVarType],
        irangeback: Iterable,
    ):  # back?
        """
        对于区间`irange`的每个数`i`,通过二进制变量`bin[i]`的控制,当`bin[i] == 1`,则`var_bin[i] == var[i - 1]`；当`bin[i] == 0`,则`var_bin[i - 1] == 0`

        其中`var[i - 1]`是一个大于0的实数

        每添加一个约束组,编号加一

        Args:
            model (docplex.mp.model.Model): 求解模型实例
            var_bin (List[Var]): 受控变量组
            var (List[Var]): 原变量组
            bin (List[BinaryVarType]): 控制变量组
            irange (Iterable): 整数区间
        """
        Linearization.index += 1
        model.add_constraints(var_bin[i] >= 0 for i in irangeback)
        model.add_constraints(
            var_bin[i] >= var[i - 1] - (1 - bin0[i]) * self.bigNumber0
            for i in irangeback
        )
        model.add_constraints(var_bin[i] <= var[i - 1] for i in irangeback)
        model.add_constraints(
            var_bin[i] <= bin0[i] * self.bigNumber0 for i in irangeback
        )

    def max_zeros(
        self, num_hour: int, model: Model, x: List[Var], y: List[Var]
    ):  # max?
        """
        对于区间`range(0, num_hour)`的每个数`h`,`y[h]`是非负实数,`y_flag[h]`是不同情况对应的二进制变量,约定以下两种情况有且只有一种出现:

        1. `y[h] == 0`,`-bigNumber <= x[h] <= 0`,此时`y_flag[h] == 0`
        2. `y[h] == x[h]`,此时`y_flag[h] == 1`

        每添加一个约束组,编号加一

        Args:
            num_hour (int): 一天小时数
            model (docplex.mp.model.Model): 求解模型实例
            x (List[Var]): 变量组`x`
            y (List[Var]): 变量组`y`
        """
        Linearization.index += 1
        y_flag = model1.binary_var_list(
            [i for i in range(0, num_hour)],
            name="y_flag{0}".format(Linearization.index),
        )
        model.add_constraints(
            y[h] <= x[h] + (1 - y_flag[h]) * bigNumber for h in range(0, num_hour)
        )
        # 当y_flag[h] == 0, y[h] 小于等于 x[h] + bigNumber (此时 -bigNumber <= x[h] )
        # 当y_flag[h] == 1, y[h] 小于等于 x[h]
        model.add_constraints(
            y[h] >= x[h] - (1 - y_flag[h]) * bigNumber for h in range(0, num_hour)
        )
        # 当y_flag[h] == 0, y[h] 大于等于 x[h] - bigNumber (此时 bigNumber >= x[h] )
        # 当y_flag[h] == 1, y[h] 大于等于 x[h] (y[h] == x[h])
        model.add_constraints(y[h] <= y_flag[h] * bigNumber for h in range(0, num_hour))
        # 当y_flag[h] == 0, y[h] 小于等于 0 (此时y[h] == 0)
        # 当y_flag[h] == 1, y[h] 小于等于 bigNumber
        model.add_constraints(x[h] <= y_flag[h] * bigNumber for h in range(0, num_hour))
        # 当y_flag[h] == 0, x[h] 小于等于 0 (-bigNumber<=x[h]<=0) 非正数？
        # 当y_flag[h] == 1, x[h] 小于等于 bigNumber
        model.add_constraints(y[h] >= 0 for h in range(0, num_hour))
        # y[h] 是非负数

    def add(self, num_hour: int, model: Model, x1: List[Var], x2: List[Var]) -> List[Var]:
        """
        对于区间`range(0, num_hour)`的每个数`h`,将两个变量`x1[h]`,`x2[h]`组合为一个变量`add_y[h]`

        每添加一个约束组,编号加一

        Args:
            num_hour (int): 一天小时数
            model (docplex.mp.model.Model): 求解模型实例
            x1 (List[Var]): 变量组`x1`
            x2 (List[Var]): 变量组`x2`

        Return:
            add_y (List[Var]): 两个变量组在指定区间`range(0, num_hour)`内相加的变量
        """
        # looks like two lists.
        Linearization.index += 1
        add_y = model1.continuous_var_list(
            [i for i in range(0, num_hour)], name="add_y{0}".format(Linearization.index)
        )
        model.add_constraints(add_y[h] == x1[h] + x2[h] for h in range(0, num_hour))
        return add_y

    def positive_negitive_constraints_register(
        self,
        num_hour: int,
        model: Model,
        x: List[Var],
        xpositive: List[Var],
        xnegitive: List[Var],
    ):
        """
        对于区间`range(0, num_hour)`的每个数`h`,`x[h] == xpositive[h] - xnegitive[h]`,`positive_flag[h]`是不同情况对应的二进制变量,约定以下两种情况有且只有一种出现:

        1. `xpositive[h] == 0`,`0 <= xnegitive[h] <= bigNumber`,此时`positive_flag[h] == 0`,`x[h] == -xnegitive[h]`
        2. `0 <= xpositive[h] <= bigNumber`,`xnegitive[h] == 0`,此时`positive_flag[h] == 1`,`x[h] == xpositive[h]`

        每添加一个约束组,编号加一

        Args:
            num_hour (int): 一天小时数
            model (docplex.mp.model.Model): 求解模型实例
            x (List[Var]): 存放`xpositive`和`xnegitive`在区间`range(0, num_hour)`内逐元素相减结果约束得到的变量组`x`
            xpositive (List[Var]): 变量组`xpositive`
            xnegitive (List[Var]): 变量组`xnegitive`
        """
        Linearization.index += 1
        bigNumber = 1e10
        positive_flag = model1.binary_var_list(
            [i for i in range(0, num_hour)],
            name="Linearization_positive_flag{0}".format(Linearization.index),
        )
        model.add_constraints(
            x[h] == xpositive[h] - xnegitive[h] for h in range(0, num_hour)
        )
        # 两变量组在区间内逐元素相减 存在传入的元素组x中
        model.add_constraints(xpositive[h] >= 0 for h in range(0, num_hour))
        model.add_constraints(xnegitive[h] >= 0 for h in range(0, num_hour))
        # 两变量组在区间内元素都是非负数
        model.add_constraints(
            xpositive[h] <= bigNumber * positive_flag[h] for h in range(0, num_hour)
        )
        # 当positive_flag[h] == 0,xpositive[h] <= 0 (xpositive[h] == 0)
        # 当positive_flag[h] == 1,xpositive[h] <= bigNumber
        model.add_constraints(
            xnegitive[h] <= bigNumber * (1 - positive_flag[h])
            for h in range(0, num_hour)
        )
        # 当positive_flag[h] == 0,xnegitive[h] <= bigNumber
        # 当positive_flag[h] == 1,xnegitive[h] <= 0 (xnegitive[h] == 0)


load = LoadGet()
power_load = load.get_power_load(num_hour0)
cool_load = load.get_power_load(num_hour0)
heat_load = load.get_power_load(num_hour0)
steam_load = load.get_power_load(num_hour0)

# absolute1 = Linear_absolute(model1, [-5, 6], [0, 1])
# absolute1.absolute_add_constraints(model1)


if __name__ == "__main__":
    resource = ResourceGet()
    # model_input
    intensityOfIllumination0: np.ndarray = resource.get_radiation(
        "jinan_changqing-hour.dat", num_hour0
    )
    # what is the output? break here.

    electricity_price0 = resource.get_electricity_price(num_hour0)
    gas_price0 = resource.get_gas_price(num_hour0)
    municipalHotWater_price0 = resource.get_municipalHotWater_price(num_hour0)
    municipalSteam_price0 = resource.get_municipalSteam_price(num_hour0)
    ####################

    dieselEngine = DieselEngine(num_hour0, model1, 320, 750, 2)  # 柴油机
    dieselEngine.constraints_register(model1)
    photoVoltaic = PhotoVoltaic(
        num_hour0, model1, 5000, 4500, intensityOfIllumination0, 0.8, "PhotoVoltaic"
    )  # 光伏
    photoVoltaic.constraints_register(model1)
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
    batteryEnergyStorageSystem.constraints_register(model1, 1, day_node)
    # highTemperature蒸汽
    troughPhotoThermal = TroughPhotoThermal(
        num_hour0, model1, 5000, 2000, 1000, intensityOfIllumination0, 0.8
    )
    troughPhotoThermal.constraints_register(model1)
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
    gasBoiler = GasBoiler(
        num_hour0,
        model1,
        gasBoiler_device_max=5000,
        gasBoiler_price=200,
        gas_price=gas_price0,
        efficiency=0.9,
    )
    gasBoiler.constraints_register(model1)
    municipalSteam = CitySupply(
        num_hour0,
        model1,
        citySupplied_device_max=5000,
        device_price=3000,
        run_price=0.3 * np.ones(num_hour0),
        efficiency=0.9,
    )
    municipalSteam.constraints_register(model1)
    # 以上为蒸汽发生装置
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
        + gasBoiler.heat_gasBoiler[h]
        for h in range(0, num_hour0)
    )
    # highTemperature蒸汽去处
    model1.add_constraints(
        power_steam_sum[h] >= steam_load[h] + power_steam_used_heatcool[h]
        for h in range(0, num_hour0)
    )
    steamAndWater_exchanger = Exchanger(
        num_hour0, model1, device_max=20000, device_price=400, k=50
    )
    steamAndWater_exchanger.constraints_register(model1)  # qs - 泉水？ steamAndWater热交换器？
    steamPowered_LiBr = LiBrRefrigeration(  # 蒸汽？
        num_hour0, model1, LiBr_device_max=10000, device_price=1000, efficiency=0.9
    )
    steamPowered_LiBr.constraints_register(model1)

    model1.add_constraints(
        power_steam_used_heatcool[h]
        >= steamAndWater_exchanger.heat_exchange[h]
        + steamPowered_LiBr.heat_LiBr_from[h]
        for h in range(0, num_hour0)
    )
    # highTemperaturehotWater
    # 1) combinedHeatAndPower gasTurbineSystem?
    # 2) combinedHeatAndPower wasteGasAndHeat__to_water?
    # 3
    platePhotothermal = PhotoVoltaic(
        num_hour0,
        model1,
        10000,
        500,
        intensityOfIllumination0,
        0.8,
        "platePhotothermal",
    )  # platePhotothermal
    platePhotothermal.constraints_register(model1)
    # 4
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
    # 5
    municipalHotWater = CitySupply(
        num_hour0,
        model1,
        citySupplied_device_max=10000,
        device_price=3000,
        run_price=municipalHotWater_price0,
        efficiency=0.9,
    )
    municipalHotWater.constraints_register(model1)
    # 6
    hotWaterElectricBoiler = ElectricBoiler(
        num_hour0,
        model1,
        electricBoiler_device_max=10000,
        electricBoiler_price=200,
        electricity_price=electricity_price0,
        efficiency=0.9,
    )
    hotWaterElectricBoiler.constraints_register(model1)
    # 7
    gasBoiler_hotWater = GasBoiler(
        num_hour0,
        model1,
        gasBoiler_device_max=20000,
        gasBoiler_price=200,
        gas_price=gas_price0,
        efficiency=0.9,
    )
    gasBoiler_hotWater.constraints_register(model1)
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

    waterStorageTank.constraints_register(model1, 1, day_node)
    # highTemperaturehotWater合计
    power_highTemperaturehotWater_sum = model1.continuous_var_list(
        [i for i in range(0, num_hour0)], name="power_highTemperaturehotWater_sum"
    )
    model1.add_constraints(
        power_highTemperaturehotWater_sum[h]
        == combinedHeatAndPower.gasTurbineSystem_device.heat_exchange[h]
        + combinedHeatAndPower.wasteGasAndHeat_water_device.heat_exchange[
            h
        ]  # wasteGasAndHeat_？
        + platePhotothermal.power_photoVoltaic[h]
        + phaseChangeHeatStorage.power_energyStorageSystem[h]
        + municipalHotWater.heat_citySupplied[h]
        + gasBoiler_hotWater.heat_gasBoiler[h]
        + hotWaterElectricBoiler.heat_electricBoiler[h]
        + waterStorageTank.power_waterStorageTank_gheat[h]
        for h in range(0, num_hour0)
    )

    # hotWaterLiBr
    hotWaterLiBr = LiBrRefrigeration(
        num_hour0, model1, LiBr_device_max=10000, device_price=1000, efficiency=0.9
    )
    hotWaterLiBr.constraints_register(model1)
    # hotWaterExchanger
    hotWaterExchanger = Exchanger(
        num_hour0, model1, device_max=20000, device_price=400, k=50
    )
    hotWaterExchanger.constraints_register(model1)
    # highTemperaturehotWater去向
    model1.add_constraints(
        power_highTemperaturehotWater_sum[h]
        >= hotWaterLiBr.heat_LiBr_from[h] + hotWaterExchanger.heat_exchange[h]
        for h in range(0, num_hour0)
    )
    model1.add_constraints(
        power_highTemperaturehotWater_sum[h] >= 0 for h in range(0, num_hour0)
    )

    # power_heatPump[h]*heatPump_flag[h]+power_waterStorageTank[h]*waterStorageTank_flag[h]+power_waterCooledScrewMachine[h]*waterSourceHeatPumps_flag[h]+power_LiBr[h]+power_waterCooledScrewMachine[h]+power_bx[h]==cool_load[h]%冷量需求
    # power_heatPump[h]*(1-heatPump_flag[h])+power_waterStorageTank[h]*(1-waterStorageTank_flag[h])+power_waterSourceHeatPumps[h]*(1-waterSourceHeatPumps_flag[h])+power_gas[h]+power_groundSourceHeatPump[h]==heat_load[h]%热量需求
    # 采用线性化技巧,处理为下面的约束.基于每种设备要么制热,要么制冷。
    # 供冷:风冷heatPump groundSourceHeatPump 蓄能水罐 hotWaterLiBr机组 蒸汽LiBr机组 phaseChangeRefrigerantStorage
    # 供热:风冷heatPump groundSourceHeatPump 蓄能水罐 地热 水水Exchanger传热
    # heatPump = AirHeatPump(num_hour0, model1, device_max=10000, device_price=1000, electricity_price=electricity_price0)
    # heatPump.constraints_register(model1)

    heatPump = WaterHeatPump(
        num_hour0,
        model1,
        device_max=20000,
        device_price=1000,
        electricity_price=electricity_price0,
        case_ratio=np.array([1, 1, 1, 1]),  # total four cases?
    )
    heatPump.constraints_register(model1)

    waterSourceHeatPumps = WaterHeatPump(
        num_hour0,
        model1,
        device_max=2000,
        device_price=3000,
        electricity_price=electricity_price0,
        case_ratio=np.ones(4),
    )
    waterSourceHeatPumps.constraints_register(model1)
    waterCooledScrewMachine = WaterCooledScrew(
        num_hour0,
        model1,
        device_max=2000,
        device_price=1000,
        electricity_price=electricity_price0,
        case_ratio=np.array([1, 0.8]),
    )
    waterCooledScrewMachine.constraints_register(model1)
    tripleWorkingConditionUnit = TripleWorkingConditionUnit(
        num_hour0,
        model1,
        device_max=20000,
        device_price=1000,
        electricity_price=electricity_price0,
        case_ratio=[1, 0.8, 0.8],
    )
    tripleWorkingConditionUnit.constraints_register(model1)
    doubleWorkingConditionUnit = DoubleWorkingConditionUnit(
        num_hour0,
        model1,
        device_max=20000,
        device_price=1000,
        electricity_price=electricity_price0,
        case_ratio=[1, 0.8],
    )
    doubleWorkingConditionUnit.constraints_register(model1)
    groundSourceHeatPump = GeothermalHeatPump(
        num_hour0,
        model1,
        device_max=20000,
        device_price=40000,
        electricity_price=electricity_price0,
    )
    groundSourceHeatPump.constraints_register(model1)
    bx = EnergyStorageSystem(  # what is this?
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
    bx.constraints_register(model1)

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

    power_xcool = model1.continuous_var_list(
        [i for i in range(0, num_hour0)], name="power_xcool"
    )
    power_xheat = model1.continuous_var_list(
        [i for i in range(0, num_hour0)], name="power_xheat"
    )
    power_xice = model1.continuous_var_list(
        [i for i in range(0, num_hour0)], name="power_xice"
    )
    # power_heatPump_cool[h]+power_xcool[h]+power_waterSourceHeatPumps_cool[h]+power_zqLiBr[h]+power_hotWaterLiBr[h]+power_waterCooledScrewMachine_cool[h]+power_ice[h]+power_tripleWorkingConditionUnit_cool[h]+power_doubleWorkingConditionUnit_cool[h]==cool_load[h]%冷量需求

    # what is "_x"?
    model1.add_constraints(
        heatPump.power_waterSourceHeatPumps_cool[h]
        + power_xcool[h]
        + waterSourceHeatPumps.power_waterSourceHeatPumps_cool[h]
        + steamPowered_LiBr.cool_LiBr[h]
        + hotWaterLiBr.cool_LiBr[h]
        + waterCooledScrewMachine.power_waterCooledScrewMachine_cool[h]
        + power_xice[h]
        + tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_cool[h]
        + doubleWorkingConditionUnit.power_doubleWorkingConditionUnit_cool[h]
        == cool_load[h]
        for h in range(0, num_hour0)
    )
    # power_heatPump_heat[h]+power_xheat[h]+power_waterSourceHeatPumps_heat[h]+power_gas_heat[h]+power_ss_heat[h]+power_groundSourceHeatPump[h]+power_tripleWorkingConditionUnit_heat[h]==heat_load[h]%热量需求
    model1.add_constraints(
        heatPump.power_waterSourceHeatPumps_heat[h]
        + power_xheat[h]
        + waterSourceHeatPumps.power_waterSourceHeatPumps_heat[h]
        + steamAndWater_exchanger.heat_exchange[h]
        + hotWaterExchanger.heat_exchange[h]
        + tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_heat[h]
        + groundSourceHeatPump.power_groundSourceHeatPump[h]
        == heat_load[h]
        for h in range(0, num_hour0)
    )
    # 冰蓄冷逻辑组合
    model1.add_constraints(
        tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_ice[h]
        + doubleWorkingConditionUnit.power_doubleWorkingConditionUnit_ice[h]
        + bx.power_energyStorageSystem[h]
        == power_xice[h]
        for h in range(0, num_hour0)
    )
    linearization = Linearization()
    #
    linearization.max_zeros(num_hour0, model1, power_xice, bx.power_energyStorageSystem)
    # 蓄冷逻辑组合
    model1.add_constraints(
        heatPump.power_waterSourceHeatPumps_xcool[h]
        + waterSourceHeatPumps.power_waterSourceHeatPumps_xcool[h]
        + waterCooledScrewMachine.power_waterCooledScrewMachine_xcool[h]
        + waterStorageTank.power_waterStorageTank_cool[h]
        + phaseChangeRefrigerantStorage.power_energyStorageSystem[h]
        == power_xcool[h]
        for h in range(0, num_hour0)
    )
    linearization.max_zeros(
        num_hour0,
        model1,
        power_xcool,
        linearization.add(
            num_hour0,
            model1,
            waterStorageTank.power_waterStorageTank_cool,
            phaseChangeRefrigerantStorage.power_energyStorageSystem,
        ),
    )
    # 蓄热逻辑组合
    model1.add_constraints(
        heatPump.power_waterSourceHeatPumps_xheat[h]
        + waterSourceHeatPumps.power_waterSourceHeatPumps_xheat[h]
        + waterStorageTank.power_waterStorageTank_heat[h]
        + lowphaseChangeHeatStorage.power_energyStorageSystem[h]
        == power_xheat[h]
        for h in range(0, num_hour0)
    )
    linearization.max_zeros(
        num_hour0,
        model1,
        power_xheat,
        linearization.add(
            num_hour0,
            model1,
            waterStorageTank.power_waterStorageTank_heat,
            lowphaseChangeHeatStorage.power_energyStorageSystem,
        ),
    )
    # 电量平衡
    # electricity_groundSourceHeatPump[h] + electricity_waterCooledScrewMachine[h] + electricity_heatPump[h] - power_batteryEnergyStorageSystem[h] - power_photoVoltaic[h] + electricity_waterSourceHeatPumps[h] + power_load[h] - power_combinedHeatAndPower[h] - power_chargeaifa[h] + \
    # power_groundSourceSteamGenerator[h] + power_electricBoiler[h] + electricity_tripleWorkingConditionUnit[h] + electricity_doubleWorkingConditionUnit[h] == total_power[h]
    # 市政电力电流是双向的,其余市政是单向的。

    # what is "chargeaifa" ??

    gridNet = GridNet(
        num_hour0,
        model1,
        gridNet_device_max=200000,
        device_price=0,
        electricity_price_from=electricity_price0,
        electricity_price_to=0.35,
    )
    gridNet.constraints_register(model1, 2000)
    model1.add_constraints(
        groundSourceHeatPump.electricity_groundSourceHeatPump[h]
        + waterCooledScrewMachine.electricity_waterCooledScrewMachine[h]
        + heatPump.electricity_waterSourceHeatPumps[h]
        - batteryEnergyStorageSystem.power_energyStorageSystem[h]
        - photoVoltaic.power_photoVoltaic[h]
        + waterSourceHeatPumps.electricity_waterSourceHeatPumps[h]
        + power_load[h]
        - combinedHeatAndPower.power_combinedHeatAndPower[h]
        - dieselEngine.power_dieselEngine[h]
        + groundSourceSteamGenerator.power_groundSourceSteamGenerator[h]
        + hotWaterElectricBoiler.electricity_electricBoiler[h]
        + tripleWorkingConditionUnit.electricity_tripleWorkingConditionUnit[h]
        + doubleWorkingConditionUnit.electricity_doubleWorkingConditionUnit[h]
        == gridNet.total_power[h]
        for h in range(0, num_hour0)
    )

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
            waterCooledScrewMachine,
            tripleWorkingConditionUnit,
            doubleWorkingConditionUnit,
            groundSourceHeatPump,
            bx,  # ?
            phaseChangeRefrigerantStorage,
            lowphaseChangeHeatStorage,
            gridNet,
        ]
    )
    objective = integratedEnergySystem_device[0].annualized
    for ii in range(1, len(integratedEnergySystem_device)):
        objective = objective + integratedEnergySystem_device[ii].annualized

    model1.minimize(objective)
    model1.print_information()
    # refiner = ConflictRefiner()  # 先实例化ConflictRefiner类
    # res = refiner.refine_conflict(model1)  # 将模型导入该类,调用方法
    # res.display()  # 显示冲突约束
    print("start calculation:")

    model1.set_time_limit(1000)

    solution_run1: Union[None, SolveSolution] = model1.solve(
        log_output=True
    )  # output some solution.
    # docplex.mp.solution.SolveSolution or None

    if solution_run1 is None:
        from docplex.mp.sdetails import SolveDetails

        print("SOLUTION IS NONE.")
        solution_detail: SolveDetails = model1.solve_details
        print()
        print("SOLVE DETAILS?")
        print(solution_detail)
    else:
        # now we have solution.

        # not model1.solve_details, which always return:
        # docplex.mp.sdetails.SolveDetails

        # print('absolute2 value:')
        # print(solution_run1.get_value(absolute1.absolute_x[1]))
        print("__SOLVE_DETAILS__")
        print(solution_run1.solve_details)
        print("__SOLVE_DETAILS__")

        # ii = 0

        print("objective: annual", solution_run1.get_value(objective))
        for index, item in enumerate(integratedEnergySystem_device):
            subitems = dir(item)
            print(f"objective index: {index}")
            print(f"objective class: {type(item).__name__}")
            for subitem in subitems:
                if subitem.endswith("_device"):
                    val = item.__dict__[subitem]
                    print("value name:", subitem)
                    print("value:", val)
            print("_____")
        # ii += 1
        # print(
        #     "objective:{0}".format(ii),
        #     solution_run1.get_value(
        #         integratedEnergySystem_device[ii].photoVoltaic_device # 1
        #     ),
        # )
        # ii += 1
        # print(
        #     "objective:{0}".format(ii),
        #     solution_run1.get_value(
        #         integratedEnergySystem_device[ii].energyStorageSystem_device #2
        #     ),
        # )
        # ii += 1
        # print(
        #     "objective:{0}".format(ii),
        #     solution_run1.get_value(integratedEnergySystem_device[ii].troughPhotoThermal_device),#3
        # )
        # ii += 1
        # print(
        #     "objective:{0}".format(ii),
        #     solution_run1.get_value(integratedEnergySystem_device[ii].groundSourceSteamGenerator_device),#4
        # )
        # ii += 1
        # print(
        #     "objective:{0}".format(ii),
        #     solution_run1.get_value(
        #         integratedEnergySystem_device[ii].combinedHeatAndPower_device
        #     ),#5
        # )
        # ii += 1
        # print(
        #     "objective:{0}".format(ii),
        #     solution_run1.get_value(integratedEnergySystem_device[ii].gasBoiler_device),#6
        # )
        # ii += 1
        # print(
        #     "objective:{0}".format(ii),
        #     solution_run1.get_value(integratedEnergySystem_device[ii].exchanger_device),#7
        # )
        # ii += 1
        # print(
        #     "objective:{0}".format(ii),
        #     solution_run1.get_value(integratedEnergySystem_device[ii].LiBr_device),#8
        # )
        # ii += 1
        # print(
        #     "objective:{0}".format(ii),
        #     solution_run1.get_value(
        #         integratedEnergySystem_device[ii].photoVoltaic_device #9
        #     ),
        # )
        # ii += 1
        # print(
        #     "objective:{0}".format(ii),
        #     solution_run1.get_value(
        #         integratedEnergySystem_device[ii].energyStorageSystem_device
        #     ),#10
        # )
        # ii += 1
        print()
        print("___INTEGER DECISION VARIABLES___")
        for variable in model1.iter_integer_vars():
            print("INT", variable, "=", variable.solution_value)
        print("___INTEGER DECISION VARIABLES___")
        print()

        print()
        print("___CONTINUOUS DECISION VARIABLES___")
        for variable in model1.iter_continuous_vars():
            print("CONT", variable, "=", variable.solution_value)
        print("___CONTINUOUS DECISION VARIABLES___")
        print()

        print()
        print("___BINARY DECISION VARIABLES___")
        for variable in model1.iter_binary_vars():
            print("BIN", variable, "=", variable.solution_value)
        print("___BINARY DECISION VARIABLES___")
        print()

        # for v in model1.iter_continuous_vars():
        #     print(v, "=", v.solution_value)

        value = Value(solution_run1)

        # plt.plot(value.value(batteryEnergyStorageSystem.power_energyStorageSystem))
        # print(value.value(batteryEnergyStorageSystem.energyStorageSystem_device))

        # plt.figure()

        def plotSingle(data, title_content):
            fig = plt.figure()
            plt.plot(data)
            plt.xlabel("Time/h")
            plt.ylabel("Power/kW")
            plt.title(title_content)
            plt.savefig("fig/" + title_content + ".png")
            plt.close(fig=fig)

        plotSingle(
            value.value(batteryEnergyStorageSystem.power_energyStorageSystem),
            "BatteryEnergyStorageSystem",
        )

        database = {
            "electricity": {
                "list": [
                    groundSourceHeatPump.electricity_groundSourceHeatPump,
                    waterCooledScrewMachine.electricity_waterCooledScrewMachine,
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
                    "waterCooledScrewMachine.electricity_waterCooledScrewMachine",
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
            "cool": {
                "list": [
                    heatPump.power_waterSourceHeatPumps_cool,
                    power_xcool,
                    waterSourceHeatPumps.power_waterSourceHeatPumps_cool,
                    steamPowered_LiBr.cool_LiBr,  # cooling? 直取？
                    hotWaterLiBr.cool_LiBr,
                    waterCooledScrewMachine.power_waterCooledScrewMachine_cool,
                    power_xice,  # consume?
                    tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_cool,
                    doubleWorkingConditionUnit.power_doubleWorkingConditionUnit_cool,
                ],
                "name": [
                    "heatPump.power_waterSourceHeatPumps_cool",
                    "power_xcool",
                    "waterSourceHeatPumps.power_waterSourceHeatPumps_cool",
                    "steamPowered_LiBr.cool_LiBr",
                    "hotWaterLiBr.cool_LiBr",
                    "waterCooledScrewMachine.power_waterCooledScrewMachine_cool",
                    "power_xice",
                    "tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_cool",
                    "doubleWorkingConditionUnit.power_doubleWorkingConditionUnit_cool",
                ],
            },
            "heat": {
                "list": [
                    heatPump.power_waterSourceHeatPumps_heat,
                    power_xheat,
                    waterSourceHeatPumps.power_waterSourceHeatPumps_heat,
                    steamAndWater_exchanger.heat_exchange,
                    hotWaterExchanger.heat_exchange,
                    tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_heat,
                    groundSourceHeatPump.power_groundSourceHeatPump,
                    heat_load,
                ],
                "name": [
                    "heatPump.power_waterSourceHeatPumps_heat",
                    "power_xheat",
                    "waterSourceHeatPumps.power_waterSourceHeatPumps_heat",
                    "steamAndWater_exchanger.heat_exchange",
                    "hotWaterExchanger.heat_exchange",
                    "tripleWorkingConditionUnit.power_tripleWorkingConditionUnit_heat",
                    "groundSourceHeatPump.power_groundSourceHeatPump",
                    "heat_load",
                ],
            },
            "gwheat": {
                "list": [
                    combinedHeatAndPower.gasTurbineSystem_device.heat_exchange,
                    combinedHeatAndPower.wasteGasAndHeat_water_device.heat_exchange,
                    platePhotothermal.power_photoVoltaic,
                    phaseChangeHeatStorage.power_energyStorageSystem,  # phaseChangeHeatStorage？
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

        for key, value in database.items():
            datalist, names = value["list"], value["name"]
            for data, name in zip(datalist, names):
                plotSingle(data, name)

        # pllist = IntegratedEnergySystemPlot(solution_run1)

        # # pllist.plot_list(  [groundSourceHeatPump.electricity_groundSourceHeatPump, waterCooledScrewMachine.electricity_waterCooledScrewMachine], ['groundSourceHeatPump.electricity_groundSourceHeatPump', 'waterCooledScrewMachine.electricity_waterCooledScrewMachine'], "ele balance")

        # pllist.plot_list(
        #     database["electricity"]["list"],
        #     database["electricity"]["name"],
        #     "ele balance",
        # )
        # plt.figure()
        # pllist.plot_list(database['cool']['list'],database['cool']['name'],
        #     "cool_balance",
        # )

        # plt.figure()
        # pllist.plot_list(database['heat']['list'],database['heat']['name'],
        #     "heat_balance",
        # )
        # plt.figure()
        # pllist.plot_list(database['gwheat']['list'],database['gwheat']['name'],
        #     "gwheat_balance",  # gw?
        # )

        # plt.show()
        # let's not show.
