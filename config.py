
"""
仿真共享参数
"""


# ma = 0  # not using? moving average?
import numpy as np
import time
localtime1 = time.time()

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
# total simulation rounds?
simulationTime = 3600
# a big number
bigNumber = 10e10
"""
设置一个大的数,默认值为10的10次方
"""


# every hour of one day?
intensityOfIllumination = np.ones(shape=num_hour0)

"""
24小时光照强度数组,数组形状为`(num_hour0,)`,所有元素初始化为1
"""
# what is this "ha"? just sunlight stats per hour in a day?

