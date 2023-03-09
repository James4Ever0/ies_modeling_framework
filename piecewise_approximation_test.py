# z = x*sin(y)
# y_s ~= sin(y)
# i_0 = (x+y_s)/2, i_1 = (x-y_s)/2
# z = i_0^2-i_1^2
from linearization_config import *


y_s_lb = -1
y_s_ub = 1

i_0_lb = (x_lb + y_s_lb) / 2
i_0_ub = (x_ub + y_s_ub) / 2
i_1_lb = (x_lb - y_s_ub) / 2
i_1_ub = (x_ub - y_s_lb) / 2


import numpy as np
from scipy.interpolate import interp1d


# # 定义输入和输出数组
# x = np.array([0, 1, 2, 3, 4, 5])
# y = np.array([0, 1, 4, 9, 16, 25])
def interpolate_from_input_and_output_array(x, y):
    # 使用interp1d函数将输入和输出数组转化为分段函数
    f = interp1d(x, y, kind="linear")  # put np.ndarray here
    return f


def get_piecewise_function(lb, ub, sample_size, func):
    print("LB:", lb, "UB:", ub)
    input_array = np.linspace(lb, ub, sample_size)
    output_array = func(input_array)
    piecewise_func = interpolate_from_input_and_output_array(input_array, output_array)
    return piecewise_func


piecewise_sample_size = 1000
piecewise_y_sin = get_piecewise_function(
    y_lb, y_ub, piecewise_sample_size, lambda x: np.sin(x)
)
piecewise_pow_2_1 = get_piecewise_function(
    i_0_lb, i_0_ub, piecewise_sample_size, lambda x: x**2
)
piecewise_pow_2_2 = get_piecewise_function(
    i_1_lb, i_1_ub, piecewise_sample_size, lambda x: x**2
)

import math


def z_func_approx(x: float, y: float):
    assert x > x_lb
    assert x < x_ub
    assert y > y_lb
    assert y < y_ub

    y = np.array([y])
    x = np.array([x])

    y_s = piecewise_y_sin(y)

    i_0 = (x + y_s) / 2
    i_1 = (x - y_s) / 2

    pow_2_i_0 = piecewise_pow_2_1(i_0)
    pow_2_i_1 = piecewise_pow_2_2(i_1)

    z_approx = pow_2_i_0 - pow_2_i_1

    return z_approx


print(z_func_approx(0.5, 2), 0.5 * np.sin(2))
