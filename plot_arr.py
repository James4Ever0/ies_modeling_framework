# import docplex
# from docplex.mp.model import Model
# import pandas as pd
# import numpy as np

import matplotlib.pyplot as plt
from matplotlib import style
from result_processlib import Value


class IGESPlot(object):
    def __init__(self, sol):
        self.sol = sol

    # n 行向量
    def plot_list(self, arr, legend_title, title_content):
        value = Value(self.sol)
        if isinstance(arr, list):
            xlen = len(arr)
            if isinstance(arr[0], list):
                ylen = len(arr[0])
            else:
                ylen = 1
        else:
            xlen = 1
        print('xlen:',xlen,' ylen:',ylen)
        wide = 4
        # 全部为0的时候就不显示
        index = 1
        title2 = list()
        index = 0
        for row in range(0, xlen):
            arrtemp: list = value.value(arr[row])
            flag = 0
            for col in range(0, ylen):
                if arrtemp[col] >= 1 or arrtemp[col] <= -1:
                    flag = 1
            if flag == 0:
                # 全部为0
                np_ = 0
            else:
                #print(arrtemp)
                plt.plot(arrtemp)
                #print('index:', index, ' row:', row)
                title2.append(legend_title[row])

                print('row:',row)
                index = index + 1
        plt.xlabel('Time/h')
        plt.ylabel('Power/kW')
        # plt.set(gca, 'Fontsize', 20)
        plt.legend(title2)
        plt.title(title_content)
        plt.savefig('fig/'+title_content+'.png')

        