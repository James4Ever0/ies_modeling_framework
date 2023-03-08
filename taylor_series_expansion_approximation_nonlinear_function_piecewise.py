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

pow_3_lb = y_3_lb = y_lb**3
pow_3_ub = y_3_ub = y_ub**3

pow_5_lb = y_5_lb = y_lb**5
pow_5_ub = y_5_ub = y_ub**5

i_0_lb = (x_lb + y_lb) / 2
i_0_ub = (x_ub + y_ub) / 2
i_1_lb = (x_lb - y_ub) / 2
i_1_ub = (x_ub - y_lb) / 2

i_2_lb = (x_lb + y_3_lb) / 2
i_2_ub = (x_ub + y_3_ub) / 2
i_3_lb = (x_lb - y_3_ub) / 2
i_3_ub = (x_ub - y_3_lb) / 2

i_4_lb = (x_lb + y_5_lb) / 2
i_4_ub = (x_ub + y_5_ub) / 2
i_5_lb = (x_lb - y_5_ub) / 2
i_5_ub = (x_ub - y_5_lb) / 2

pow_2_lb = min(i_0_lb, i_1_lb, i_2_lb, i_3_lb, i_4_lb, i_5_lb)
pow_2_ub = max(i_0_ub, i_1_ub, i_2_ub, i_3_ub, i_4_ub, i_5_ub)

import numpy as np
from scipy.interpolate import interp1d


# # 定义输入和输出数组
# x = np.array([0, 1, 2, 3, 4, 5])
# y = np.array([0, 1, 4, 9, 16, 25])
def interpolate_from_input_and_output_array(x, y):
    # 使用interp1d函数将输入和输出数组转化为分段函数
    f = interp1d(x, y, kind="linear")  # put np.ndarray here
    return f


# # 使用分段函数计算新的输出值
# x_new = np.array([1.5, 3.5])
# y_new = f(x_new)
# # 打印新的输出值
# print(y_new)


def get_piecewise_function(lb, ub, sample_size, func):
    print("LB:",lb, "UB:",ub)
    input_array = np.linspace(lb, ub, sample_size)
    output_array = func(input_array)
    piecewise_func = interpolate_from_input_and_output_array(input_array, output_array)
    return piecewise_func


piecewise_sample_size = 100000
piecewise_pow_2 = get_piecewise_function(
    pow_2_lb, pow_2_ub, piecewise_sample_size, lambda x: x**2
)
piecewise_pow_3 = get_piecewise_function(
    pow_3_lb, pow_3_ub, piecewise_sample_size, lambda x: x**3
)
piecewise_pow_5 = get_piecewise_function(
    pow_5_lb, pow_5_ub, piecewise_sample_size, lambda x: x**5
)

import math


def z_func_approx(x: float, y: float):
    assert x > x_lb
    assert x < x_ub
    assert y > y_lb
    assert y < y_ub

    y = np.array([y])
    x = np.array([x])

    y_3 = piecewise_pow_3(y)
    y_5 = piecewise_pow_5(y)
    # breakpoint()

    i_0 = (x + y) / 2
    i_1 = (x - y) / 2
    i_2 = (x + y_3) / 2
    i_3 = (x - y_3) / 2
    i_4 = (x + y_5) / 2
    i_5 = (x - y_5) / 2

    pow_2_i_0 = piecewise_pow_2(i_0)
    pow_2_i_1 = piecewise_pow_2(i_1)
    pow_2_i_2 = piecewise_pow_2(i_2)
    pow_2_i_3 = piecewise_pow_2(i_3)
    # print("I_4:",i_4)
    pow_2_i_4 = piecewise_pow_2(i_4)
    pow_2_i_5 = piecewise_pow_2(i_5)

    z_approx = (
        (pow_2_i_0 - pow_2_i_1)
        - (pow_2_i_2 - pow_2_i_3) / math.factorial(3)
        + (pow_2_i_4 - pow_2_i_5) / math.factorial(5)
    )

    return z_approx


print(z_func_approx(1, 2), np.sin(2))
