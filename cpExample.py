#!/usr/bin/python3

from docplex.mp.solution import SolveSolution
import docplex  # modeling with ibm cplex
from docplex.mp.model import Model
import pandas as pd
import numpy as np
import time
import os.path
import math
from docplex.mp.conflict_refiner import ConflictRefiner
import matplotlib.pyplot as plt
from matplotlib import style
from result_processlib import Value
from docplex.mp.dvar import Var
from typing import List

from plot_arr import IGESPlot as IntegratedEnergySystemPlot

localtime1 = time.time()

# create main model
mdl1 = Model(name="buses")


ma = 0  # not using? moving average?
debug = 1
run = 0
year = 1
day_node = 24

node = day_node * 1 * 1
if debug == 0:
    num_h0 = node
else:
    num_h0 = node * year

# a big number
bigM = 10e10

# total simulation rounds?
simulationT = 3600

# every hour of one day?
ha = np.ones(num_h0)


# another name for IES?
class IntegratedEnergySystem(object):
    set_count: int = 0

    def __init__(self, set_name: str):
        self.set_name = set_name
        IntegratedEnergySystem.set_count += 1
        print(
            "IntegratedEnergySystem Define a set named:",
            set_name,
            ", total set count/set number is:",
            IntegratedEnergySystem.set_count,
        )


# 适用于光伏及平板式光热
class PhotoVoltaic(IntegratedEnergySystem):  # Photovoltaic
    index = 0

    def __init__(
        self,
        num_h: int,
        mdl: Model,
        pv_set_max: int,
        set_price: int,  # float?
        ha0: np.ndarray,
        eff: float,  # efficiency
        set_name="PhotoVoltaic",
    ):
        IntegratedEnergySystem(set_name)
        PhotoVoltaic.index += 1  # increase the index whenever another PhotoVoltaic system is created.

        self.pv_set = mdl.continuous_var(name="pv_set{0}".format(PhotoVoltaic.index))
        self.p_pv = mdl.continuous_var_list(
            [i for i in range(0, num_h)], name="p_pv{0}".format(PhotoVoltaic.index)
        )
        self.pv_set_max = pv_set_max
        self.set_price = set_price
        self.num_h = num_h
        # 光照强度
        self.ha = ha0
        self.eff = eff
        self.nianhua = mdl.continuous_var(name="pv_nianhua{0}".format(PhotoVoltaic.index))

    def cons_register(self, mdl: Model):
        mdl.add_constraint(self.pv_set <= self.pv_set_max)
        mdl.add_constraint(self.pv_set >= 0)
        mdl.add_constraints(
            self.p_pv[i] <= self.pv_set * self.eff * self.ha[i]
            for i in range(self.num_h)
        )
        mdl.add_constraint(self.nianhua == self.pv_set * self.set_price / 15)

    def total_cost(self, sol:SolveSolution):
        return sol.get_value(self.pv_set) * self.set_price


# 溴化锂
class LiBrRefrigeration(IntegratedEnergySystem):
    index = 0

    def __init__(
        self,
        num_h: int,
        mdl: Model,
        xhl_set_max: int,
        set_price: int,# what is this set? 
        eff: float,
        set_name: str = "LiBrRefrigeration",
    ):
        IntegratedEnergySystem(set_name)
        LiBrRefrigeration.index += 1
        self.num_h = num_h
        self.xhl_set = mdl.continuous_var(
            name="xhl_set{0}".format(LiBrRefrigeration.index)
        )

        self.h_xhl_from = mdl.continuous_var_list( # iterate through hours in a day?
            [i for i in range(0, self.num_h)],
            name="h_xhl_from{0}".format(LiBrRefrigeration.index),
        )
        self.c_xhl = mdl.continuous_var_list( # the same?
            [i for i in range(0, self.num_h)],
            name="h_xhl{0}".format(LiBrRefrigeration.index),
        )

        self.xhl_set_max = xhl_set_max
        self.set_price = set_price
        self.eff = eff
        self.nianhua = mdl.continuous_var(
            name="xhl_nianhua{0}".format(LiBrRefrigeration.index)
        )

    def cons_register(self, mdl: Model):
        # register constraints
        hrange = range(0, self.num_h)
        mdl.add_constraint(self.xhl_set >= 0)
        mdl.add_constraint(self.xhl_set <= self.xhl_set_max)
        mdl.add_constraints(self.h_xhl_from[h] >= 0 for h in hrange)
        mdl.add_constraints(self.h_xhl_from[h] <= self.xhl_set for h in hrange)
        mdl.add_constraints(
            self.c_xhl[h] == self.h_xhl_from[h] / self.eff for h in hrange
        )
        mdl.add_constraint(self.nianhua == self.xhl_set * self.set_price / 15)


# 柴油
class Diesel(IntegratedEnergySystem):
    index = 0

    def __init__(
        self,
        num_h: int,
        mdl: Model,
        diesel_set_max: int,
        set_price: int,
        run_price: int,
        set_name="diesel",
    ):
        IntegratedEnergySystem(set_name)
        Diesel.index += 1
        self.num_h = num_h
        self.diesel_set = mdl.continuous_var(name="diesel_set{0}".format(Diesel.index))
        self.p_diesel = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="p_diesel{0}".format(Diesel.index)
        )
        self.diesel_set_max = diesel_set_max
        self.set_price = set_price
        self.run_price = run_price
        self.p_sum = mdl.sum(self.p_diesel[i] for i in range(0, self.num_h))
        self.nianhua = mdl.continuous_var(name="diesel_nianhua{0}".format(Diesel.index))

    def cons_register(self, mdl: Model):
        mdl.add_constraint(self.diesel_set <= self.diesel_set_max)
        mdl.add_constraint(self.diesel_set >= 0)
        mdl.add_constraints(
            self.p_diesel[i] <= self.diesel_set for i in range(0, self.num_h)
        )
        mdl.add_constraint(
            self.nianhua
            == self.diesel_set * self.set_price / 15
            + self.p_sum * self.run_price * 8760 / self.num_h
        )

    def total_cost(self, sol:SolveSolution):
        # guess you will have it?
        return sol.get_value(self.diesel_set) * self.set_price


# 储能系统基类
class EnergyStorageSystem(IntegratedEnergySystem):
    index: int = 0

    def __init__(
        self,
        num_h: int,
        mdl: Model,
        ess_set_max: int,
        ess_price: int,
        pcs_price: int,
        c_rate_max: float,
        eff: float,
        ess_init: int,
        soc_min: float,
        soc_max: float,
        set_name: str = "ess",
    ):
        IntegratedEnergySystem(set_name)
        EnergyStorageSystem.index += 1

        self.ess_set = mdl.continuous_var(name="ess_set{0}".format(EnergyStorageSystem.index))
        self.p_ess = mdl.continuous_var_list(
            [i for i in range(0, num_h)], lb=-bigM, name="p_ess{0}".format(EnergyStorageSystem.index)
        )
        # 充电功率
        self.p_ess_ch = mdl.continuous_var_list(
            [i for i in range(0, num_h)], name="p_ess_ch{0}".format(EnergyStorageSystem.index)
        )
        # 放电功率
        self.p_ess_dis = mdl.continuous_var_list(
            [i for i in range(0, num_h)], name="p_ess_dis{0}".format(EnergyStorageSystem.index)
        )
        # 能量
        self.ess = mdl.continuous_var_list(
            [i for i in range(0, num_h)], name="ess{0}".format(EnergyStorageSystem.index)
        )
        self.ess_set_max = ess_set_max
        self.ess_price = ess_price
        self.pcs_price = pcs_price
        self.num_h = num_h
        self.pcs_set = mdl.continuous_var(name="pcs_set{0}".format(EnergyStorageSystem.index))  # pcs
        self.ch_flag = mdl.binary_var_list(
            [i for i in range(0, num_h)], name="bess_ch_flag{0}".format(EnergyStorageSystem.index)
        )  # 充电
        self.dis_flag = mdl.binary_var_list(
            [i for i in range(0, num_h)], name="bess_dis_flag{0}".format(EnergyStorageSystem.index)
        )  # 放电
        # 效率
        self.eff = eff
        self.c_rate_max = c_rate_max
        self.ess_init = ess_init
        self.soc_min = soc_min
        self.soc_max = soc_max
        self.nianhua = mdl.continuous_var(name="ess_nianhua{0}".format(EnergyStorageSystem.index))

    def cons_register(self, mdl:Model, regester_period_constraints=1, day_node=24):
        bigM = 1e10
        irange = range(0, self.num_h)
        mdl.add_constraint(self.ess_set <= self.ess_set_max)
        mdl.add_constraint(self.ess_set >= 0)
        mdl.add_constraint(self.ess_set * self.c_rate_max >= self.pcs_set)
        mdl.add_constraint(self.pcs_set >= 0)
        # 功率拆分
        mdl.add_constraints(
            self.p_ess[i] == -self.p_ess_ch[i] + self.p_ess_dis[i] for i in irange
        )

        mdl.add_constraints(self.p_ess_ch[i] >= 0 for i in irange)
        mdl.add_constraints(self.p_ess_ch[i] <= self.ch_flag[i] * bigM for i in irange)
        mdl.add_constraints(self.p_ess_ch[i] <= self.pcs_set for i in irange)

        mdl.add_constraints(self.p_ess_dis[i] >= 0 for i in irange)
        mdl.add_constraints(
            self.p_ess_dis[i] <= self.dis_flag[i] * bigM for i in irange
        )
        mdl.add_constraints(self.p_ess_dis[i] <= self.pcs_set for i in irange)

        mdl.add_constraints(self.ch_flag[i] + self.dis_flag[i] == 1 for i in irange)
        # 节点必须是24的倍数
        # day_node=24
        for day in range(1, int(self.num_h / day_node) + 1):
            mdl.add_constraints(
                self.ess[i]
                == self.ess[i - 1]
                + (self.p_ess_ch[i] * self.eff - self.p_ess_dis[i] / self.eff)
                * simulationT
                / 3600
                for i in range(1 + day_node * (day - 1), day_node * day)
            )

        mdl.add_constraints(
            self.ess[i] <= self.ess_set * self.soc_max for i in range(1, self.num_h)
        )
        mdl.add_constraints(
            self.ess[i] >= self.ess_set * self.soc_min for i in range(1, self.num_h)
        )
        mdl.add_constraint(
            self.nianhua
            == (self.ess_set * self.ess_price + self.pcs_set * self.pcs_price) / 15
        )

        # 两天之间直接割裂，没有啥关系
        if regester_period_constraints == 1:
            mdl.add_constraints(
                self.ess[i] == self.ess[i - (day_node - 1)]
                for i in range(day_node - 1, self.num_h:int, day_node)
            )
        else:
            # 初始值
            mdl.add_constraint(self.ess[0] == self.ess_init * self.ess_set)
            # 两天之间的连接
            mdl.add_constraints(
                self.ess[i]
                == self.ess[i - 1]
                + (self.p_ess_ch[i] * self.eff - self.p_ess_dis[i] / self.eff)
                * simulationT
                / 3600
                for i in range(day_node, self.num_h, day_node)
            )

    def total_cost(self, sol:SolveSolution):
        return (
            sol.get_value(self.ess_set) * self.ess_price
            + sol.get_value(self.pcs_set) * self.pcs_price
        )


# 可变容量储能
class EnergyStorageSystemVariable(IntegratedEnergySystem):
    index = 0

    def __init__(
        self,
        num_h:int,
        mdl:Model,
        ess_set_max:int,
        ess_price:int,
        pcs_price:int,
        c_rate_max:float,
        eff:float,
        ess_init:int,
        soc_min:float,
        soc_max:float,
        set_name:str="ess_variable",
    ):
        IntegratedEnergySystem(set_name)
        EnergyStorageSystemVariable.index += 1

        self.ess_set = mdl.continuous_var_list(
            [i for i in range(0, num_h)],
            name="essVariable_set{0}".format(EnergyStorageSystemVariable.index),
        )
        self.p_ess = mdl.continuous_var_list(
            [i for i in range(0, num_h)],
            lb=-bigM,
            name="p_essVariable{0}".format(EnergyStorageSystemVariable.index),
        )
        # 充电功率
        self.p_ess_ch = mdl.continuous_var_list(
            [i for i in range(0, num_h)],
            name="p_essVariable_ch{0}".format(EnergyStorageSystemVariable.index),
        )
        # 放电功率
        self.p_ess_dis = mdl.continuous_var_list(
            [i for i in range(0, num_h)],
            name="p_essVariable_dis{0}".format(EnergyStorageSystemVariable.index),
        )
        # 能量
        self.ess = mdl.continuous_var_list(
            [i for i in range(0, num_h)],
            name="essVariable{0}".format(EnergyStorageSystemVariable.index),
        )
        self.ess_set_max = ess_set_max
        self.ess_price = ess_price
        self.pcs_price = pcs_price
        self.num_h = num_h
        self.pcs_set = mdl.continuous_var_list(
            [i for i in range(0, num_h)],
            name="pcs_setVariable{0}".format(EnergyStorageSystemVariable.index),
        )  # pcs
        self.ch_flag = mdl.binary_var_list(
            [i for i in range(0, num_h)],
            name="bessVariable_ch_flag{0}".format(EnergyStorageSystemVariable.index),
        )  # 充电
        self.dis_flag = mdl.binary_var_list(
            [i for i in range(0, num_h)],
            name="bessVariable_dis_flag{0}".format(EnergyStorageSystemVariable.index),
        )  # 放电
        # 效率
        self.eff = eff
        self.c_rate_max = c_rate_max
        self.ess_init = ess_init
        self.soc_min = soc_min
        self.soc_max = soc_max

    def cons_register(self, mdl:Model, regester_period_constraints=1, day_node=24):
        bigM = 1e10
        irange = range(0, self.num_h)
        mdl.add_constraints(self.ess_set[i] <= self.ess_set_max for i in irange)
        mdl.add_constraints(self.ess_set[i] >= 0 for i in irange)
        mdl.add_constraints(
            self.ess_set[i] * self.c_rate_max >= self.pcs_set[i] for i in irange
        )
        mdl.add_constraints(self.pcs_set[i] >= 0 for i in irange)
        # 功率拆分
        mdl.add_constraints(
            self.p_ess[i] == -self.p_ess_ch[i] + self.p_ess_dis[i] for i in irange
        )

        mdl.add_constraints(self.p_ess_ch[i] >= 0 for i in irange)
        mdl.add_constraints(self.p_ess_ch[i] <= self.ch_flag[i] * bigM for i in irange)
        mdl.add_constraints(self.p_ess_ch[i] <= self.pcs_set[i] for i in irange)

        mdl.add_constraints(self.p_ess_dis[i] >= 0 for i in irange)
        mdl.add_constraints(
            self.p_ess_dis[i] <= self.dis_flag[i] * bigM for i in irange
        )
        mdl.add_constraints(self.p_ess_dis[i] <= self.pcs_set[i] for i in irange)

        mdl.add_constraints(self.ch_flag[i] + self.dis_flag[i] == 1 for i in irange)
        for day in range(1, int(self.num_h / day_node) + 1):
            mdl.add_constraints(
                self.ess[i]
                == self.ess[i - 1]
                + (self.p_ess_ch[i] * self.eff - self.p_ess_dis[i] / self.eff)
                * simulationT
                / 3600
                for i in range(1 + day_node * (day - 1), day_node * day)
            )
        mdl.add_constraints(
            self.ess[0] == self.ess_init * self.ess_set[i] for i in range(1, self.num_h)
        )

        mdl.add_constraints(
            self.ess[i] <= self.ess_set[i] * self.soc_max for i in range(1, self.num_h)
        )
        mdl.add_constraints(
            self.ess[i] >= self.ess_set[i] * self.soc_min for i in range(1, self.num_h)
        )

        # 两天之间直接割裂，没有啥关系
        if regester_period_constraints == 1:
            mdl.add_constraints(
                self.ess[i] == self.ess[i - (day_node - 1)]
                for i in range(day_node - 1, self.num_h, day_node)
            )
        else:
            # 初始值
            mdl.add_constraint(self.ess[0] == self.ess_init * self.ess_set)
            # 两天之间的连接
            mdl.add_constraints(
                self.ess[i]
                == self.ess[i - 1]
                + (self.p_ess_ch[i] * self.eff - self.p_ess_dis[i] / self.eff)
                * simulationT
                / 3600
                for i in range(day_node, self.num_h, day_node)
            )


# 槽式光热
class TroughPhotoThermal(IntegratedEnergySystem):
    index = 0

    def __init__(
        self,
        num_h:int,
        mdl:Model,
        csgr_set_max,
        csgr_price,
        csgrgtxr_price,
        ha0,
        eff:float,
        set_name="csgr",
    ):
        IntegratedEnergySystem(set_name)
        TroughPhotoThermal.index += 1
        self.num_h = num_h
        self.csgr_set = mdl.continuous_var(name="csgr_set{0}".format(TroughPhotoThermal.index))
        self.p_csgr = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="p_csgr{0}".format(TroughPhotoThermal.index)
        )
        self.p_csgr_steam = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="p_csgr_steam{0}".format(TroughPhotoThermal.index)
        )
        self.csgr_set_max = csgr_set_max
        self.csgrgtxr_set_max = csgr_set_max * 6
        self.csgr_price = csgr_price
        self.csgrgtxr_price = csgrgtxr_price
        self.ha = ha0  # 光照强度
        self.nianhua = mdl.continuous_var(name="csgr_nianhua{0}".format(TroughPhotoThermal.index))
        self.eff = eff

        self.csgrgtxr_set = EnergyStorageSystem(
            num_h,
            mdl,
            self.csgrgtxr_set_max,
            self.csgrgtxr_price,
            pcs_price=100,
            c_rate_max=2,
            eff=0.9,
            ess_init=1,
            soc_min=0,
            soc_max=1,
        )

    def cons_register(self, mdl: Model):
        hrange = range(0, self.num_h)
        self.csgrgtxr_set.cons_register(mdl)
        mdl.add_constraint(self.csgr_set >= 0)
        mdl.add_constraint(self.csgr_set <= self.csgr_set_max)
        mdl.add_constraints(self.p_csgr[h] >= 0 for h in hrange)
        mdl.add_constraints(
            self.p_csgr[h] <= self.csgr_set * self.ha[h] * self.eff for h in hrange
        )  # 与天气相关
        mdl.add_constraints(
            self.p_csgr[h] + self.csgrgtxr_set.p_ess[h] == self.p_csgr_steam[h]
            for h in hrange
        )  # 槽式光热系统产生的高温
        mdl.add_constraints(0 <= self.p_csgr_steam[h] for h in hrange)  # 约束能量不能倒流
        mdl.add_constraint(
            self.nianhua
            == self.csgr_set * self.csgr_price / 15 + self.csgrgtxr_set.nianhua
        )


# CombinedHeatAndPower设备
# 输入：
class CombinedHeatAndPower(IntegratedEnergySystem):
    index = 0

    def __init__(
        self,
        num_h:int,
        mdl:Model,
        chp_num_max,
        chp_price,
        gas_price,
        chp_single_set,
        drratio,
        set_name="chp",
    ):
        IntegratedEnergySystem(set_name)
        CombinedHeatAndPower.index += 1
        self.num_h = num_h
        self.chp_set = mdl.continuous_var(name="chp_set{0}".format(CombinedHeatAndPower.index))
        self.p_chp = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="p_chp{0}".format(CombinedHeatAndPower.index)
        )
        self.h_chp = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="h_chp{0}".format(CombinedHeatAndPower.index)
        )
        self.gas_chp = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="gas_chp{0}".format(CombinedHeatAndPower.index)
        )  # 时时耗气量
        self.chp_price = chp_price
        self.gas_price = gas_price
        self.chp_open_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)], name="chp_open_flag{0}".format(CombinedHeatAndPower.index)
        )
        self.yqyrwater_flag = mdl.binary_var(name="yqyrwater_flag{0}".format(CombinedHeatAndPower.index))
        self.yqyrsteam_flag = mdl.binary_var(name="yqyrsteam_flag{0}".format(CombinedHeatAndPower.index))
        # 机组数量
        self.chp_run_num = mdl.integer_var_list(
            [i for i in range(0, self.num_h)], name="chp_run_num{0}".format(CombinedHeatAndPower.index)
        )
        self.chp_num = mdl.integer_var(name="chp_num{0}".format(CombinedHeatAndPower.index))
        self.nianhua = mdl.continuous_var(name="chp_nianhua{0}".format(CombinedHeatAndPower.index))
        self.gas_cost = mdl.continuous_var(
            name="CombinedHeatAndPower_gas_cost{0}".format(CombinedHeatAndPower.index)
        )  # 燃气费用统计
        self.chp_num_max = chp_num_max
        self.chp_single_set = chp_single_set
        self.chp_limit_down_ratio = 0.2
        self.drratio = drratio
        self.gts_set = Exchanger(
            self.num_h, mdl, self.chp_set * 0.5, set_price=300, k=0
        )
        self.yqyrwater_set = Exchanger(
            self.num_h, mdl, self.chp_set * 0.5, set_price=300, k=0
        )
        self.yqyrsteam_set = Exchanger(
            self.num_h, mdl, self.chp_set * 0.5, set_price=300, k=0
        )

    def cons_register(self, mdl: Model):
        hrange = range(0, self.num_h)
        mdl.add_constraint(self.chp_num >= 0)
        mdl.add_constraint(self.chp_num <= self.chp_num_max)
        mdl.add_constraint(self.chp_set == self.chp_num * self.chp_single_set)
        mdl.add_constraints(
            self.chp_open_flag[h] * self.chp_single_set * self.chp_limit_down_ratio
            <= self.p_chp[h]
            for h in hrange
        )
        # p_chp(1, h) <= chp_set * chp_open_flag(1, h) % chp功率限制, 采用线性化约束，有以下等效：
        mdl.add_constraints(self.p_chp[h] <= self.chp_set for h in hrange)
        mdl.add_constraints(
            self.p_chp[h] <= self.chp_open_flag[h] * bigM for h in hrange
        )
        # p_chp[h]>= 0
        # p_chp(1, h) >= chp_set - (1 - chp_open_flag[h]) * bigM
        mdl.add_constraints(
            self.chp_run_num[h] * self.chp_single_set >= self.p_chp[h] for h in hrange
        )  # 确定CombinedHeatAndPower开启台数
        mdl.add_constraints(
            self.chp_run_num[h] * self.chp_single_set
            <= self.p_chp[h] + self.chp_single_set + 1
            for h in hrange
        )  # 确定CombinedHeatAndPower开启台数
        mdl.add_constraints(0 <= self.chp_run_num[h] for h in hrange)
        mdl.add_constraints(self.chp_run_num[h] <= self.chp_num for h in hrange)
        mdl.add_constraints(
            self.p_chp[h] * self.drratio == self.h_chp[h] for h in hrange
        )
        mdl.add_constraints(self.gas_chp[h] == self.p_chp[h] / 3.5 for h in hrange)

        self.gas_cost = mdl.sum(
            self.gas_chp[h] * self.gas_price[h] for h in hrange
        )  # 统计燃气费用
        #
        mdl.add_constraint(self.yqyrwater_flag + self.yqyrsteam_flag == 1)
        mdl.add_constraint(self.yqyrwater_set.exch_set <= self.yqyrwater_flag * bigM)
        mdl.add_constraint(self.yqyrsteam_set.exch_set <= self.yqyrsteam_flag * bigM)
        mdl.add_constraints(
            self.gts_set.h_exch[h] <= self.h_chp[h] * 0.5 for h in hrange
        )
        mdl.add_constraints(
            self.yqyrwater_set.h_exch[h] <= self.h_chp[h] * 0.5 for h in hrange
        )
        mdl.add_constraints(
            self.yqyrsteam_set.h_exch[h] <= self.h_chp[h] * 0.5 for h in hrange
        )

        mdl.add_constraint(
            self.nianhua
            == self.chp_num * self.chp_single_set * self.chp_price / 15
            + self.gts_set.nianhua
            + self.yqyrwater_set.nianhua
            + self.yqyrsteam_set.nianhua
            + self.gas_cost * 8760 / self.num_h
        )


# 燃气锅炉：蒸汽，热水
class GasBoiler(IntegratedEnergySystem):
    index = 0

    def __init__(
        self, num_h:int, mdl:Model, gasgl_set_max, gasgl_price, gas_price, eff:float, set_name="gasgl"
    ):
        IntegratedEnergySystem(set_name)
        GasBoiler.index += 1
        self.num_h = num_h
        self.gasgl_set = mdl.continuous_var(name="gasgl_set{0}".format(GasBoiler.index))

        self.h_gasgl = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="h_gasgl{0}".format(GasBoiler.index)
        )
        self.gas_gasgl = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="gas_gasgl{0}".format(GasBoiler.index)
        )  # 时时耗气量
        self.gasgl_set_max = gasgl_set_max
        self.gasgl_price = gasgl_price
        self.gas_price = gas_price
        self.eff = eff
        self.gas_cost = mdl.continuous_var(name="gasgl_gas_cost{0}".format(GasBoiler.index))
        self.nianhua = mdl.continuous_var(name="gasgl_nianhua{0}".format(GasBoiler.index))

    def cons_register(self, mdl: Model):
        hrange = range(0, self.num_h)
        mdl.add_constraint(self.gasgl_set >= 0)
        mdl.add_constraint(self.gasgl_set <= self.gasgl_set_max)
        mdl.add_constraints(self.h_gasgl[h] >= 0 for h in hrange)
        mdl.add_constraints(
            self.h_gasgl[h] <= self.gasgl_set for h in hrange
        )  # 天然气蒸汽锅炉
        mdl.add_constraints(
            self.gas_gasgl[h] == self.h_gasgl[h] / (10 * self.eff) for h in hrange
        )
        self.gas_cost = mdl.sum(self.gas_gasgl[h] * self.gas_price[h] for h in hrange)
        mdl.add_constraint(
            self.nianhua
            == self.gasgl_set * self.gasgl_price / 15
            + self.gas_cost * 8760 / self.num_h
        )


# 电锅炉
class ElectricBoiler(IntegratedEnergySystem):
    index = 0

    def __init__(
        self, num_h:int, mdl:Model, dgl_set_max, dgl_price, ele_price, eff:float, set_name="dgl"
    ):
        IntegratedEnergySystem(set_name)
        ElectricBoiler.index += 1
        self.num_h = num_h
        self.dgl_set = mdl.continuous_var(name="dgl_set{0}".format(ElectricBoiler.index))
        self.h_dgl = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="h_dgl{0}".format(ElectricBoiler.index)
        )
        self.ele_dgl = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="ele_dgl{0}".format(ElectricBoiler.index)
        )  # 时时耗气量
        self.gas_set_max = dgl_set_max
        self.dgl_price = dgl_price
        self.ele_price = ele_price
        self.eff = eff
        self.ele_cost = mdl.continuous_var(name="ele_cost{0}".format(ElectricBoiler.index))
        self.nianhua = mdl.continuous_var(name="dgl_nianhua{0}".format(ElectricBoiler.index))

    def cons_register(self, mdl: Model):
        hrange = range(0, self.num_h)
        mdl.add_constraint(self.dgl_set >= 0)
        mdl.add_constraint(self.dgl_set <= self.gas_set_max)
        mdl.add_constraints(self.h_dgl[h] >= 0 for h in hrange)
        mdl.add_constraints(self.h_dgl[h] <= self.dgl_set for h in hrange)  # 天然气蒸汽锅炉
        mdl.add_constraints(self.ele_dgl[h] == self.h_dgl[h] / self.eff for h in hrange)
        self.ele_cost = mdl.sum(self.ele_dgl[h] * self.ele_price[h] for h in hrange)
        mdl.add_constraint(
            self.nianhua
            == self.dgl_set * self.dgl_price / 15 + self.ele_cost * 8760 / self.num_h
        )


class Exchanger(IntegratedEnergySystem):
    index = 0

    def __init__(self, num_h:int, mdl:Model, set_max, set_price, k, set_name="exchanger"):
        IntegratedEnergySystem(set_name)
        # k 传热系数
        Exchanger.index += 1
        self.num_h = num_h
        self.exch_set = mdl.continuous_var(
            name="exchanger_set{0}".format(Exchanger.index)
        )
        self.nianhua = mdl.continuous_var(
            name="exchanger_nianhua{0}".format(Exchanger.index)
        )
        self.set_price = set_price
        self.exch_set_max = set_max
        self.h_exch = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="h_exchanger{0}".format(Exchanger.index),
        )

    def cons_register(self, mdl: Model):
        hrange = range(0, self.num_h)
        mdl.add_constraint(self.exch_set >= 0)
        mdl.add_constraint(self.exch_set <= self.exch_set_max)
        mdl.add_constraints(self.h_exch[h] >= 0 for h in hrange)
        mdl.add_constraints(self.h_exch[h] <= self.exch_set for h in hrange)  # 天然气蒸汽锅炉
        mdl.add_constraint(self.nianhua == self.exch_set * self.set_price / 15)


class AirHeatPump(IntegratedEnergySystem):
    index = 0

    def __init__(
        self, num_h:int, mdl:Model, set_max, set_price, ele_price, set_name="air_heat_pump"
    ):
        IntegratedEnergySystem(set_name)
        self.num_h = num_h
        AirHeatPump.index += 1
        self.ele_price = ele_price
        self.rb_set = mdl.continuous_var(name="rb_set{0}".format(AirHeatPump.index))
        self.nianhua = mdl.continuous_var(
            name="AirHeatPump_nianhua{0}".format(AirHeatPump.index)
        )
        self.ele_cost = mdl.continuous_var(
            name="AirHeatPump_ele_cost{0}".format(AirHeatPump.index)
        )
        self.set_price = set_price
        self.set_max = set_max
        self.p_rb_cool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_rb_cool{0}".format(AirHeatPump.index),
        )
        self.cool_rb_out = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="cool_rb_out{0}".format(AirHeatPump.index),
        )

        self.rb_cool_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="rb_cool_flag{0}".format(AirHeatPump.index),
        )

        self.p_rb_xcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_rb_xcool{0}".format(AirHeatPump.index),
        )
        self.xcool_rb_out = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="xcool_rb_out{0}".format(AirHeatPump.index),
        )

        self.rb_xcool_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="rb_xcool_flag{0}".format(AirHeatPump.index),
        )
        self.p_rb_heat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_rb_heat{0}".format(AirHeatPump.index),
        )
        self.heat_rb_out = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="heat_rb_out{0}".format(AirHeatPump.index),
        )
        self.rb_heat_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="rb_heat_flag{0}".format(AirHeatPump.index),
        )
        self.p_rb_xheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_rb_xheat{0}".format(AirHeatPump.index),
        )
        self.xheat_rb_out = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="xheat_rb_out{0}".format(AirHeatPump.index),
        )
        self.rb_xheat_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="rb_xheat_flag{0}".format(AirHeatPump.index),
        )
        self.ele_rb = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ele_rb{0}".format(AirHeatPump.index),
        )
        self.p_rb = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="p_rb{0}".format(AirHeatPump.index)
        )
        self.cop_rb_cool = 3
        self.cop_rb_xcool = 3
        self.cop_rb_heat = 3
        self.cop_rb_xheat = 3

    def cons_register(self, mdl: Model):
        hrange = range(0, self.num_h)
        mdl.add_constraint(0 <= self.rb_set)
        mdl.add_constraint(self.rb_set <= self.set_max)

        mdl.add_constraints(0 <= self.p_rb_cool[h] for h in hrange)
        mdl.add_constraints(
            self.p_rb_cool[h] <= self.cool_rb_out[h] * self.rb_set / 100 for h in hrange
        )
        mdl.add_constraints(
            self.p_rb_cool[h] <= bigM * self.rb_cool_flag[h] for h in hrange
        )

        mdl.add_constraints(0 <= self.p_rb_xcool[h] for h in hrange)
        mdl.add_constraints(
            self.p_rb_xcool[h] <= self.xcool_rb_out[h] * self.rb_set / 100
            for h in hrange
        )
        mdl.add_constraints(
            self.p_rb_xcool[h] <= bigM * self.rb_xcool_flag[h] for h in hrange
        )

        mdl.add_constraints(0 <= self.p_rb_heat[h] for h in hrange)
        mdl.add_constraints(
            self.p_rb_heat[h] <= self.heat_rb_out[h] * self.rb_set / 100 for h in hrange
        )
        mdl.add_constraints(
            self.p_rb_heat[h] <= bigM * self.rb_heat_flag[h] for h in hrange
        )

        mdl.add_constraints(0 <= self.p_rb_xheat[h] for h in hrange)
        mdl.add_constraints(
            self.p_rb_xheat[h] <= self.xheat_rb_out[h] * self.rb_set / 100
            for h in hrange
        )
        mdl.add_constraints(
            self.p_rb_xheat[h] <= bigM * self.rb_xheat_flag[h] for h in hrange
        )

        mdl.add_constraints(
            self.rb_cool_flag[h]
            + self.rb_xcool_flag[h]
            + self.rb_heat_flag[h]
            + self.rb_xheat_flag[h]
            == 1
            for h in hrange
        )
        mdl.add_constraints(
            self.ele_rb[h]
            == self.p_rb_cool[h] / self.cop_rb_cool[h]
            + self.p_rb_xcool[h] / self.cop_rb_xcool[h]
            + self.p_rb_heat[h] / self.cop_rb_heat[h]
            + self.p_rb_xheat[h] / self.cop_rb_xheat[h]
            for h in hrange
        )
        mdl.add_constraints(
            self.p_rb[h]
            == self.p_rb_cool[h]
            + self.p_rb_xcool[h]
            + self.p_rb_heat[h]
            + self.p_rb_xheat[h]
            for h in hrange
        )

        self.ele_cost = mdl.sum(self.ele_rb[h] * self.ele_price[h] for h in hrange)
        # 年化
        mdl.add_constraint(
            self.nianhua
            == self.rb_set * self.set_price / 15 + self.ele_cost * 8760 / self.num_h
        )


# 水源热泵
class WaterHeatPump(IntegratedEnergySystem):
    index = 0

    def __init__(
        self,
        num_h:int,
        mdl:Model,
        set_max,
        set_price,
        ele_price,
        case_ratio,
        set_name="water_heat_pump",
    ):
        IntegratedEnergySystem(set_name)
        # case_ratio 不同工况下制热量/制冷量的比值
        self.num_h = num_h
        WaterHeatPump.index += 1
        self.ele_price = ele_price
        self.sy_set = mdl.continuous_var(name="sy_set{0}".format(WaterHeatPump.index))
        self.nianhua = mdl.continuous_var(
            name="WaterHeatPump_nianhua{0}".format(WaterHeatPump.index)
        )
        self.ele_cost = mdl.continuous_var(
            name="WaterHeatPump_ele_sum{0}".format(WaterHeatPump.index)
        )
        self.set_price = set_price
        self.set_max = set_max
        self.case_ratio = case_ratio

        self.p_sy_cool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_sy_cool{0}".format(WaterHeatPump.index),
        )

        self.sy_cool_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="sy_cool_flag{0}".format(WaterHeatPump.index),
        )

        self.p_sy_xcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_sy_xcool{0}".format(WaterHeatPump.index),
        )

        self.sy_xcool_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="sy_xcool_flag{0}".format(WaterHeatPump.index),
        )
        self.p_sy_heat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_sy_heat{0}".format(WaterHeatPump.index),
        )

        self.sy_heat_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="sy_heat_flag{0}".format(WaterHeatPump.index),
        )
        self.p_sy_xheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_sy_xheat{0}".format(WaterHeatPump.index),
        )

        self.sy_xheat_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="sy_xheat_flag{0}".format(WaterHeatPump.index),
        )
        self.ele_sy = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ele_sy{0}".format(WaterHeatPump.index),
        )
        self.p_sy = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_sy{0}".format(WaterHeatPump.index),
        )
        self.cop_sy_cool = 5
        self.cop_sy_xcool = 5
        self.cop_sy_heat = 5
        self.cop_sy_xheat = 5

    def cons_register(self, mdl: Model):
        hrange = range(0, self.num_h)
        mdl.add_constraint(0 <= self.sy_set)
        mdl.add_constraint(self.sy_set <= self.set_max)

        mdl.add_constraints(0 <= self.p_sy_cool[h] for h in hrange)
        mdl.add_constraints(
            self.p_sy_cool[h] <= self.sy_set * self.case_ratio[0] for h in hrange
        )
        mdl.add_constraints(
            self.p_sy_cool[h] <= bigM * self.sy_cool_flag[h] for h in hrange
        )

        mdl.add_constraints(0 <= self.p_sy_xcool[h] for h in hrange)
        mdl.add_constraints(
            self.p_sy_xcool[h] <= self.sy_set * self.case_ratio[1] for h in hrange
        )
        mdl.add_constraints(
            self.p_sy_xcool[h] <= bigM * self.sy_xcool_flag[h] for h in hrange
        )

        mdl.add_constraints(0 <= self.p_sy_heat[h] for h in hrange)
        mdl.add_constraints(
            self.p_sy_heat[h] <= self.sy_set * self.case_ratio[2] for h in hrange
        )
        mdl.add_constraints(
            self.p_sy_heat[h] <= bigM * self.sy_heat_flag[h] for h in hrange
        )

        mdl.add_constraints(0 <= self.p_sy_xheat[h] for h in hrange)
        mdl.add_constraints(
            self.p_sy_xheat[h] <= self.sy_set * self.case_ratio[3] for h in hrange
        )
        mdl.add_constraints(
            self.p_sy_xheat[h] <= bigM * self.sy_xheat_flag[h] for h in hrange
        )

        mdl.add_constraints(
            self.sy_cool_flag[h]
            + self.sy_xcool_flag[h]
            + self.sy_heat_flag[h]
            + self.sy_xheat_flag[h]
            == 1
            for h in hrange
        )
        mdl.add_constraints(
            self.ele_sy[h]
            == self.p_sy_cool[h] / self.cop_sy_cool
            + self.p_sy_xcool[h] / self.cop_sy_xcool
            + self.p_sy_heat[h] / self.cop_sy_heat
            + self.p_sy_xheat[h] / self.cop_sy_xheat
            for h in hrange
        )
        mdl.add_constraints(
            self.p_sy[h]
            == self.p_sy_cool[h]
            + self.p_sy_xcool[h]
            + self.p_sy_heat[h]
            + self.p_sy_xheat[h]
            for h in hrange
        )

        self.ele_cost = mdl.sum(self.ele_sy[h] * self.ele_price[h] for h in hrange)
        # 年化
        mdl.add_constraint(
            self.nianhua
            == self.sy_set * self.set_price / 15 + self.ele_cost * 8760 / self.num_h
        )


# 水冷螺杆机
class WaterCooledScrew(IntegratedEnergySystem):
    index = 0

    def __init__(
        self,
        num_h:int,
        mdl:Model,
        set_max,
        set_price,
        ele_price,
        case_ratio,
        set_name="water_cooled_screw",
    ):
        IntegratedEnergySystem(set_name)
        self.num_h = num_h
        WaterCooledScrew.index += 1
        self.ele_price = ele_price
        self.slj_set = mdl.continuous_var(
            name="slj_set{0}".format(WaterCooledScrew.index)
        )
        self.nianhua = mdl.continuous_var(
            name="WaterCooledScrew_nianhua{0}".format(WaterCooledScrew.index)
        )
        self.ele_cost = mdl.continuous_var(
            name="WaterCooledScrew_ele_sum{0}".format(WaterCooledScrew.index)
        )
        self.set_price = set_price
        self.set_max = set_max
        self.case_ratio = case_ratio
        self.p_slj_cool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_slj_cool{0}".format(WaterCooledScrew.index),
        )

        self.slj_cool_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="slj_cool_flag{0}".format(WaterCooledScrew.index),
        )

        self.p_slj_xcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_slj_xcool{0}".format(WaterCooledScrew.index),
        )

        self.slj_xcool_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="slj_xcool_flag{0}".format(WaterCooledScrew.index),
        )

        self.ele_slj = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ele_slj{0}".format(WaterCooledScrew.index),
        )
        self.p_slj = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_slj{0}".format(WaterCooledScrew.index),
        )
        self.cop_slj_cool = 5
        self.cop_slj_xcool = 5

    def cons_register(self, mdl: Model):
        hrange = range(0, self.num_h)
        mdl.add_constraint(0 <= self.slj_set)
        mdl.add_constraint(self.slj_set <= self.set_max)

        mdl.add_constraints(0 <= self.p_slj_cool[h] for h in hrange)
        mdl.add_constraints(
            self.p_slj_cool[h] <= self.slj_set * self.case_ratio[0] for h in hrange
        )
        mdl.add_constraints(
            self.p_slj_cool[h] <= bigM * self.slj_cool_flag[h] for h in hrange
        )

        mdl.add_constraints(0 <= self.p_slj_xcool[h] for h in hrange)
        mdl.add_constraints(
            self.p_slj_xcool[h] <= self.slj_set * self.case_ratio[1] for h in hrange
        )
        mdl.add_constraints(
            self.p_slj_xcool[h] <= bigM * self.slj_xcool_flag[h] for h in hrange
        )

        mdl.add_constraints(
            self.slj_cool_flag[h] + self.slj_xcool_flag[h] == 1 for h in hrange
        )
        mdl.add_constraints(
            self.ele_slj[h]
            == self.p_slj_cool[h] / self.cop_slj_cool
            + self.p_slj_xcool[h] / self.cop_slj_xcool
            for h in hrange
        )
        mdl.add_constraints(
            self.p_slj[h] == self.p_slj_cool[h] + self.p_slj_xcool[h] for h in hrange
        )

        self.ele_cost = mdl.sum(self.ele_slj[h] * self.ele_price[h] for h in hrange)
        # 年化
        mdl.add_constraint(
            self.nianhua
            == self.slj_set * self.set_price / 15 + self.ele_cost * 8760 / self.num_h
        )


# 双工况机组
class DoubleWorkingConditionUnit(IntegratedEnergySystem):
    index = 0

    def __init__(
        self, num_h:int, mdl:Model, set_max, set_price, ele_price, case_ratio, set_name="doublegk"
    ):
        IntegratedEnergySystem(set_name)
        self.num_h = num_h
        DoubleWorkingConditionUnit.index += 1
        self.ele_price = ele_price
        self.doublegk_set = mdl.continuous_var(
            name="doublegk_set{0}".format(DoubleWorkingConditionUnit.index)
        )
        self.nianhua = mdl.continuous_var(
            name="DoubleWorkingConditionUnit_nianhua{0}".format(DoubleWorkingConditionUnit.index)
        )
        self.ele_cost = mdl.continuous_var(
            name="DoubleWorkingConditionUnit_ele_sum{0}".format(DoubleWorkingConditionUnit.index)
        )
        self.set_price = set_price
        self.set_max = set_max
        self.case_ratio = case_ratio
        self.p_doublegk_cool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_doublegk_cool{0}".format(DoubleWorkingConditionUnit.index),
        )

        self.doublegk_cool_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="doublegk_cool_flag{0}".format(DoubleWorkingConditionUnit.index),
        )

        self.p_doublegk_ice = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_doublegk_ice{0}".format(DoubleWorkingConditionUnit.index),
        )

        self.doublegk_ice_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="doublegk_ice_flag{0}".format(DoubleWorkingConditionUnit.index),
        )

        self.ele_doublegk = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ele_doublegk{0}".format(DoubleWorkingConditionUnit.index),
        )
        self.p_doublegk = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_doublegk{0}".format(DoubleWorkingConditionUnit.index),
        )
        self.cop_doublegk_cool = 5
        self.cop_doublegk_ice = 5

    # 三工况机组

    def cons_register(self, mdl: Model):
        hrange = range(0, self.num_h)
        mdl.add_constraint(0 <= self.doublegk_set)
        mdl.add_constraint(self.doublegk_set <= self.set_max)

        mdl.add_constraints(0 <= self.p_doublegk_cool[h] for h in hrange)
        mdl.add_constraints(
            self.p_doublegk_cool[h] <= self.doublegk_set * self.case_ratio[0]
            for h in hrange
        )
        mdl.add_constraints(
            self.p_doublegk_cool[h] <= bigM * self.doublegk_cool_flag[h] for h in hrange
        )

        mdl.add_constraints(0 <= self.p_doublegk_ice[h] for h in hrange)
        mdl.add_constraints(
            self.p_doublegk_ice[h] <= self.doublegk_set * self.case_ratio[1]
            for h in hrange
        )
        mdl.add_constraints(
            self.p_doublegk_ice[h] <= bigM * self.doublegk_ice_flag[h] for h in hrange
        )

        mdl.add_constraints(
            self.doublegk_cool_flag[h] + self.doublegk_ice_flag[h] == 1 for h in hrange
        )
        mdl.add_constraints(
            self.ele_doublegk[h]
            == self.p_doublegk_cool[h] / self.cop_doublegk_cool
            + self.p_doublegk_ice[h] / self.cop_doublegk_ice
            for h in hrange
        )
        mdl.add_constraints(
            self.p_doublegk[h] == self.p_doublegk_cool[h] + self.p_doublegk_ice[h]
            for h in hrange
        )

        self.ele_cost = mdl.sum(
            self.ele_doublegk[h] * self.ele_price[h] for h in hrange
        )
        # 年化
        mdl.add_constraint(
            self.nianhua
            == self.doublegk_set * self.set_price / 15
            + self.ele_cost * 8760 / self.num_h
        )


class TripleWorkingConditionUnit(IntegratedEnergySystem):
    index = 0

    def __init__(
        self, num_h:int, mdl:Model, set_max, set_price, ele_price, case_ratio, set_name="threegk"
    ):
        IntegratedEnergySystem(set_name)
        self.num_h = num_h

        TripleWorkingConditionUnit.index += 1
        self.ele_price = ele_price
        self.threegk_set = mdl.continuous_var(
            name="threegk_set{0}".format(TripleWorkingConditionUnit.index)
        )
        self.nianhua = mdl.continuous_var(
            name="TripleWorkingConditionUnit_nianhua{0}".format(TripleWorkingConditionUnit.index)
        )
        self.ele_cost = mdl.continuous_var(
            name="TripleWorkingConditionUnit_ele_sum{0}".format(TripleWorkingConditionUnit.index)
        )
        self.set_price = set_price
        self.set_max = set_max
        self.case_ratio = case_ratio
        self.p_threegk_cool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_threegk_cool{0}".format(TripleWorkingConditionUnit.index),
        )

        self.threegk_cool_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="threegk_cool_flag{0}".format(TripleWorkingConditionUnit.index),
        )

        self.p_threegk_ice = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_threegk_ice{0}".format(TripleWorkingConditionUnit.index),
        )

        self.threegk_ice_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="threegk_ice_flag{0}".format(TripleWorkingConditionUnit.index),
        )

        self.p_threegk_heat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_threegk_heat{0}".format(TripleWorkingConditionUnit.index),
        )

        self.threegk_heat_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="threegk_heat_flag{0}".format(TripleWorkingConditionUnit.index),
        )

        self.ele_threegk = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ele_threegk{0}".format(TripleWorkingConditionUnit.index),
        )
        self.p_threegk = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="p_threegk{0}".format(TripleWorkingConditionUnit.index)
        )
        self.cop_threegk_cool = 5
        self.cop_threegk_ice = 4
        self.cop_threegk_heat = 5

    def cons_register(self, mdl: Model):
        hrange = range(0, self.num_h)
        mdl.add_constraint(0 <= self.threegk_set)
        mdl.add_constraint(self.threegk_set <= self.set_max)

        mdl.add_constraints(0 <= self.p_threegk_cool[h] for h in hrange)
        mdl.add_constraints(
            self.p_threegk_cool[h] <= self.threegk_set * self.case_ratio[0]
            for h in hrange
        )
        mdl.add_constraints(
            self.p_threegk_cool[h] <= bigM * self.threegk_cool_flag[h] for h in hrange
        )

        mdl.add_constraints(0 <= self.p_threegk_ice[h] for h in hrange)
        mdl.add_constraints(
            self.p_threegk_ice[h] <= self.threegk_set * self.case_ratio[1]
            for h in hrange
        )
        mdl.add_constraints(
            self.p_threegk_ice[h] <= bigM * self.threegk_ice_flag[h] for h in hrange
        )

        mdl.add_constraints(0 <= self.p_threegk_heat[h] for h in hrange)
        mdl.add_constraints(
            self.p_threegk_heat[h] <= self.threegk_set * self.case_ratio[2]
            for h in hrange
        )
        mdl.add_constraints(
            self.p_threegk_heat[h] <= bigM * self.threegk_heat_flag[h] for h in hrange
        )

        mdl.add_constraints(
            self.threegk_cool_flag[h]
            + self.threegk_ice_flag[h]
            + self.threegk_heat_flag[h]
            == 1
            for h in hrange
        )
        mdl.add_constraints(
            self.ele_threegk[h]
            == self.p_threegk_cool[h] / self.cop_threegk_cool
            + self.p_threegk_ice[h] / self.cop_threegk_ice
            + self.p_threegk_heat[h] / self.cop_threegk_heat
            for h in hrange
        )
        mdl.add_constraints(
            self.p_threegk[h]
            == self.p_threegk_cool[h] + self.p_threegk_ice[h] + self.p_threegk_heat[h]
            for h in hrange
        )

        self.ele_cost = mdl.sum(self.ele_threegk[h] * self.ele_price[h] for h in hrange)
        # 年化
        mdl.add_constraint(
            self.nianhua
            == self.threegk_set * self.set_price / 15
            + self.ele_cost * 8760 / self.num_h
        )


class GeothermalHeatPump(IntegratedEnergySystem):
    index = 0

    def __init__(
        self, num_h:int, mdl:Model, set_max, set_price, ele_price, set_name="geothermal_heat_pump"
    ):
        IntegratedEnergySystem(set_name)
        self.num_h = num_h
        GeothermalHeatPump.index += 1
        self.ele_price = ele_price
        self.dire_set = mdl.continuous_var(
            name="dire_set{0}".format(GeothermalHeatPump.index)
        )
        self.nianhua = mdl.continuous_var(
            name="GeothermalHeatPump_nianhua{0}".format(GeothermalHeatPump.index)
        )
        self.ele_cost = mdl.continuous_var(
            name="GeothermalHeatPump_ele_sum{0}".format(GeothermalHeatPump.index)
        )
        self.set_price = set_price
        self.set_max = set_max

        self.ele_dire = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ele_dire{0}".format(GeothermalHeatPump.index),
        )
        self.p_dire = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_dire{0}".format(GeothermalHeatPump.index),
        )
        self.cop_dire = 5

    def cons_register(self, mdl: Model):
        hrange = range(0, self.num_h)

        mdl.add_constraint(0 <= self.dire_set)
        mdl.add_constraint(self.dire_set <= self.set_max)

        mdl.add_constraints(0 <= self.p_dire[h] for h in hrange)
        mdl.add_constraints(self.p_dire[h] <= self.dire_set for h in hrange)

        mdl.add_constraints(
            self.ele_dire[h] == self.p_dire[h] / self.cop_dire for h in hrange
        )
        self.ele_cost = mdl.sum(self.ele_dire[h] * self.ele_price[h] for h in hrange)
        # 年化
        mdl.add_constraint(
            self.nianhua
            == self.dire_set * self.set_price / 15 + self.ele_cost * 8760 / self.num_h
        )


# 水蓄能，可续蓄高温，可以蓄低温
# 水蓄能罐，可变容量的储能体
class WaterEnergyStorage(IntegratedEnergySystem):
    # index=0
    def __init__(
        self,
        num_h:int,
        mdl:Model,
        sx_V_max:int,
        v_price:int,
        pcs_price:int,
        c_rate_max:float,
        eff:float,
        ess_init,
        soc_min:float,
        soc_max:float,
        ratio_cool:int,
        ratio_heat:int,
        ratio_gheat:int,
        set_name:str="water_energy_storage",
    ):
        IntegratedEnergySystem(set_name)
        self.num_h = num_h
        self.mdl = mdl
        # 对于水蓄能，优化的变量为水罐的体积
        self.sx = EnergyStorageSystemVariable(
            num_h, mdl, bigM, 0, pcs_price, c_rate_max, eff:float, ess_init, soc_min, soc_max
        )
        self.index = EnergyStorageSystemVariable.index
        self.sx_set_cool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="sx_set_cool{0}".format(self.index)
        )
        self.sx_set_heat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="sx_set_heat{0}".format(self.index)
        )
        self.sx_set_gheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="sx_set_gheat{0}".format(self.index)
        )
        self.v_price = v_price
        self.sx_V_max = sx_V_max
        self.sx_V = mdl.continuous_var(name="sx_V{0}".format(self.index))
        self.sx_cool_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)], name="sx_cool_flag{0}".format(self.index)
        )
        self.sx_heat_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)], name="sx_heat_flag{0}".format(self.index)
        )
        self.sx_gheat_flag = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="sx_gheat_flag{0}".format(self.index),
        )
        self.ratio_cool = ratio_cool
        self.ratio_heat = ratio_heat
        self.ratio_gheat = ratio_gheat
        self.p_sx_cool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="p_sx_cool{0}".format(self.index)
        )
        self.p_sx_heat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="p_sx_heat{0}".format(self.index)
        )
        self.p_sx_gheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="p_sx_gheat{0}".format(self.index)
        )
        self.nianhua = mdl.continuous_var(name="p_sx_nianhua{0}".format(self.index))

    def cons_regester(self, mdl:Model, regester_period_constraints, day_node):
        bigM = 1e10
        hrange = range(0, self.num_h)
        self.sx.cons_register(mdl, regester_period_constraints, day_node)
        # sx_set[h] == sx_cool_flag[h] * sx_V * ratio_cool + sx_heat_flag[h] * sx_V * ratio_heat + sx_gheat_flag[
        #   h] * sx_V * ratio_gheat
        # 用下面的式子进行线性化
        mdl.add_constraint(self.sx_V <= self.sx_V_max)
        mdl.add_constraint(self.sx_V >= 0)
        mdl.add_constraints(
            self.sx.ess_set[h]
            == self.sx_set_cool[h] + self.sx_set_heat[h] + self.sx_set_gheat[h]
            for h in hrange
        )
        # (1)
        mdl.add_constraints(
            self.sx_set_cool[h] <= self.sx_V * self.ratio_cool for h in hrange
        )
        mdl.add_constraints(
            self.sx_set_cool[h] <= self.sx_cool_flag[h] * bigM for h in hrange
        )
        mdl.add_constraints(self.sx_set_cool[h] >= 0 for h in hrange)
        mdl.add_constraints(
            self.sx_set_cool[h]
            >= self.sx_V * self.ratio_cool - (1 - self.sx_cool_flag[h]) * bigM
            for h in hrange
        )
        # (2)
        mdl.add_constraints(
            self.sx_set_heat[h] <= self.sx_V * self.ratio_heat for h in hrange
        )
        mdl.add_constraints(
            self.sx_set_heat[h] <= self.sx_heat_flag[h] * bigM for h in hrange
        )
        mdl.add_constraints(self.sx_set_heat[h] >= 0 for h in hrange)
        mdl.add_constraints(
            self.sx_set_heat[h]
            >= self.sx_V * self.ratio_heat - (1 - self.sx_heat_flag[h]) * bigM
            for h in hrange
        )
        # (3)
        mdl.add_constraints(
            self.sx_set_gheat[h] <= self.sx_V * self.ratio_gheat for h in hrange
        )
        mdl.add_constraints(
            self.sx_set_gheat[h] <= self.sx_gheat_flag[h] * bigM for h in hrange
        )
        mdl.add_constraints(self.sx_set_gheat[h] >= 0 for h in hrange)
        mdl.add_constraints(
            self.sx_set_gheat[h]
            >= self.sx_V * self.ratio_gheat - (1 - self.sx_gheat_flag[h]) * bigM
            for h in hrange
        )
        # % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
        mdl.add_constraints(
            self.sx_cool_flag[h] + self.sx_heat_flag[h] + self.sx_gheat_flag[h] == 1
            for h in hrange
        )  # % 三个方面进行核算。
        # （1） p_sx_cool[h] == p_sx[h] * sx_cool_flag[h]
        # （2）p_sx_heat[h] == p_sx[h] * sx_heat_flag[h]
        # （3）p_sx_gheat[h] == p_sx[h] * sx_gheat_flag[h]
        # 上面的公式进行线性化后，用下面的公式替代
        # (1)

        mdl.add_constraints(
            -bigM * self.sx_cool_flag[h] <= self.p_sx_cool[h] for h in hrange
        )
        mdl.add_constraints(
            self.p_sx_cool[h] <= bigM * self.sx_cool_flag[h] for h in hrange
        )
        mdl.add_constraints(
            self.sx.p_ess[h] - (1 - self.sx_cool_flag[h]) * bigM <= self.p_sx_cool[h]
            for h in hrange
        )
        mdl.add_constraints(
            self.p_sx_cool[h] <= self.sx.p_ess[h] + (1 - self.sx_cool_flag[h]) * bigM
            for h in hrange
        )
        # (2)
        mdl.add_constraints(
            -bigM * self.sx_heat_flag[h] <= self.p_sx_heat[h] for h in hrange
        )
        mdl.add_constraints(
            self.p_sx_heat[h] <= bigM * self.sx_heat_flag[h] for h in hrange
        )
        mdl.add_constraints(
            self.sx.p_ess[h] - (1 - self.sx_heat_flag[h]) * bigM <= self.p_sx_heat[h]
            for h in hrange
        )
        mdl.add_constraints(
            self.p_sx_heat[h] <= self.sx.p_ess[h] + (1 - self.sx_heat_flag[h]) * bigM
            for h in hrange
        )
        # (3)
        mdl.add_constraints(
            -bigM * self.sx_gheat_flag[h] <= self.p_sx_gheat[h] for h in hrange
        )
        mdl.add_constraints(
            self.p_sx_gheat[h] <= bigM * self.sx_gheat_flag[h] for h in hrange
        )
        mdl.add_constraints(
            self.sx.p_ess[h] - (1 - self.sx_gheat_flag[h]) * bigM <= self.p_sx_gheat[h]
            for h in hrange
        )
        mdl.add_constraints(
            self.p_sx_gheat[h] <= self.sx.p_ess[h] + (1 - self.sx_gheat_flag[h]) * bigM
            for h in hrange
        )
        mdl.add_constraint(self.nianhua == self.sx_V * self.v_price / 20)

# 地源蒸汽发生器
class GroundSourceSteamGenerator(IntegratedEnergySystem):
    index = 0

    def __init__(
        self,
        num_h:int,
        mdl:Model,
        dyzqfsq_set_max,
        dyzqfsq_price,
        dyzqfsqgtxr_price,
        ele_price,
        eff:float,
        set_name="dyzqfsq",
    ):
        IntegratedEnergySystem(set_name)
        GroundSourceSteamGenerator.index += 1
        self.num_h = num_h
        self.dyzqfsq_set = mdl.continuous_var(
            name="dyzqfsq_set{0}".format(GroundSourceSteamGenerator.index)
        )
        self.p_dyzqfsq = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="p_dyzqfsq{0}".format(GroundSourceSteamGenerator.index)
        )

        self.p_dyzqfsq_steam = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="p_dyzqfsq_steam{0}".format(TroughPhotoThermal.index),
        )

        self.dyzqfsq_set_max = dyzqfsq_set_max
        self.dyzqfsqgtxr_set_max = dyzqfsq_set_max * 6
        self.dyzqfsq_price = dyzqfsq_price
        self.dyzqfsqgtxr_price = dyzqfsqgtxr_price
        self.ele_price = ele_price

        self.nianhua = mdl.continuous_var(
            name="GroundSourceSteamGenerator_nianhua{0}".format(GroundSourceSteamGenerator.index)
        )
        self.eff = eff

        self.dyzqfsqgtxr_set = EnergyStorageSystem(
            num_h,
            mdl,
            self.dyzqfsqgtxr_set_max,
            self.dyzqfsqgtxr_price,
            pcs_price=0,
            c_rate_max=2,
            eff=0.9,
            ess_init=1,
            soc_min=0,
            soc_max=1,
        )
        self.ele_cost = mdl.continuous_var(
            name="dyzqfsq_ele_cost{0}".format(GroundSourceSteamGenerator.index)
        )

    def cons_register(self, mdl: Model):
        hrange = range(0, self.num_h)
        self.dyzqfsqgtxr_set.cons_register(mdl)
        mdl.add_constraint(self.dyzqfsq_set >= 0)
        mdl.add_constraint(self.dyzqfsq_set <= self.dyzqfsq_set_max)
        mdl.add_constraints(self.p_dyzqfsq[h] >= 0 for h in hrange)
        mdl.add_constraints(
            self.p_dyzqfsq[h] <= self.dyzqfsq_set for h in hrange
        )  # 与天气相关
        mdl.add_constraints(
            self.p_dyzqfsq[h] + self.dyzqfsqgtxr_set.p_ess[h] == self.p_dyzqfsq_steam[h]
            for h in hrange
        )  # 槽式光热系统产生的高温
        mdl.add_constraints(0 <= self.p_dyzqfsq_steam[h] for h in hrange)  # 约束能量不能倒流
        mdl.add_constraints(
            self.ele_cost == self.p_dyzqfsq[h] * self.ele_price[h] for h in hrange
        )
        mdl.add_constraint(
            self.nianhua
            == self.dyzqfsq_set * self.dyzqfsq_price / 15
            + self.dyzqfsqgtxr_set.nianhua
            + self.ele_cost
        )


class ResourceGet(object):
    # 光照资源，超过一年的，将一年数据进行重复
    # light intensity ranging from 0 to 1? not even reaching 0.3
    def get_radiation(self, path: str, num_h: int) -> np.ndarray:
        if os.path.exists(path):
            raw_file = np.loadtxt(path, dtype=float)
            radiation = raw_file[:, 0]
            ha1 = radiation
            for loop in range(1, math.ceil(num_h / 8760)):
                ha1 = np.concatenate((ha1, radiation), axis=0)

            ha2 = ha1[0:num_h] / 1000  # 转化为kW
            return ha2  # shape: 1d array.
        else:
            raise Exception("File not extists.")

    def get_ele_price(self, num_h: int):
        ele_price = np.ones(num_h, dtype=float) * 0.5
        return ele_price

    def get_gas_price(self, num_h: int):
        gas_price = np.ones(num_h, dtype=float) * 2.77
        return gas_price

    def get_cityrs_price(self, num_h: int):
        cityrs_price = np.ones(num_h, dtype=float) * 0.3
        return cityrs_price

    def get_citysteam_price(self, num_h: int):
        citysteam = np.ones(num_h, dtype=float) * 0.3
        return citysteam


class LoadGet(object):
    def get_cool_load(self, num_h):
        cool_load = np.ones(num_h, dtype=float) * 10000
        return cool_load

    def get_heat_load(self, num_h):
        heat_load = np.ones(num_h, dtype=float) * 10000
        return heat_load

    def get_power_load(self, num_h):
        power_load = np.ones(num_h, dtype=float) * 10000
        return power_load

    def get_steam_load(self, num_h):
        steam_load = np.ones(num_h, dtype=float) * 10000
        return steam_load


class Linear_abs(object):
    bigM0 = 1e10
    index = 0

    def __init__(self, mdl:Model, x, irange):
        Linearization.index += 1  # 要增加变量
        self.b_posi = mdl.binary_var_list(
            [i for i in irange], name="b_posi_abs{0}".format(Linear_abs.index)
        )
        self.b_neg = mdl.binary_var_list(
            [i for i in irange], name="b_neg_abs{0}".format(Linear_abs.index)
        )
        self.x_posi = mdl.continuous_var_list(
            [i for i in irange], name="x_posi_abs{0}".format(Linear_abs.index)
        )
        self.x_neg = mdl.continuous_var_list(
            [i for i in irange], name="x_neg_abs{0}".format(Linear_abs.index)
        )
        self.abs_x = mdl.continuous_var_list(
            [i for i in irange], name="abs_x{0}".format(Linear_abs.index)
        )
        self.irange = irange
        self.x = x

    def abs_add_constraints(self, mdl: Model):
        mdl.add_constraints(self.b_posi[i] + self.b_neg[i] == 1 for i in self.irange)
        mdl.add_constraints(self.x_posi[i] >= 0 for i in self.irange)
        mdl.add_constraints(
            self.x_posi[i] <= self.bigM0 * self.b_posi[i] for i in self.irange
        )
        mdl.add_constraints(self.x_neg[i] >= 0 for i in self.irange)
        mdl.add_constraints(
            self.x_neg[i] <= self.bigM0 * self.b_neg[i] for i in self.irange
        )
        mdl.add_constraints(
            self.x[i] == self.x_posi[i] - self.x_neg[i] for i in self.irange
        )
        mdl.add_constraints(
            self.abs_x[i] == self.x_posi[i] + self.x_neg[i] for i in self.irange
        )


# 适用于市政蒸汽，市政热水
class CitySupply(IntegratedEnergySystem):
    index = 0

    def __init__(
        self,
        num_h:int,
        mdl:Model,
        citysupply_set_max,
        set_price,
        run_price,
        eff:float,
        set_name="city_supply",
    ):
        IntegratedEnergySystem(set_name)
        CitySupply.index += 1
        self.num_h = num_h # hours in a day
        self.citysupply_set = mdl.continuous_var(
            name="citysupply_set{0}".format(CitySupply.index)
        )

        self.h_citysupply = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="h_citysupply{0}".format(CitySupply.index),
        )
        self.h_citysupply_from = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="h_citysupply_from{0}".format(CitySupply.index),
        )
        self.citysupply_set_max = citysupply_set_max
        self.run_price = run_price
        self.set_price = set_price

        self.eff = eff
        self.citysupply_cost = mdl.continuous_var(
            name="citysupply_cost{0}".format(CitySupply.index)
        )
        self.nianhua = mdl.continuous_var(
            name="citysupply_nianhua{0}".format(CitySupply.index)
        )

    def cons_register(self, mdl: Model):
        hrange = range(0, self.num_h)
        mdl.add_constraint(self.citysupply_set >= 0)
        mdl.add_constraint(self.citysupply_set <= self.citysupply_set_max)
        mdl.add_constraints(self.h_citysupply[h] >= 0 for h in hrange)
        mdl.add_constraints(self.h_citysupply[h] <= self.citysupply_set for h in hrange)
        mdl.add_constraints(
            self.h_citysupply[h] == self.h_citysupply_from[h] / self.eff for h in hrange
        )
        self.citysupply_cost = mdl.sum(
            self.h_citysupply_from[h] * self.run_price[h] for h in hrange
        )
        mdl.add_constraint(
            self.nianhua
            == self.citysupply_set * self.set_price / 15
            + self.citysupply_cost * 8760 / self.num_h
        )


class GridNet(IntegratedEnergySystem):
    index = 0

    def __init__(
        self,
        num_h:int,
        mdl:Model,
        gridnet_set_max,
        set_price,
        ele_price_from,
        ele_price_to,
        set_name="grid_net",
    ):
        IntegratedEnergySystem(set_name)
        GridNet.index += 1
        self.num_h = num_h
        self.mdl = mdl
        self.gridnet_set = mdl.continuous_var(
            name="gridnet_set{0}".format(GridNet.index)
        )

        self.gridnet_set_max = gridnet_set_max
        self.ele_price_from = ele_price_from
        self.ele_price_to = ele_price_to

        self.set_price = set_price

        self.gridnet_cost = mdl.continuous_var(
            name="gridnet_cost{0}".format(GridNet.index)
        )
        self.nianhua = mdl.continuous_var(
            name="gridnet_nianhua{0}".format(GridNet.index)
        )

        self.total_power = mdl1.continuous_var_list(
            [i for i in range(0, num_h0)],
            lb=-bigM,
            name="total_power {0}".format(GridNet.index),
        )
        self.powerfrom = mdl1.continuous_var_list(
            [i for i in range(0, num_h0)], name="powerfrom{0}".format(GridNet.index)
        )
        self.powerto = mdl1.continuous_var_list(
            [i for i in range(0, num_h0)], name="powerto {0}".format(GridNet.index)
        )
        self.powerpeak = mdl1.continuous_var(name="powerpeak{0}".format(GridNet.index))
        self.basecost = mdl1.continuous_var(name="basecost{0}".format(GridNet.index))
        self.powerfrom_max = mdl1.continuous_var(
            name="powerfrom_max{0}".format(GridNet.index)
        )
        self.powerto_max = mdl1.continuous_var(
            name="powerto_max{0}".format(GridNet.index)
        )

    def cons_register(self, mdl:Model, powerpeak_pre=2000):
        hrange = range(0, self.num_h)
        lin = Linearization()
        lin.posi_neg_cons_regester(
            self.num_h, mdl, self.total_power, self.powerfrom, self.powerto
        )
        mdl.add_constraint(self.gridnet_set >= 0)
        mdl.add_constraint(self.gridnet_set <= self.gridnet_set_max)
        mdl.add_constraints(self.powerfrom[h] <= self.gridnet_set for h in hrange)
        mdl.add_constraints(self.powerto[h] <= self.gridnet_set for h in hrange)

        mdl.add_constraints(self.powerfrom[h] <= self.powerpeak for h in hrange)
        mdl.add_constraints(self.powerto[h] <= self.powerpeak for h in hrange)
        self.powerfrom_max = mdl1.max(self.powerfrom)
        self.powerto_max = mdl1.max(self.powerfrom)
        self.powerpeak = mdl1.max(self.powerfrom_max, self.powerto_max)
        self.basecost = (
            mdl1.min(
                mdl.max([self.powerpeak, powerpeak_pre]) * 31, self.gridnet_set * 22
            )
            * 12
        )

        self.gridnet_cost = (
            mdl.sum(
                self.powerfrom[h] * self.ele_price_from[h]
                + self.powerto[h] * self.ele_price_to
                for h in hrange
            )
            + self.basecost
        )
        mdl.add_constraint(
            self.nianhua
            == self.gridnet_set * self.set_price / 15
            + self.gridnet_cost * 8760 / self.num_h
        )


class Linearization(object):
    bigM0 = 1e10
    index = 0

    def product_var_bin(self, mdl:Model, var_bin, var, bin):
        Linearization.index += 1
        mdl.add_constraint(var_bin >= 0)
        mdl.add_constraint(var_bin >= var - (1 - bin) * self.bigM0)
        mdl.add_constraint(var_bin <= var)
        mdl.add_constraint(var_bin <= bin * self.bigM0)

    def product_var_bins(self, mdl:Model, var_bin, var, bin0, irange):
        Linearization.index += 1
        mdl.add_constraints(var_bin[i] >= 0 for i in irange)
        mdl.add_constraints(
            var_bin[i] >= var[i] - (1 - bin0[i]) * self.bigM0 for i in irange
        )
        mdl.add_constraints(var_bin[i] <= var[i] for i in irange)
        mdl.add_constraints(var_bin[i] <= bin0[i] * self.bigM0 for i in irange)

    def product_var_back_bins(self, mdl:Model, var_bin, var, bin0, irangeback):
        Linearization.index += 1
        mdl.add_constraints(var_bin[i] >= 0 for i in irangeback)
        mdl.add_constraints(
            var_bin[i] >= var[i - 1] - (1 - bin0[i]) * self.bigM0 for i in irangeback
        )
        mdl.add_constraints(var_bin[i] <= var[i - 1] for i in irangeback)
        mdl.add_constraints(var_bin[i] <= bin0[i] * self.bigM0 for i in irangeback)

    def max_zeros(self, num_h:int, mdl:Model, x, y):
        Linearization.index += 1
        y_flag = mdl1.binary_var_list(
            [i for i in range(0, num_h)], name="y_flag{0}".format(Linearization.index)
        )
        mdl.add_constraints(
            y[h] <= x[h] + (1 - y_flag[h]) * bigM for h in range(0, num_h)
        )
        mdl.add_constraints(
            y[h] >= x[h] - (1 - y_flag[h]) * bigM for h in range(0, num_h)
        )
        mdl.add_constraints(y[h] <= y_flag[h] * bigM for h in range(0, num_h))
        mdl.add_constraints(x[h] <= y_flag[h] * bigM for h in range(0, num_h))
        mdl.add_constraints(y[h] >= 0 for h in range(0, num_h))

    def add(self, num_h:int, mdl:Model, x1:List[Var], x2:List[Var]):
        # looks like two lists.
        Linearization.index += 1
        add_y = mdl1.continuous_var_list(
            [i for i in range(0, num_h)], name="add_y{0}".format(Linearization.index)
        )
        mdl.add_constraints(add_y[h] == x1[h] + x2[h] for h in range(0, num_h))
        return add_y

    def posi_neg_cons_regester(self, num_h:int, mdl:Model, x:List[Var], xposi:List[Var], xneg:List[Var]):
        Linearization.index += 1
        bigM = 1e10
        posi_flag = mdl1.binary_var_list(
            [i for i in range(0, num_h)],
            name="Linearization_posi_flag{0}".format(Linearization.index),
        )
        mdl.add_constraints(x[h] == xposi[h] - xneg[h] for h in range(0, num_h))
        mdl.add_constraints(xposi[h] >= 0 for h in range(0, num_h))
        mdl.add_constraints(xneg[h] >= 0 for h in range(0, num_h))
        mdl.add_constraints(xposi[h] <= bigM * posi_flag[h] for h in range(0, num_h))
        mdl.add_constraints(
            xneg[h] <= bigM * (1 - posi_flag[h]) for h in range(0, num_h)
        )


load = LoadGet()
power_load = load.get_power_load(num_h0)
cool_load = load.get_power_load(num_h0)
heat_load = load.get_power_load(num_h0)
steam_load = load.get_power_load(num_h0)

# abs1 = Linear_abs(mdl1, [-5, 6], [0, 1])
# abs1.abs_add_constraints(mdl1)


if __name__ == "__main__":
    resource = ResourceGet()
    ha0: np.ndarray = resource.get_radiation("jinan_changqing-hour.dat", num_h0)
    # what is the output? break here.

    ele_price0 = resource.get_ele_price(num_h0)
    gas_price0 = resource.get_gas_price(num_h0)
    cityrs_price0 = resource.get_cityrs_price(num_h0)
    citysteam_price0 = resource.get_citysteam_price(num_h0)

    diesel = Diesel(num_h0, mdl1, 320, 750, 2)  # 柴油机
    diesel.cons_register(mdl1)
    pv = PhotoVoltaic(num_h0, mdl1, 5000, 4500, ha0, 0.8, "PhotoVoltaic")  # 光伏
    pv.cons_register(mdl1)
    bess = EnergyStorageSystem(
        num_h0,
        mdl1,
        ess_set_max=20000,
        ess_price=1800,
        pcs_price=250,
        c_rate_max=2,
        eff=0.9,
        ess_init=1,
        soc_min=0,  # state of charge
        soc_max=1,
    )
    bess.cons_register(mdl1, 1, day_node)
    # 高温蒸汽
    csgr = TroughPhotoThermal(num_h0, mdl1, 5000, 2000, 1000, ha0, 0.8)
    csgr.cons_register(mdl1)
    dyzqfsq = GroundSourceSteamGenerator(
        num_h0,
        mdl1,
        dyzqfsq_set_max=20000,
        dyzqfsq_price=200,
        dyzqfsqgtxr_price=200,
        ele_price=ele_price0,
        eff=0.9,
    )
    dyzqfsq.cons_register(mdl1)
    chp = CombinedHeatAndPower(
        num_h0,
        mdl1,
        chp_num_max=5,
        chp_price=2000,
        gas_price=gas_price0,
        chp_single_set=2000,
        drratio=1.2,
    )
    chp.cons_register(mdl1)
    gasgl = GasBoiler(
        num_h0, mdl1, gasgl_set_max=5000, gasgl_price=200, gas_price=gas_price0, eff=0.9
    )
    gasgl.cons_register(mdl1)
    shizheng_steam = CitySupply(
        num_h0,
        mdl1,
        citysupply_set_max=5000,
        set_price=3000,
        run_price=0.3 * np.ones(num_h0),
        eff=0.9,
    )
    shizheng_steam.cons_register(mdl1)
    # 以上为蒸汽发生装置
    p_steam_used_product = mdl1.continuous_var_list(
        [i for i in range(0, num_h0)], name="p_steam_used_product"
    )
    p_steam_used_heatcool = mdl1.continuous_var_list(
        [i for i in range(0, num_h0)], name="p_steam_used_heatcool"
    )
    p_steam_sum = mdl1.continuous_var_list(
        [i for i in range(0, num_h0)], name="p_steam_sum "
    )
    mdl1.add_constraints(
        p_steam_sum[h]
        == shizheng_steam.h_citysupply[h]
        + chp.yqyrsteam_set.h_exch[h]
        + csgr.p_csgr_steam[h]
        + dyzqfsq.p_dyzqfsq_steam[h]
        + gasgl.h_gasgl[h]
        for h in range(0, num_h0)
    )
    # 高温蒸汽去处
    mdl1.add_constraints(
        p_steam_sum[h] >= steam_load[h] + p_steam_used_heatcool[h]
        for h in range(0, num_h0)
    )
    qs_exchanger = Exchanger(num_h0, mdl1, set_max=20000, set_price=400, k=50)
    qs_exchanger.cons_register(mdl1)
    zq_xhl = LiBrRefrigeration(num_h0, mdl1, xhl_set_max=10000, set_price=1000, eff=0.9)
    zq_xhl.cons_register(mdl1)

    mdl1.add_constraints(
        p_steam_used_heatcool[h] >= qs_exchanger.h_exch[h] + zq_xhl.h_xhl_from[h]
        for h in range(0, num_h0)
    )
    # 高温热水
    # 1) chp gts
    # 2) chp yqyr_to_water
    # 3
    pbgr = PhotoVoltaic(num_h0, mdl1, 10000, 500, ha0, 0.8, "pbgr")  # 平板光热
    pbgr.cons_register(mdl1)
    # 4
    xbxr = EnergyStorageSystem(
        num_h0,
        mdl1,
        ess_set_max=10000,
        ess_price=350,
        pcs_price=0,
        c_rate_max=0.5,
        eff=0.9,
        ess_init=1,
        soc_min=0,
        soc_max=1,
    )
    xbxr.cons_register(mdl1)
    # 5
    szrs = CitySupply(
        num_h0,
        mdl1,
        citysupply_set_max=10000,
        set_price=3000,
        run_price=cityrs_price0,
        eff=0.9,
    )
    szrs.cons_register(mdl1)
    # 6
    rsdgl = ElectricBoiler(
        num_h0, mdl1, dgl_set_max=10000, dgl_price=200, ele_price=ele_price0, eff=0.9
    )
    rsdgl.cons_register(mdl1)
    # 7
    gasgl_rs = GasBoiler(
        num_h0,
        mdl1,
        gasgl_set_max=20000,
        gasgl_price=200,
        gas_price=gas_price0,
        eff=0.9,
    )
    gasgl_rs.cons_register(mdl1)
    sx = WaterEnergyStorage(
        num_h0,
        mdl1,
        sx_V_max=10000,
        v_price=300,
        pcs_price=1,
        c_rate_max=0.5,
        eff=0.9,
        ess_init=1,
        soc_min=0,
        soc_max=1,
        ratio_cool=10,
        ratio_heat=10,
        ratio_gheat=20,
    )

    sx.cons_regester(mdl1, 1, day_node)
    # 高温热水合计
    p_gws_sum = mdl1.continuous_var_list(
        [i for i in range(0, num_h0)], name="p_gws_sum "
    )
    mdl1.add_constraints(
        p_gws_sum[h]
        == chp.gts_set.h_exch[h]
        + chp.yqyrwater_set.h_exch[h]
        + pbgr.p_pv[h]
        + xbxr.p_ess[h]
        + szrs.h_citysupply[h]
        + gasgl_rs.h_gasgl[h]
        + rsdgl.h_dgl[h]
        + sx.p_sx_gheat[h]
        for h in range(0, num_h0)
    )

    # 热水溴化锂
    rs_xhl = LiBrRefrigeration(num_h0, mdl1, xhl_set_max=10000, set_price=1000, eff=0.9)
    rs_xhl.cons_register(mdl1)
    # 热水换热器
    ss_exchanger = Exchanger(num_h0, mdl1, set_max=20000, set_price=400, k=50)
    ss_exchanger.cons_register(mdl1)
    # 高温热水去向
    mdl1.add_constraints(
        p_gws_sum[h] >= rs_xhl.h_xhl_from[h] + ss_exchanger.h_exch[h]
        for h in range(0, num_h0)
    )
    mdl1.add_constraints(p_gws_sum[h] >= 0 for h in range(0, num_h0))

    # p_rb[h]*rb_flag[h]+p_sx[h]*sx_flag[h]+p_slj[h]*sy_flag[h]+p_xhl[h]+p_slj[h]+p_bx[h]==cool_load[h]%冷量需求
    # p_rb[h]*(1-rb_flag[h])+p_sx[h]*(1-sx_flag[h])+p_sy[h]*(1-sy_flag[h])+p_gas[h]+p_dire[h]==heat_load[h]%热量需求
    # 采用线性化技巧，处理为下面的约束.基于每种设备要么制热,要么制冷。
    # 供冷：风冷热泵 地源热泵 蓄能水罐 热水溴化锂机组 蒸汽溴化锂机组 相变蓄冷
    # 供热：风冷热泵 地源热泵 蓄能水罐 地热 水水换热器传热
    # rb = AirHeatPump(num_h0, mdl1, set_max=10000, set_price=1000, ele_price=ele_price0)
    # rb.cons_register(mdl1)

    rb = WaterHeatPump(
        num_h0,
        mdl1,
        set_max=20000,
        set_price=1000,
        ele_price=ele_price0,
        case_ratio=np.array([1, 1, 1, 1]),
    )
    rb.cons_register(mdl1)

    sy = WaterHeatPump(
        num_h0,
        mdl1,
        set_max=2000,
        set_price=3000,
        ele_price=ele_price0,
        case_ratio=np.ones(4),
    )
    sy.cons_register(mdl1)
    slj = WaterCooledScrew(
        num_h0,
        mdl1,
        set_max=2000,
        set_price=1000,
        ele_price=ele_price0,
        case_ratio=np.array([1, 0.8]),
    )
    slj.cons_register(mdl1)
    sangk = TripleWorkingConditionUnit(
        num_h0,
        mdl1,
        set_max=20000,
        set_price=1000,
        ele_price=ele_price0,
        case_ratio=[1, 0.8, 0.8],
    )
    sangk.cons_register(mdl1)
    doublegk = DoubleWorkingConditionUnit(
        num_h0,
        mdl1,
        set_max=20000,
        set_price=1000,
        ele_price=ele_price0,
        case_ratio=[1, 0.8],
    )
    doublegk.cons_register(mdl1)
    dire = GeothermalHeatPump(
        num_h0, mdl1, set_max=20000, set_price=40000, ele_price=ele_price0
    )
    dire.cons_register(mdl1)
    bx = EnergyStorageSystem(
        num_h0,
        mdl1,
        ess_set_max=20000,
        ess_price=300,
        pcs_price=1,
        c_rate_max=0.5,
        eff=0.9,
        ess_init=1,
        soc_min=0,
        soc_max=1,
    )
    bx.cons_register(mdl1)

    xbxl = EnergyStorageSystem(
        num_h0,
        mdl1,
        ess_set_max=20000,
        ess_price=500,
        pcs_price=1,
        c_rate_max=0.5,
        eff=0.9,
        ess_init=1,
        soc_min=0,
        soc_max=1,
    )
    xbxl.cons_register(mdl1)

    lowxbxr = EnergyStorageSystem(
        num_h0,
        mdl1,
        ess_set_max=20000,
        ess_price=300,
        pcs_price=1,
        c_rate_max=0.5,
        eff=0.9,
        ess_init=1,
        soc_min=0,
        soc_max=1,
    )
    lowxbxr.cons_register(mdl1)

    p_xcool = mdl1.continuous_var_list([i for i in range(0, num_h0)], name="p_xcool ")
    p_xheat = mdl1.continuous_var_list([i for i in range(0, num_h0)], name="p_xheat ")
    p_xice = mdl1.continuous_var_list([i for i in range(0, num_h0)], name="p_xice ")
    # p_rb_cool[h]+p_xcool[h]+p_sy_cool[h]+p_zqxhl[h]+p_rsxhl[h]+p_slj_cool[h]+p_ice[h]+p_sangk_cool[h]+p_doublegk_cool[h]==cool_load[h]%冷量需求

    mdl1.add_constraints(
        rb.p_sy_cool[h]
        + p_xcool[h]
        + sy.p_sy_cool[h]
        + zq_xhl.c_xhl[h]
        + rs_xhl.c_xhl[h]
        + slj.p_slj_cool[h]
        + p_xice[h]
        + sangk.p_threegk_cool[h]
        + doublegk.p_doublegk_cool[h]
        == cool_load[h]
        for h in range(0, num_h0)
    )
    # p_rb_heat[h]+p_xheat[h]+p_sy_heat[h]+p_gas_heat[h]+p_ss_heat[h]+p_dire[h]+p_sangk_heat[h]==heat_load[h]%热量需求
    mdl1.add_constraints(
        rb.p_sy_heat[h]
        + p_xheat[h]
        + sy.p_sy_heat[h]
        + qs_exchanger.h_exch[h]
        + ss_exchanger.h_exch[h]
        + sangk.p_threegk_heat[h]
        + dire.p_dire[h]
        == heat_load[h]
        for h in range(0, num_h0)
    )
    # 冰蓄冷逻辑组合
    mdl1.add_constraints(
        sangk.p_threegk_ice[h] + doublegk.p_doublegk_ice[h] + bx.p_ess[h] == p_xice[h]
        for h in range(0, num_h0)
    )
    lin = Linearization()
    #
    lin.max_zeros(num_h0, mdl1, p_xice, bx.p_ess)
    # 蓄冷逻辑组合
    mdl1.add_constraints(
        rb.p_sy_xcool[h]
        + sy.p_sy_xcool[h]
        + slj.p_slj_xcool[h]
        + sx.p_sx_cool[h]
        + xbxl.p_ess[h]
        == p_xcool[h]
        for h in range(0, num_h0)
    )
    lin.max_zeros(
        num_h0, mdl1, p_xcool, lin.add(num_h0, mdl1, sx.p_sx_cool, xbxl.p_ess)
    )
    # 蓄热逻辑组合
    mdl1.add_constraints(
        rb.p_sy_xheat[h] + sy.p_sy_xheat[h] + sx.p_sx_heat[h] + lowxbxr.p_ess[h]
        == p_xheat[h]
        for h in range(0, num_h0)
    )
    lin.max_zeros(
        num_h0, mdl1, p_xheat, lin.add(num_h0, mdl1, sx.p_sx_heat, lowxbxr.p_ess)
    )
    # 电量平衡
    # ele_dire[h] + ele_slj[h] + ele_rb[h] - p_bess[h] - p_pv[h] + ele_sy[h] + power_load[h] - p_chp[h] - p_chaifa[h] + \
    # p_dyzqfsq[h] + p_dgl[h] + ele_sangk[h] + ele_doublegk[h] == total_power[h]
    # 市政电力电流是双向的，其余市政是单向的。

    gridnet = GridNet(
        num_h0,
        mdl1,
        gridnet_set_max=200000,
        set_price=0,
        ele_price_from=ele_price0,
        ele_price_to=0.35,
    )
    gridnet.cons_register(mdl1, 2000)
    mdl1.add_constraints(
        dire.ele_dire[h]
        + slj.ele_slj[h]
        + rb.ele_sy[h]
        - bess.p_ess[h]
        - pv.p_pv[h]
        + sy.ele_sy[h]
        + power_load[h]
        - chp.p_chp[h]
        - diesel.p_diesel[h]
        + dyzqfsq.p_dyzqfsq[h]
        + rsdgl.ele_dgl[h]
        + sangk.ele_threegk[h]
        + doublegk.ele_doublegk[h]
        == gridnet.total_power[h]
        for h in range(0, num_h0)
    )

    iges_set = [ # all constrains in IES/IntegratedEnergySystem system
        diesel,
        pv,
        bess,
        csgr,
        dyzqfsq,
        chp,
        gasgl,
        qs_exchanger,
        zq_xhl,
        pbgr,
        xbxr,
        szrs,
        rsdgl,
        gasgl_rs,
        sx,
        shizheng_steam,
        rs_xhl,
        ss_exchanger,
        rb,
        sy,
        slj,
        sangk,
        doublegk,
        dire,
        bx,
        xbxl,
        lowxbxr,
        gridnet,
    ]
    obj = iges_set[0].nianhua
    for ii in range(1, len(iges_set)):
        obj = obj + iges_set[ii].nianhua

    mdl1.minimize(obj)
    mdl1.print_information()
    # refiner = ConflictRefiner()  # 先实例化ConflictRefiner类
    # res = refiner.refine_conflict(mdl1)  # 将模型导入该类，调用方法
    # res.display()  # 显示冲突约束
    print("start cal:")

    mdl1.set_time_limit(1000)

    sol_run1 = mdl1.solve(log_output=True) # output some solution.
    # docplex.mp.solution.SolveSolution or None
    
    if sol_run1 is None:
        from docplex.mp.sdetails import SolveDetails
        print("SOLUTION IS NONE.")
        solution_detail:SolveDetails = mdl1.solve_details
        print()
        print("SOLVE DETAILS?")
        print(solution_detail)
    else:
        # now we have solution.
        
        # not mdl1.solve_details, which always return:
        # docplex.mp.sdetails.SolveDetails
        
        # print('abs2 value:')
        # print(sol_run1.get_value(abs1.abs_x[1]))
        print(sol_run1.solve_details)

        ii = 0
        print("obj:{0}".format(ii), sol_run1.get_value(obj))
        ii += 1
        print("obj:{0}".format(ii), sol_run1.get_value(iges_set[ii].pv_set))
        ii += 1
        print("obj:{0}".format(ii), sol_run1.get_value(iges_set[ii].ess_set))
        ii += 1
        print("obj:{0}".format(ii), sol_run1.get_value(iges_set[ii].csgr_set))
        ii += 1
        print("obj:{0}".format(ii), sol_run1.get_value(iges_set[ii].dyzqfsq_set))
        ii += 1
        print("obj:{0}".format(ii), sol_run1.get_value(iges_set[ii].chp_set))
        ii += 1
        print("obj:{0}".format(ii), sol_run1.get_value(iges_set[ii].gasgl_set))
        ii += 1
        print("obj:{0}".format(ii), sol_run1.get_value(iges_set[ii].exch_set))
        ii += 1
        print("obj:{0}".format(ii), sol_run1.get_value(iges_set[ii].xhl_set))
        ii += 1
        print("obj:{0}".format(ii), sol_run1.get_value(iges_set[ii].pv_set))
        ii += 1
        print("obj:{0}".format(ii), sol_run1.get_value(iges_set[ii].ess_set))
        ii += 1

        for v in mdl1.iter_integer_vars():
            print(v, " = ", v.solution_value)
        # for v in mdl1.iter_continuous_vars():
        #     print(v, " = ", v.solution_value)

        value = Value(sol_run1)

        plt.plot(value.value(bess.p_ess))
        print(value.value(bess.ess_set))

        plt.figure()
        pllist = IntegratedEnergySystemPlot(sol_run1)

        # pllist.plot_list(  [dire.ele_dire, slj.ele_slj], ['dire.ele_dire', 'slj.ele_slj'], "ele balance")

        pllist.plot_list(
            [
                dire.ele_dire,
                slj.ele_slj,
                rb.ele_sy,
                bess.p_ess,
                pv.p_pv,
                sy.ele_sy,
                power_load,
                chp.p_chp,
                diesel.p_diesel,
                dyzqfsq.p_dyzqfsq,
                rsdgl.ele_dgl,
                sangk.ele_threegk,
                doublegk.ele_doublegk,
                gridnet.total_power,
            ],
            [
                "dire.ele_dire",
                "slj.ele_slj",
                "rb.ele_sy",
                "bess.p_ess",
                "pv.p_pv",
                "sy.ele_sy",
                "power_load",
                "chp.p_chp",
                "diesel.p_diesel",
                "dyzqfsq.p_dyzqfsq",
                "rsdgl.ele_dgl",
                "sangk.ele_threegk",
                "doublegk.ele_doublegk",
                "gridnet.total_power",
            ],
            "ele balance",
        )
        plt.figure()
        pllist.plot_list(
            [
                rb.p_sy_cool,
                p_xcool,
                sy.p_sy_cool,
                zq_xhl.c_xhl,
                rs_xhl.c_xhl,
                slj.p_slj_cool,
                p_xice,
                sangk.p_threegk_cool,
                doublegk.p_doublegk_cool,
            ],
            [
                "rb.p_sy_cool",
                "p_xcool",
                "sy.p_sy_cool",
                "zq_xhl.c_xhl",
                "rs_xhl.c_xhl",
                "slj.p_slj_cool",
                "p_xice",
                "sangk.p_threegk_cool",
                "doublegk.p_doublegk_cool",
            ],
            "cool_balance",
        )

        plt.figure()
        pllist.plot_list(
            [
                rb.p_sy_heat,
                p_xheat,
                sy.p_sy_heat,
                qs_exchanger.h_exch,
                ss_exchanger.h_exch,
                sangk.p_threegk_heat,
                dire.p_dire,
                heat_load,
            ],
            [
                "rb.p_sy_heat",
                "p_xheat",
                "sy.p_sy_heat",
                "qs_exchanger.h_exch",
                "ss_exchanger.h_exch",
                " sangk.p_threegk_heat",
                "dire.p_dire",
                "heat_load",
            ],
            "heat_balance",
        )
        plt.figure()
        pllist.plot_list(
            [
                chp.gts_set.h_exch,
                chp.yqyrwater_set.h_exch,
                pbgr.p_pv,
                xbxr.p_ess,
                szrs.h_citysupply,
                gasgl_rs.h_gasgl,
                rsdgl.h_dgl,
                sx.p_sx_gheat,
            ],
            [
                "chp.gts_set.h_exchh, chp",
                "yqyrwater_set.h_exch",
                "pbgr.p_pv",
                "xbxr.p_ess",
                "szrs.h_citysupply",
                "gasgl_rs.h_gasgl",
                "rsdgl.h_dgl",
                "sx.p_sx_gheat",
            ],
            "gwheat_balance",
        )

        plt.show()
