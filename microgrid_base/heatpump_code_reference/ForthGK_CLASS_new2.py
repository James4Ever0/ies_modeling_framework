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
from IGES_Math import RRproduct
from IGES_Math import RRSqure

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

#############################3

load_rate_cop_cool = [[0.25, 3], [0.5, 5], [0.75, 8], [1, 6]]
load_rate_cop_heat = [[0.25, 3], [0.5, 5], [0.75, 8], [1, 6]]
load_rate_arr_cool = np.zeros([4, 2], dtype=float)
load_rate_arr_heat = np.zeros([4, 2], dtype=float)
# normalized cop 是每个负载率的cop除以负载率为1时的cop
for i in range(4):
    load_rate_arr_cool[i][1] = (
        load_rate_cop_cool[i][1] / load_rate_cop_cool[3][1]
    )  # normalized cop
    load_rate_arr_cool[i][0] = load_rate_cop_cool[i][0]

    load_rate_arr_heat[i][1] = load_rate_cop_heat[i][1] / load_rate_cop_heat[3][1]
    load_rate_arr_heat[i][0] = load_rate_cop_heat[i][0]
###############################


set_cool_fit.fit_pwk_rate_coeff(load_rate_arr_cool)
set_heat_fit.fit_pwk_rate_coeff(load_rate_arr_heat)

bcool = set_cool_fit.get_pwk_rate_coeff()
"""
Parameters for f(1, load_rate, load_rate^2) = load_rate/normalized_cop
"""
bheat = set_heat_fit.get_pwk_rate_coeff()
"""
Parameters for f(1, load_rate, load_rate^2) = load_rate/normalized_cop
"""


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
        # 'w' is for electricity input
        self.pw_rated_cool = 30
        self.pw_rated_heat = 30
        # constant
        # output temperatures
        self.Tcool_out = 7
        self.Txcool_out = 5
        self.Theat_out = 7
        self.Txheat_out = 5

        # total power of output arrays

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

        self.tzcool = mdl.binary_var_list(
            [i for i in range(0, self.num_h)], name="tzcool{0}".format(ForthGK.index)
        )
        self.tzxcool = mdl.binary_var_list(
            [i for i in range(0, self.num_h)], name="tzxcool{0}".format(ForthGK.index)
        )
        self.tzheat = mdl.binary_var_list(
            [i for i in range(0, self.num_h)], name="tzheat{0}".format(singleRB.index)
        )
        self.tzxheat = mdl.binary_var_list(
            [i for i in range(0, self.num_h)], name="tzxheat{0}".format(singleRB.index)
        )
        self.nianhua = mdl.continuous_var(name="nianhua{0}".format(singleRB.index))
        self.ele_cost = mdl.continuous_var(name="ele_cost{0}".format(singleRB.index))

        self.pincool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="pincool{0}".format(ForthGK.index)
        )
        self.pinheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)], name="pinheat{0}".format(ForthGK.index)
        )
        # this shall be input, not 'builtin' static parameters.
        self.Tin = np.ones(num_h) * 12
        # mdl.continuous_var_list([i for i in range(0, self.num_h)],
        #                                  name='Tin{0}'.format(ForthGK.index))
        self.Nmax = round(self.heat_max / self.p_rated_heat)

        # if this is 1, then allow buying less subdevices, otherwise all subdevices shall be bought (deviceCount == maxDeviceCount)
        self.nsetopt = 1

        hrange = range(num_h)

        # constants
        # get heat/cooling power at given time, if running in corrsponding mode

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

    def cons_register(self, mdl: Model):  # taking eternal
        hrange = range(0, self.num_h)
        mdl.add_constraint(self.nset * self.p_rated_heat >= self.heat_min)
        mdl.add_constraint(self.nset * self.p_rated_cool >= self.cool_min)
        mdl.add_constraint(self.nset * self.p_rated_heat <= self.heat_max)
        mdl.add_constraint(self.nset * self.p_rated_cool <= self.cool_max)

        sigRB = self.build_submodels(mdl)
        if self.nsetopt == 1:
            # exclude nonexistent subdevices
            self.nset = mdl.sum([sigRB[n].exist for n in range(self.Nmax)])
        else:
            mdl.add_constraints(sigRB[n].exist == 1 for n in range(self.Nmax))

        for h in range(self.num_h):
            mdl.add_constraint(
                self.tpcool[h] == mdl.sum([sigRB[n].pcool[h] for n in range(self.Nmax)])
            )
            mdl.add_constraint(
                self.tpxcool[h]
                == mdl.sum([sigRB[n].pxcool[h] for n in range(self.Nmax)])
            )
            mdl.add_constraint(
                self.tpheat[h] == mdl.sum([sigRB[n].pheat[h] for n in range(self.Nmax)])
            )
            mdl.add_constraint(
                self.tpxheat[h]
                == mdl.sum([sigRB[n].pxheat[h] for n in range(self.Nmax)])
            )
            mdl.add_constraint(
                self.tpwcool[h]
                == mdl.sum([sigRB[n].zpw_cool[h] for n in range(self.Nmax)])
            )
            mdl.add_constraint(
                self.tpwxcool[h]
                == mdl.sum([sigRB[n].zpw_xcool[h] for n in range(self.Nmax)])
            )
            mdl.add_constraint(
                self.tpwheat[h]
                == mdl.sum([sigRB[n].zpw_heat[h] for n in range(self.Nmax)])
            )
            mdl.add_constraint(
                self.tpwxheat[h]
                == mdl.sum([sigRB[n].zpw_xheat[h] for n in range(self.Nmax)])
            )
            mdl.add_constraint(
                self.tpw[h] == mdl.sum([sigRB[n].pw[h] for n in range(self.Nmax)])
            )
            mdl.add_constraint(
                self.Nrun[h] == mdl.sum([sigRB[n].zrun[h] for n in range(self.Nmax)])
            )

        # 'z' is for states. these are mutually exclusive states.
        mdl.add_constraints(
            self.tzcool[h] + self.tzxcool[h] + self.tzheat[h] + self.tzxheat[h] <= 1
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
        # 15 is for device lifetime in years
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

    def build_submodels(self, mdl):
        sigRB = []  # submodels
        for n in range(self.Nmax):
            sigRB.append(
                singleRB(self.num_h, mdl, self, set_name="singleRB{0}".format(n))
            )

        return sigRB


bigM = 1e8


class singleRB(IGES):
    index = 0

    def __init__(
        self, num_h, mdl: Model, father: ForthGK, set_name="singleRB"
    ):  # also taking eternal
        IGES(set_name)
        singleRB.index += 1
        self.num_h = num_h
        self.exist = mdl.binary_var(name="singleRB-exist{0}".format(singleRB.index))
        self.zcool = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-zcool{0}".format(singleRB.index),
        )
        self.zxcool = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-zxcool{0}".format(singleRB.index),
        )
        self.zheat = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-zheat{0}".format(singleRB.index),
        )
        self.zxheat = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-zxheat{0}".format(singleRB.index),
        )
        self.zrun = mdl.binary_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-zrun{0}".format(singleRB.index),
        )
        self.pcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-pcool{0}".format(singleRB.index),
        )
        self.pxcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-pxcool{0}".format(singleRB.index),
        )
        self.pheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-pheat{0}".format(singleRB.index),
        )
        self.pxheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-pxheat{0}".format(singleRB.index),
        )

        self.pw_cool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-pw_cool{0}".format(singleRB.index),
        )
        self.pw_xcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-pw_xcool{0}".format(singleRB.index),
        )
        self.pw_heat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-pw_heat{0}".format(singleRB.index),
        )
        self.pw_xheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-pw_xheat{0}".format(singleRB.index),
        )
        self.pw = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-pw{0}".format(singleRB.index),
        )

        self.zpset_xheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-zpset_xheat{0}".format(singleRB.index),
        )
        self.zpset_heat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-zpset_heat{0}".format(singleRB.index),
        )
        self.zpset_xcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-zpset_xcool{0}".format(singleRB.index),
        )
        self.zpset_cool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-zpset_cool{0}".format(singleRB.index),
        )

        self.zpw_xheat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-zpw_xheat{0}".format(singleRB.index),
        )
        self.zpw_heat = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-zpw_heat{0}".format(singleRB.index),
        )
        self.zpw_xcool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-zpw_xcool{0}".format(singleRB.index),
        )
        self.zpw_cool = mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="singleRB-zpw_cool{0}".format(singleRB.index),
        )
        # this shall be the mininum heat/cooling power output of the entire device, relative to the rated output of a single subdevice
        # PWM-free subdevice models are in other files
        lamda0 = 0.25

        # (1)
        mdl.add_constraints(
            lamda0 * father.pset_cool[h] * self.zcool[h] <= self.pcool[h]
            for h in range(num_h)
        )
        mdl.add_constraints(
            self.pcool[h] <= father.pset_cool[h] * self.zcool[h] for h in range(num_h)
        )
        # subdevice cooling mode will never be turned on if not exists
        mdl.add_constraints(self.zcool[h] <= self.exist for h in range(num_h))
        # subdevice cooling mode will not be turned on if the device is not in the state
        mdl.add_constraints(self.zcool[h] <= father.tzcool[h] for h in range(num_h))

        # (2)
        mdl.add_constraints(
            lamda0 * father.pset_xcool[h] * self.zxcool[h] <= self.pxcool[h]
            for h in range(num_h)
        )
        mdl.add_constraints(
            self.pxcool[h] <= father.pset_xcool[h] * self.zxcool[h]
            for h in range(num_h)
        )
        mdl.add_constraints(self.zxcool[h] <= self.exist for h in range(num_h))
        mdl.add_constraints(self.zxcool[h] <= father.tzxcool[h] for h in range(num_h))

        # (3)

        mdl.add_constraints(
            lamda0 * father.pset_heat[h] * self.zheat[h] <= self.pheat[h]
            for h in range(num_h)
        )
        mdl.add_constraints(
            self.pheat[h] <= father.pset_heat[h] * self.zheat[h] for h in range(num_h)
        )
        mdl.add_constraints(self.zheat[h] <= self.exist for h in range(num_h))
        mdl.add_constraints(self.zheat[h] <= father.tzheat[h] for h in range(num_h))

        # (4)
        mdl.add_constraints(
            lamda0 * father.pset_xheat[h] * self.zxheat[h] <= self.pxheat[h]
            for h in range(num_h)
        )
        mdl.add_constraints(
            self.pxheat[h] <= father.pset_xheat[h] * self.zxheat[h]
            for h in range(num_h)
        )
        mdl.add_constraints(self.zxheat[h] <= self.exist for h in range(num_h))
        mdl.add_constraints(self.zxheat[h] <= father.tzxheat[h] for h in range(num_h))

        mdl.add_constraints(
            self.zrun[h]
            == self.zcool[h] + self.zxcool[h] + self.zheat[h] + self.zxheat[h]
            for h in range(num_h)
        )

        pcool_squre1 = []
        pxcool_squre1 = []
        pheat_squre1 = []
        pxheat_squre1 = []
        # these might slow things down
        # use pyomo piecewise!
        # be it like:
        # model.const = Piecewise(index_1,...,index_n,yvar,xvar,**Keywords)
        res = 5  # original: 11
        upper_bound = 2 # original: 5000
        for h in range(num_h):
            pcool_squre1.append(
                RRSqure(mdl, self.pcool[h] / father.pset_cool[h], upper_bound, res).getxx()
                # / father.pset_cool[h]
                # / father.pset_cool[h]
            )
            pxcool_squre1.append(
                RRSqure(mdl, self.pxcool[h] / father.pset_xcool[h], upper_bound, res).getxx()
                # / father.pset_xcool[h]
                # / father.pset_xcool[h]
            )
            pheat_squre1.append(
                RRSqure(mdl, self.pheat[h] / father.pset_heat[h], upper_bound, res).getxx()
                # / father.pset_heat[h]
                # / father.pset_heat[h]
            )
            pxheat_squre1.append(
                RRSqure(mdl, self.pxheat[h] / father.pset_xheat[h], upper_bound, res).getxx()
                # / father.pset_xheat[h]
                # / father.pset_xheat[h]
            )

        mdl.add_constraints(
            self.pw_cool[h]
            == father.pw_rated_cool
            * (
                bcool[0]
                + bcool[1] * self.pcool[h] / father.pset_cool[h]
                + bcool[2] * pcool_squre1[h]
            )
            * set_cool_fit.get_pwk_without_rate(father.Tcool_out, father.Tin[h])
            for h in range(num_h)
        )

        mdl.add_constraints(
            self.pw_xcool[h]
            == father.pw_rated_cool
            * (
                bcool[0]
                + bcool[1] * self.pxcool[h] / father.pset_xcool[h]
                + bcool[2] * pxcool_squre1[h]
            )
            * set_cool_fit.get_pwk_without_rate(father.Txcool_out, father.Tin[h])
            for h in range(num_h)
        )

        mdl.add_constraints(
            self.pw_heat[h]
            == father.pw_rated_heat
            * (
                bheat[0]
                + bheat[1] * self.pheat[h] / father.pset_heat[h]
                + bheat[2] * pheat_squre1[h]
            )
            * set_heat_fit.get_pwk_without_rate(father.Theat_out, father.Tin[h])
            for h in range(num_h)
        )
        # actual electricity input = rated electricity input * (load_rate / normalized_cop (electricity input load rate correlation coefficient)) * electricity input temperature correlation coefficient

        mdl.add_constraints(
            self.pw_xheat[h]
            == father.pw_rated_heat
            * (
                bheat[0]
                + bheat[1] * self.pxheat[h] / father.pset_xheat[h]
                + bheat[2] * pxheat_squre1[h]
            )
            * set_heat_fit.get_pwk_without_rate(father.Txheat_out, father.Tin[h])
            for h in range(num_h)
        )

        mdl.add_constraints(
            self.pw[h]
            == self.zpw_cool[h]
            + self.zpw_xcool[h]
            + self.zpw_heat[h]
            + self.zpw_xheat[h]
            for h in range(num_h)
        )

        mdl.add_constraints(self.zpw_cool[h] <= self.pw_cool[h] for h in range(num_h))
        mdl.add_constraints(
            self.zpw_cool[h] <= self.zcool[h] * bigM for h in range(num_h)
        )
        mdl.add_constraints(self.zpw_cool[h] >= 0 for h in range(num_h))
        mdl.add_constraints(
            self.zpw_cool[h] >= self.pw_cool[h] - (1 - self.zcool[h]) * bigM
            for h in range(num_h)
        )

        mdl.add_constraints(self.zpw_xcool[h] <= self.pw_xcool[h] for h in range(num_h))
        mdl.add_constraints(
            self.zpw_xcool[h] <= self.zxcool[h] * bigM for h in range(num_h)
        )
        mdl.add_constraints(self.zpw_xcool[h] >= 0 for h in range(num_h))
        mdl.add_constraints(
            self.zpw_xcool[h] >= self.pw_xcool[h] - (1 - self.zxcool[h]) * bigM
            for h in range(num_h)
        )

        mdl.add_constraints(self.zpw_heat[h] <= self.pw_heat[h] for h in range(num_h))
        mdl.add_constraints(
            self.zpw_heat[h] <= self.zheat[h] * bigM for h in range(num_h)
        )
        mdl.add_constraints(self.zpw_heat[h] >= 0 for h in range(num_h))
        mdl.add_constraints(
            self.zpw_heat[h] >= self.pw_heat[h] - (1 - self.zheat[h]) * bigM
            for h in range(num_h)
        )

        mdl.add_constraints(self.zpw_xheat[h] <= self.pw_xheat[h] for h in range(num_h))
        mdl.add_constraints(
            self.zpw_xheat[h] <= self.zxheat[h] * bigM for h in range(num_h)
        )
        mdl.add_constraints(self.zpw_xheat[h] >= 0 for h in range(num_h))
        mdl.add_constraints(
            self.zpw_xheat[h] >= self.pw_xheat[h] - (1 - self.zxheat[h]) * bigM
            for h in range(num_h)
        )
