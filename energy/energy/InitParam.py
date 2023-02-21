from pathlib import Path

import numpy as np
from pandas import read_csv


class ResourceGet(object):

    def __init__(self,path,num_h):
        self.num_h = num_h
        self.path = path
        self.get_radiation()
        self.get_init_price()
        self.get_init_load()

    # 光照资源，超过一年的，将一年数据进行重复
    def get_radiation(self):
        if Path(self.path).exists():
            raw_file = read_csv(self.path,sep='\t',header=None)
            radiation = raw_file[0].values
            for _ in range(1, self.num_h//8760):
                radiation.extrend(radiation)
            self.ha = radiation/1000  # 转化为kW
        else:
            raise FileNotFoundError('File not extists.')

    def get_init_price(self):
        self.ele_price    = np.ones(self.num_h, dtype=float) * 0.5
        self.gas_price    = np.ones(self.num_h, dtype=float) * 2.77
        self.cityrs_price = np.ones(self.num_h, dtype=float) * 0.3
        self.citysteam    = np.ones(self.num_h, dtype=float) * 0.3

    def get_init_load(self):
        self.cool_load  = np.ones(self.num_h, dtype=float) * 10000
        self.heat_load  = np.ones(self.num_h, dtype=float) * 10000
        self.power_load = np.ones(self.num_h, dtype=float) * 10000
        self.steam_load = np.ones(self.num_h, dtype=float) * 10000
