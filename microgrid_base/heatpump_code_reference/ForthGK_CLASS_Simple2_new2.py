# !/usr/bin/python3
import docplex
from docplex.mp.model import Model
import pandas as pd
import numpy as np
import time
import os.path
import math
import random

# import sys
from docplex.mp.conflict_refiner import ConflictRefiner
import matplotlib.pyplot as plt
from matplotlib import style
from result_processlib import Value
from plot_arr import IGESPlot
from cpExample import IGES
from SoilSource_new import RRSqure
from Machine_para_fit2 import Set_Para_Fit

heat_para = [
    [38, 0, 0.775, 0.82],
    [38, 6, 0.95, 0.85],
    [38, 12, 1.09, 0.885],
    [45, 0, 0.75, 0.94],
    [45, 6, 0.89, 0.975],
    [45, 12, 1.06, 1.015],
    [50, 0, 0.73, 1.04],
    [50, 6, 0.87, 1.075],
    [50, 12, 1.03, 1.12],
    [55, 0, 0.715, 1.14],
    [55, 6, 0.85, 1.18],
    [55, 12, 1.1, 1.225],
]

cool_para = [
    [4, 20, 0.94, 0.895],
    [4, 28, 0.87, 1.025],
    [4, 35, 0.805, 1.17],
    [7, 20, 1.045, 0.925],
    [7, 28, 0.975, 1.05],
    [7, 35, 0.905, 1.19],
    [9, 20, 1.12, 0.94],
    [9, 28, 1.045, 1.07],
    [9, 35, 0.975, 1.21],
    [10, 20, 1.162, 0.955],
    [10, 28, 1.085, 1.08],
    [10, 35, 1.01, 1.22],
]

set_cool_fit = Set_Para_Fit(cool_para)
set_cool_fit.fit_pkcoeff()
set_cool_fit.fit_pwkcoeff_without_rate()

# acool = set_cool_fit.get_pkcoeff()

set_heat_fit = Set_Para_Fit(heat_para)
set_heat_fit.fit_pkcoeff()
set_heat_fit.fit_pwkcoeff_without_rate()
# aheat = set_heat_fit.get_pkcoeff()

load_rate_cop_cool = [[0.25, 3], [0.5, 5], [0.75, 8], [1, 6]]
load_rate_cop_heat = [[0.25, 3], [0.5, 5], [0.75, 8], [1, 6]]
load_rate_arr_cool = np.zeros([4, 2], dtype=float)
load_rate_arr_heat = np.zeros([4, 2], dtype=float)
for i in range(4):
    load_rate_arr_cool[i][1] = load_rate_cop_cool[i][1] / load_rate_cop_cool[3][1]
    load_rate_arr_cool[i][0] = load_rate_cop_cool[i][0]

    load_rate_arr_heat[i][1] = load_rate_cop_heat[i][1] / load_rate_cop_heat[3][1]
    load_rate_arr_heat[i][0] = load_rate_cop_heat[i][0]

set_cool_fit.fit_pwk_rate_coeff(load_rate_arr_cool)

# bcool = set_cool_fit.get_pwkcoeff()

# set_heat_fit.fit_pwkcoeff(load_rate_arr)
# bheat = set_cool_fit.get_pwkcoeff()
set_heat_fit.fit_pwk_rate_coeff(load_rate_arr_heat)


class ForthGK(IGES):
    index = 0

    def __init__(
        self,
        num_h,
        mdl: Model,
        cool_max,
        cool_min,
        heat_max,
        heat_min,
        set_price,
        ele_price,
        set_name="Forth",
    ):
        IGES(set_name)
        ForthGK.index += 1
        self.nset = mdl.integer_var(name="nset{0}".format(ForthGK.index))
        self.num_h = num_h
        ForthGK.index += 1
        self.average_load_rate = 0.8
        self.ele_price = ele_price
        self.set_price = set_price
        self.cool_max = cool_max
        self.cool_min = cool_min
        self.heat_max = heat_max
        self.heat_min = heat_min

        self.p_rated_cool = 150
        self.p_rated_heat = 160
        self.pw_rated_cool = 30
        self.pw_rated_heat = 30
        self.Tcool_out = 7
        self.Txcool_out = 5
        self.Theat_out = 7
        self.Txheat_out = 5

        self.tpcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="tpcool{0}".format(ForthGK.index)
        )
        self.tpxcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="tpxcool{0}".format(ForthGK.index)
        )
        self.tpheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="tpheat{0}".format(ForthGK.index)
        )
        self.tpxheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="tpxheat{0}".format(ForthGK.index)
        )

        self.tpwcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="tpwcool{0}".format(ForthGK.index)
        )
        self.tpwxcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="tpwxcool{0}".format(ForthGK.index)
        )
        self.tpwheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="tpwheat{0}".format(ForthGK.index)
        )

        self.tpwxheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="tpwxheat{0}".format(ForthGK.index)
        )

        self.tpw = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="tpw{0}".format(ForthGK.index)
        )

        self.Nrun = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="tNrun{0}".format(ForthGK.index)
        )

        self.zcool = mdl.binary_var_list(
            [i for i in range(0, self.num_h)], name="tzcool{0}".format(ForthGK.index)
        )
        self.zxcool = mdl.binary_var_list(
            [i for i in range(0, self.num_h)], name="tzxcool{0}".format(ForthGK.index)
        )
        self.zheat = mdl.binary_var_list(
            [i for i in range(0, self.num_h)], name="tzheat{0}".format(ForthGK.index)
        )
        self.zxheat = mdl.binary_var_list(
            [i for i in range(0, self.num_h)], name="tzxheat{0}".format(ForthGK.index)
        )
        self.nianhua = mdl.continuous_var(name="nianhua{0}".format(ForthGK.index))
        self.ele_cost = mdl.continuous_var(name="ele_cost{0}".format(ForthGK.index))

        self.pincool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="pincool{0}".format(ForthGK.index)
        )
        self.pinheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="pinheat{0}".format(ForthGK.index)
        )
        self.Tin = np.ones(num_h) * 12
        # mdl.continuous_var_list([i for i in range(0, self.num_h)],
        #                                  name='Tin{0}'.format(ForthGK.index))
        self.Nmax = round(self.heat_max / self.p_rated_heat)
        self.nsetopt = 1

        # acool = [1.0850, -0.0099, 0.0001, 0.0252]
        # aheat = [1.0850, -0.0099, 0.0001, 0.0252]

        hrange = range(0, self.num_h)
        """
        self.pset_cool = [(acool[0] + acool[1] * self.Tcool_out + acool[2] * self.Tcool_out * self.Tcool_out + acool[
            3] * self.Tin[h]) * self.p_rated_cool for h in hrange]
        self.pset_xcool = [(acool[0] + acool[1] * self.Txcool_out + acool[2] * self.Txcool_out * self.Txcool_out +
                            acool[3] * self.Tin[h]) * self.p_rated_cool for h in hrange]
        self.pset_heat = [(aheat[0] + aheat[1] * self.Theat_out + aheat[2] * self.Theat_out * self.Theat_out + aheat[
            3] * self.Tin[h]) * self.p_rated_heat for h in hrange]
        self.pset_xheat = [(aheat[0] + aheat[1] * self.Txheat_out + aheat[2] * self.Txheat_out * self.Txheat_out +
                            aheat[3] * self.Tin[h]) * self.p_rated_heat for h in hrange]
                            """

        self.pset_cool = [
            set_cool_fit.get_pk(self.Tcool_out, self.Tin[h]) * self.p_rated_cool
            for h in hrange
        ]
        self.pset_xcool = [
            set_cool_fit.get_pk(self.Txcool_out, self.Tin[h]) * self.p_rated_cool
            for h in hrange
        ]
        self.pset_xheat = [
            set_heat_fit.get_pk(self.Txheat_out, self.Tin[h]) * self.p_rated_heat
            for h in hrange
        ]
        self.pset_heat = [
            set_heat_fit.get_pk(self.Theat_out, self.Tin[h]) * self.p_rated_heat
            for h in hrange
        ]

    # 四工况机组

    def cons_register(self, mdl:Model):
        hrange = range(0, self.num_h)
        mdl.add_constraint(self.nset * self.p_rated_heat >= self.heat_min)
        mdl.add_constraint(self.nset * self.p_rated_cool >= self.cool_min)
        mdl.add_constraint(self.nset * self.p_rated_heat <= self.heat_max)
        mdl.add_constraint(self.nset * self.p_rated_cool <= self.cool_max)

        rb = nRB(self.num_h, mdl, self, set_name="RB")

        mdl.add_constraints(
            self.zcool[h] + self.zxcool[h] + self.zheat[h] + self.zxheat[h] <= 1
            for h in hrange
        )

        mdl.add_constraints(
            self.tpcool[h] + self.tpxcool[h]
            == self.pincool[h] - self.tpwcool[h] - self.tpwxcool[h]
            for h in hrange
        )
        mdl.add_constraints(
            self.tpheat[h] + self.tpxheat[h]
            == self.pinheat[h] + self.tpwheat[h] + self.tpwxheat[h]
            for h in hrange
        )

        self.ele_cost = mdl.sum(
            self.tpw[h] / 3600 * self.simulationT * self.ele_price[h] for h in hrange
        )
        # 年化
        if self.nsetopt == 1:
            mdl.add_constraint(
                self.nianhua
                == self.nset * self.p_rated_cool * self.set_price / 15
                + self.ele_cost * 8760 / self.num_h
            )
        else:
            mdl.add_constraint(
                self.nianhua
                == self.Nmax * self.p_rated_cool * self.set_price / 15
                + self.ele_cost * 8760 / self.num_h
            )
        bigM = 1e8


# 热泵
class nRB(IGES):
    index = 0

    def __init__(self, num_h, mdl: Model, father:FourthGK, set_name="singleRB"):
        IGES(set_name)
        nRB.index += 1
        bigM = 1e8
        self.num_h = num_h

        self.pw_cool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-pw_cool{0}".format(nRB.index),
        )
        self.pw_xcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-pw_xcool{0}".format(nRB.index),
        )
        self.pw_heat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-pw_heat{0}".format(nRB.index),
        )
        self.pw_xheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-pw_xheat{0}".format(nRB.index),
        )
        self.pw = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="singleRB-pw{0}".format(nRB.index)
        )

        """
        self.zpset_xheat = mdl.continuous_var_list([i for i in range(0, self.num_h)],
                                                   name='nRB.zpset_xheat{0}'.format(nRB.index))
        self.zpset_heat = mdl.continuous_var_list([i for i in range(0, self.num_h)],
                                                  name='nRB.zpset_heat{0}'.format(nRB.index))
        self.zpset_xcool = mdl.continuous_var_list([i for i in range(0, self.num_h)],
                                                   name='nRB.zpset_xcool{0}'.format(nRB.index))
        self.zpset_cool = mdl.continuous_var_list([i for i in range(0, self.num_h)],
                                                  name='nRB.zpset_cool{0}'.format(nRB.index))
        """

        self.zpw_xheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="nRB.zpw_xheat{0}".format(nRB.index)
        )
        self.zpw_heat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="nRB.zpw_heat{0}".format(nRB.index)
        )
        self.zpw_xcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="nRB.zpw_xcool{0}".format(nRB.index)
        )
        self.zpw_cool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="nRB.zpw_cool{0}".format(nRB.index)
        )
        lamda0 = 0.25

        mdl.add_constraints(
            lamda0 * father.pset_cool[h] * father.zcool[h] <= father.tpcool[h]
            for h in range(num_h)
        )
        mdl.add_constraints(
            father.tpcool[h] <= father.nset * father.pset_cool[h] for h in range(num_h)
        )

        mdl.add_constraints(
            father.tpcool[h] <= father.zcool[h] * bigM for h in range(num_h)
        )

        mdl.add_constraints(
            lamda0 * father.pset_xcool[h] * father.zxcool[h] <= father.tpxcool[h]
            for h in range(num_h)
        )
        mdl.add_constraints(
            father.tpxcool[h] <= father.nset * father.pset_xcool[h]
            for h in range(num_h)
        )
        mdl.add_constraints(
            father.tpxcool[h] <= father.zxcool[h] * bigM for h in range(num_h)
        )

        mdl.add_constraints(
            lamda0 * father.pset_heat[h] * father.zheat[h] <= father.tpheat[h]
            for h in range(num_h)
        )
        mdl.add_constraints(
            father.tpheat[h] <= father.nset * father.pset_heat[h] for h in range(num_h)
        )
        mdl.add_constraints(
            father.tpheat[h] <= father.zheat[h] * bigM for h in range(num_h)
        )

        mdl.add_constraints(
            lamda0 * father.pset_xheat[h] * father.zxheat[h] <= father.tpxheat[h]
            for h in range(num_h)
        )
        mdl.add_constraints(
            father.tpxheat[h] <= father.nset * father.pset_xheat[h]
            for h in range(num_h)
        )
        mdl.add_constraints(
            father.tpxheat[h] <= father.zxheat[h] * bigM for h in range(num_h)
        )

        self.average_load_rate = father.average_load_rate
        mdl.add_constraints(
            father.tpwcool[h]
            == father.tpcool[h]
            / (self.average_load_rate * father.pset_cool[h])
            * father.pw_rated_cool
            * set_cool_fit.get_pwk_rate(self.average_load_rate)
            * set_cool_fit.get_pwk_without_rate(father.Tcool_out, father.Tin[h])
            for h in range(num_h)
        )

        mdl.add_constraints(
            father.tpwxcool[h]
            == father.tpxcool[h]
            / (self.average_load_rate * father.pset_xcool[h])
            * father.pw_rated_heat
            * set_cool_fit.get_pwk_rate(self.average_load_rate)
            * set_heat_fit.get_pwk_without_rate(father.Txcool_out, father.Tin[h])
            for h in range(num_h)
        )

        mdl.add_constraints(
            father.tpwheat[h]
            == father.tpheat[h]
            / (self.average_load_rate * father.pset_heat[h])
            * father.pw_rated_heat
            * set_heat_fit.get_pwk_rate(self.average_load_rate)
            * set_heat_fit.get_pwk_without_rate(father.Theat_out, father.Tin[h])
            for h in range(num_h)
        )

        mdl.add_constraints(
            father.tpwxheat[h]
            == father.tpxheat[h]
            / (self.average_load_rate * father.pset_xheat[h])
            * father.pw_rated_heat
            * set_heat_fit.get_pwk_rate(self.average_load_rate)
            * set_heat_fit.get_pwk_without_rate(father.Txheat_out, father.Tin[h])
            for h in range(num_h)
        )

        """



        mdl.add_constraints(
            father.tpwcool[h] == father.tpcool[h] / (
                    self.average_load_rate * father.pset_cool[h]) * father.pw_rated_cool * (
                    bcool[0] + bcool[1] * self.average_load_rate + bcool[
                2] * self.average_load_rate * self.average_load_rate
                    + bcool[3] * father.Tcool_out + bcool[4] * father.Tin[h] +
                    bcool[5] * father.Tin[h] * father.Tcool_out + bcool[
                        6] * father.Tcool_out * self.average_load_rate +
                    bcool[7] * father.Tin[h] * self.average_load_rate) for h in
            range(num_h))

        mdl.add_constraints(
            father.tpwxcool[h] == father.tpxcool[h] / (
                    self.average_load_rate * father.pset_xcool[h]) * father.pw_rated_cool * (
                    bcool[0] + bcool[1] * self.average_load_rate + bcool[
                2] * self.average_load_rate * self.average_load_rate + bcool[3] * father.Txcool_out + bcool[4] *
                    father.Tin[h] + bcool[5] * father.Tin[h] * father.Txcool_out +
                    bcool[6] * father.Txcool_out * self.average_load_rate +
                    bcool[7] * father.Tin[h] * self.average_load_rate) for h in
            range(num_h))

        mdl.add_constraints(
            father.tpwheat[h] == father.tpheat[h] / (
                    self.average_load_rate * father.pset_heat[h]) * father.pw_rated_heat * (
                    bheat[0] + bheat[1] * self.average_load_rate + bheat[
                2] * self.average_load_rate * self.average_load_rate + bheat[3] * father.Theat_out + bheat[4] *
                    father.Tin[h] +
                    bheat[5] * father.Tin[h] * father.Theat_out + bheat[
                        6] * father.Theat_out * self.average_load_rate +
                    bheat[7] * father.Tin[h] * self.average_load_rate)
            for h in range(num_h))

        mdl.add_constraints(
            father.tpwxheat[h] == father.tpxheat[h] / (self.average_load_rate * father.pset_xheat[h]) *
            father.pw_rated_heat * (bheat[0] + bheat[1] * self.average_load_rate + bheat[
                2] * self.average_load_rate * self.average_load_rate

                                    + bheat[3] * father.Txheat_out + bheat[4] * father.Tin[h] +
                                    bheat[5] * father.Tin[h] * father.Txheat_out + bheat[
                                        6] * father.Txheat_out * self.average_load_rate +
                                    bheat[7] * father.Tin[h] * self.average_load_rate)
            for h in range(num_h))
            """

        mdl.add_constraints(
            father.tpw[h]
            == father.tpwcool[h]
            + father.tpwxcool[h]
            + father.tpwheat[h]
            + father.tpwxheat[h]
            for h in range(num_h)
        )
