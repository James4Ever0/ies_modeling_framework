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


set_heat_fit = Set_Para_Fit(heat_para)
set_heat_fit.fit_pkcoeff()
set_heat_fit.fit_pwkcoeff_without_rate()


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
        self.Theat_out = 50
        self.Txheat_out = 55

        self.tpcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.tpcool{0}".format(ForthGK.index),
        )
        self.tpxcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.tpxcool{0}".format(ForthGK.index),
        )
        self.tpheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.tpheat{0}".format(ForthGK.index),
        )
        self.tpxheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.tpxheat{0}".format(ForthGK.index),
        )
        self.tpwcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.tpwcool{0}".format(ForthGK.index),
        )
        self.tpwxcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.tpwxcool{0}".format(ForthGK.index),
        )
        self.tpwheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.tpwheat{0}".format(ForthGK.index),
        )

        self.tpwxheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.tpwxheat{0}".format(ForthGK.index),
        )
        self.tpw = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.tpw{0}".format(ForthGK.index),
        )

        self.Nrun = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.tNrun{0}".format(ForthGK.index),
        )

        self.zcool = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.tzcool{0}".format(ForthGK.index),
        )
        self.zxcool = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.tzxcool{0}".format(ForthGK.index),
        )
        self.zheat = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.tzheat{0}".format(ForthGK.index),
        )
        self.zxheat = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.tzxheat{0}".format(ForthGK.index),
        )
        self.nianhua = mdl.continuous_var(
            name="ForthGK.nianhua{0}".format(ForthGK.index)
        )
        self.ele_cost = mdl.continuous_var(
            name="ForthGK.ele_cost{0}".format(ForthGK.index)
        )

        self.pincool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.pincool{0}".format(ForthGK.index),
        )
        self.pinheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="ForthGK.pinheat{0}".format(ForthGK.index),
        )
        self.Tin = np.ones(num_h) * 12
        # mdl.continuous_var_list([i for i in range(0, self.num_h)],
        #                                  name='Tin{0}'.format(ForthGK.index))
        self.Nmax = round(self.heat_max / self.p_rated_heat)
        self.nsetopt = 1

        hrange = range(self.num_h)
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

        rb = nRB(self.num_h, mdl, self, set_name="nRB")

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
        ###
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


class nRB(IGES):
    index = 0

    def __init__(self, num_h, mdl: Model, father, set_name="singleRB"):
        IGES(set_name)
        nRB.index += 1
        bigM = 1e8
        self.num_h = num_h

        # ub nset*pset_xx*zXX
        self.Nrun_cool = mdl.integer_var_list(
            [i for i in range(0, self.num_h)], name="nRB.Nrun_cool{0}".format(nRB.index)
        )

        self.Nrun_xcool = mdl.integer_var_list(
            [i for i in range(0, self.num_h)],
            name="nRB.Nrun_xcool{0}".format(nRB.index),
        )

        self.Nrun_heat = mdl.integer_var_list(
            [i for i in range(0, self.num_h)],
            name="nRB.Nrun_heatl{0}".format(nRB.index),
        )
        self.Nrun_xheat = mdl.integer_var_list(
            [i for i in range(0, self.num_h)],
            name="nRB.Nrun_xheat{0}".format(nRB.index),
        )

        mdl.add_constraints(
            father.tpcool[h] == self.Nrun_cool[h] * father.pset_cool[h]
            for h in range(num_h)
        )
        mdl.add_constraints(
            father.tpxcool[h] == self.Nrun_xcool[h] * father.pset_xcool[h]
            for h in range(num_h)
        )
        mdl.add_constraints(
            father.tpheat[h] == self.Nrun_heat[h] * father.pset_heat[h]
            for h in range(num_h)
        )
        mdl.add_constraints(
            father.tpxheat[h] == self.Nrun_xheat[h] * father.pset_xheat[h]
            for h in range(num_h)
        )

        mdl.add_constraints(
            father.Nrun[h]
            == self.Nrun_cool[h]
            + self.Nrun_xcool[h]
            + self.Nrun_heat[h]
            + self.Nrun_xheat[h]
            for h in range(num_h)
        )

        mdl.add_constraints(
            father.tpcool[h] <= father.zcool[h] * bigM for h in range(num_h)
        )
        mdl.add_constraints(
            father.tpxcool[h] <= father.zxcool[h] * bigM for h in range(num_h)
        )
        mdl.add_constraints(
            father.tpheat[h] <= father.zheat[h] * bigM for h in range(num_h)
        )
        mdl.add_constraints(
            father.tpxheat[h] <= father.zxheat[h] * bigM for h in range(num_h)
        )

        mdl.add_constraints(
            father.tpwcool[h]
            == self.Nrun_cool[h]
            * father.pw_rated_cool
            * set_cool_fit.get_pwk_without_rate(father.Tcool_out, father.Tin[h])
            for h in range(num_h)
        )

        mdl.add_constraints(
            father.tpwxcool[h]
            == self.Nrun_xcool[h]
            * father.pw_rated_cool
            * set_cool_fit.get_pwk_without_rate(father.Txcool_out, father.Tin[h])
            for h in range(num_h)
        )

        mdl.add_constraints(
            father.tpwheat[h]
            == self.Nrun_heat[h]
            * father.pw_rated_heat
            * set_heat_fit.get_pwk_without_rate(father.Theat_out, father.Tin[h])
            for h in range(num_h)
        )

        mdl.add_constraints(
            father.tpwxheat[h]
            == self.Nrun_xheat[h]
            * father.pw_rated_heat
            * set_heat_fit.get_pwk_without_rate(father.Txheat_out, father.Tin[h])
            for h in range(num_h)
        )

        """
        mdl.add_constraints(
            father.tpwcool[h] == self.Nrun_cool[h] * father.pw_rated_cool * (
            (bcool[0] + bcool[1] * father.Tcool_out + bcool[2] * father.Tcool_out * father.Tcool_out + bcool[
                3] * father.Tin[h]))
            for h in range(num_h))

        mdl.add_constraints(
            father.tpwxcool[h] == self.Nrun_xcool[h] * father.pw_rated_cool * (
                        bcool[0] + bcool[1] * father.Txcool_out + bcool[2] * father.Txcool_out * father.Txcool_out +
                        bcool[3] * father.Tin[h]) for h in range(num_h))

        mdl.add_constraints(
            father.tpwheat[h] == self.Nrun_heat[h] * father.pw_rated_heat * (
                        bheat[0] + bheat[1] * father.Theat_out + bheat[2] * father.Theat_out * father.Theat_out + bheat[
                    3] * father.Tin[h]) for h in range(num_h))

        mdl.add_constraints(
            father.tpwxheat[h] == self.Nrun_xheat[h] * father.pw_rated_heat * (
            (bheat[0] + bheat[1] * father.Txheat_out + bheat[2] * father.Txheat_out * father.Txheat_out +
             bheat[3] * father.Tin[h]))
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
