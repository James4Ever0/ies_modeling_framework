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

pow_3_lb= y_3_lb = y_lb**3
pow_3_ub=y_3_ub = y_ub**3

pow_5_lb= y_5_lb = y_lb**5
pow_5_ub= y_5_ub = y_ub**5

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

pow_2_lb = min(i_0_lb, i_1_lb, i_2_lb, i_3_lb,i_4_lb, i_5_lb)
pow_2_ub = min(i_0_ub, i_1_ub, i_2_ub, i_3_ub,i_4_ub, i_5_ub)

import numpy as np
from scipy.interpolate import interp1d
# # 定义输入和输出数组
# x = np.array([0, 1, 2, 3, 4, 5])
# y = np.array([0, 1, 4, 9, 16, 25])
def interpolate_from_input_and_output_array(x,y):
# 使用interp1d函数将输入和输出数组转化为分段函数
    f = interp1d(x, y, kind='linear')
    return f
# # 使用分段函数计算新的输出值
# x_new = np.array([1.5, 3.5])
# y_new = f(x_new)
# # 打印新的输出值
# print(y_new)

piecewise_sample_size = 100
input_array = 
interp_pow_2 = interpolate_from_input_and_output_array(input_array, output_array)