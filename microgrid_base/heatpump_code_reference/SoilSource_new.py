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


class SoilSource(IGES):
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
        set_name="SoilSource",
    ):
        self.num_h = num_h
        IGES(set_name)
        SoilSource.index += 1
        num_period = round(self.num_h / 120)
        self.mdl = mdl
        self.set_price = set_price
        self.heat_max = heat_max
        self.heat_min = heat_min
        self.cool_max = cool_max
        self.cool_min = cool_min

        # self.dd = mdl.continuous_var(name='dd{0}'.format(SoilSource.index), lb=-1e3)

        self.T = np.zeros(self.num_h)
        self.q = np.zeros(self.num_h)
        self.qln_sumf = np.zeros(self.num_h)
        self.qln_sumb = np.zeros(self.num_h)
        self.Tfav = np.zeros(self.num_h)
        self.Tfav_1 = np.zeros(self.num_h)
        self.Tfav_2 = np.zeros(self.num_h)

        self.qav = np.zeros(self.num_h)

        self.pcool_out = self.mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="SoilSource.pcool_out{0}".format(SoilSource.index),
            lb=-1e3,
        )
        self.pheat_out = self.mdl.continuous_var_list(
            [i for i in range(0, self.num_h)],
            name="SoilSource.tpheat{0}".format(SoilSource.index),
            lb=-1e3,
        )
        self.nianhua = self.mdl.continuous_var(
            name="SoilSource_nianhua{0}".format(SoilSource.index)
        )
        self.length = self.mdl.continuous_var(
            name="SoilSourcelength{0}".format(SoilSource.index)
        )
        self.nset = self.mdl.continuous_var(
            name="SoilSource.nset{0}".format(SoilSource.index)
        )
        self.zcool = self.mdl.integer_var_list(
            [i for i in range(self.num_h)],
            name="SoilSource.zcool{0}".format(SoilSource.index),
        )
        self.zheat = self.mdl.integer_var_list(
            [i for i in range(self.num_h)],
            name="SoilSource.zheat{0}".format(SoilSource.index),
        )
        self.Tff = 16
        self.lamdas = 1.72
        self.k = 1 / (4 * 3.1415926 * self.lamdas)
        # 单U
        self.pi = 3.1415926

        self.db = 0.2
        self.do = 0.032
        # 钻孔回填材料的导热系数
        self.lamdab = 2
        #
        self.lamdap = 0.42
        self.di = 0.026
        self.D = 0.0064
        self.lh = 3000

        self.Rb = 0.5 * (
            1
            / (2 * self.pi * self.lamdab)
            * (
                np.log(self.db / self.do)
                + np.log(self.db / self.D)
                + (self.lamdab - self.lamdas)
                / (self.lamdab + self.lamdas)
                * np.log(
                    math.pow(self.db, 4) / (math.pow(self.db, 4) - math.pow(self.D, 4))
                )
            )
            + 1 / (2 * self.pi * self.lamdap) * np.log(self.do / self.di)
            + 1 / (self.pi * self.di * self.lh)
        )

    def cons_register(self, mdl, loop_flag):
        ####simple

        bigM = 1e8
        mdl.add_constraint(self.nset >= 0)
        mdl.add_constraint(self.nset <= 1000)
        mdl.add_constraint(self.nset * 4 <= self.heat_max)
        mdl.add_constraint(self.nset * 4 >= self.heat_min)
        mdl.add_constraint(self.nset * 6 <= self.cool_max)
        mdl.add_constraint(self.nset * 6 >= self.cool_min)
        if loop_flag == 1:
            pcool_sum = mdl.sum(self.pcool_out)
            pheat_sum = mdl.sum(self.pheat_out)

            mdl.add_constraint(pcool_sum <= pheat_sum * 1.25)
            mdl.add_constraint(pcool_sum >= pheat_sum * 0.8)

        mdl.add_constraints(
            self.pcool_out[h] <= 4 * self.nset for h in range(self.num_h)
        )
        mdl.add_constraints(self.pcool_out[h] >= 0 for h in range(self.num_h))
        mdl.add_constraints(
            self.pheat_out[h] <= 4 * self.nset for h in range(self.num_h)
        )
        mdl.add_constraints(self.pheat_out[h] >= 0 for h in range(self.num_h))
        mdl.add_constraints(
            self.pheat_out[h] <= self.zheat[h] * bigM for h in range(self.num_h)
        )
        mdl.add_constraints(
            self.pcool_out[h] <= self.zcool[h] * bigM for h in range(self.num_h)
        )
        mdl.add_constraints(
            self.zcool[h] + self.zheat[h] <= 1 for h in range(self.num_h)
        )

        mdl.add_constraint(self.nianhua == self.length * self.set_price / 30)
        mdl.add_constraint(self.length == self.nset * 120)

    def Do_simulation(self, sol_run, periodh, consideer_history):
        # q 正值为对外制冷。负值为对外值热。
        rrp = []
        length = sol_run.get_value(self.length)
        pcool_out = sol_run.get_values(self.pcool_out)
        pheat_out = sol_run.get_values(self.pheat_out)

        self.q = [
            1000 * (pcool_out[index] - pheat_out[index]) / length
            for index in range(self.num_h)
        ]
        print("do simulation")

        num_period = round(8760 / periodh)
        for period in range(num_period):
            self.qav[period] = (
                sum(self.q[period * periodh : (period + 1) * periodh]) / periodh
            )

            # self.Tfav[period] = mdl.sum(self.T[(period) * 120:(period+1) * 120]) / 120

        self.Tfav.resize((num_period, 1))
        self.Tfav_1.resize((num_period, 1))
        self.Tfav_2.resize((num_period, 1))

        for period in range(num_period):
            print(period)
            self.qln_sumf[period] = sum(
                self.qav[period + 1 - nindex] * np.log((nindex + 1) / (nindex))
                for nindex in range(1, period + 1)
            )

            self.qln_sumb[period] = sum(
                self.qav[period + 1 - nindex + num_period - 1]
                * np.log((nindex + 1) / (nindex))
                for nindex in range(period + 1, num_period)
            )
            if consideer_history == 1:
                self.Tfav[period] = (
                    self.k * (self.qln_sumf[period] + self.qln_sumb[period])
                    + self.qav[period] * self.Rb
                    + self.Tff
                )
                self.Tfav_1[period] = self.k * (
                    self.qln_sumf[period] + +self.qln_sumb[period]
                )
            else:
                self.Tfav[period] = (
                    self.k * (self.qln_sumf[period])
                    + self.qav[period] * self.Rb
                    + self.Tff
                )
                self.Tfav_1[period] = self.k * (self.qln_sumf[period])

            self.Tfav_2[period] = self.qav[period] * self.Rb

        for h in range(self.num_h):
            self.T[h] = self.Tfav[math.floor(h / periodh)]
        # 保存
        # Tfav文件
