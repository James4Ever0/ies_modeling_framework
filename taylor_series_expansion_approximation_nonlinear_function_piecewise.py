# z = x*sin(y)
# sin(y) ~= y-y^3/3!+y^5/5!
# y_3 = y^3
# y_5 = y^5
# z = x*y - x*y_3/3! + x*y_5/5!
# i_0 = (x+y)/2, i_1 = (x-y)/2
# i_2 = (x+y_3)/2, i_3 = (x-y_3)/2
# i_4 = (x+y_5)/2, i_5 = (x-y_5)/2
# z = i_0^2-i_1^2 - (i_2^2-i_3^2)/3!+(i_4^2-i_5^2)/5!

from linearization_config import *

y_3_lb = y_lb**3
y_3_ub = y_ub**3

y_5_lb = y_lb**5
y_5_ub = y_ub**5

i_0_lb = (x_lb+y_lb)/2
i_0_ub = (x_ub+y_ub)/2
i_1_lb = (x_lb-y_lb)/2
i_1_ub = (x_ub-y_ub)/2

i_2_lb = (x_lb+y_3_lb)/2
i_2_ub = (x_ub+y_3_ub)/2
i_3_lb = (x_lb-y_3_lb)/2
i_3_ub = (x_ub-y_3_ub)/2

i_4_lb = (x_lb+y_5_lb)/2
i_4_ub = (x_ub+y_5_ub)/2
i_5_lb = (x_lb-y_5_lb)/2
i_5_ub = (x_ub-y_5_ub)/2

import numpy as np
from scipy.interpolate import interp1d
# 定义输入和输出数组
x = np.array([0, 1, 2, 3, 4, 5])
y = np.array([0, 1, 4, 9, 16, 25])
# 使用interp1d函数将输入和输出数组转化为分段函数
f = interp1d(x, y, kind='linear')
# # 使用分段函数计算新的输出值
# x_new = np.array([1.5, 3.5])
# y_new = f(x_new)
# # 打印新的输出值
# print(y_new)