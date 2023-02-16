# -*- coding: utf-8 -*-
"""
基于统一能路的6节点供热网络稳态潮流计算程序 (Open source)
confirmed
"""

# def method(a:int, b:int) -> int:
#     return a+b

# method("1","2")

# def method2(a,b,c):
#     d = a+b+c
#     d+=20
#     d/=a
#     return d

# a,b,c = 1,2,3
# # d = a+b+c
# # d+=20
# # d/=a
# d = method2(a,b,c)
# print(d)

# a,b,c = 4,5,6
# # d = a+b+c
# # d+=20
# # d/=a
# d = method2(a,b,c)
# print(d)

__author__ = "Chen Binbin"

import time
import numpy as np
import pandas as pd
from cmath import phase
from scipy.fftpack import fft
from matplotlib import pyplot as plt
from contextlib import contextmanager


# benchmark
@contextmanager  # 用于将函数转化为上下文管理器
def context(event: str):  # 用于计算某个事件的开始、结束时间以及运行时间，并将其打印出来
    t0: float = time.time()
    print(
        "[{}] {} starts ...".format(time.strftime("%Y-%m-%d %H:%M:%S"), event)
    )  # 事件开始时间
    yield  # yield语句之前的代码在with语句执行之前运行，yield语句后的代码在with语句执行结束后运行
    print(
        "[{}] {} ends ...".format(time.strftime("%Y-%m-%d %H:%M:%S"), event)
    )  # 事件结束时间
    print(
        "[{}] {} runs for {:.2f} s".format(
            time.strftime("%Y-%m-%d %H:%M:%S"), event, time.time() - t0
        )
    )  # 事件运行时间


with context("数据读取与处理"):
    tb1 = pd.read_excel("./6节点热网动态data.xls", sheet_name="Node").fillna(0)
    tb2 = pd.read_excel("./6节点热网动态data.xls", sheet_name="Branch")
    tb3 = pd.read_excel(
        "./6节点热网动态data.xls", sheet_name="Device", header=None, index_col=0
    )
    tb4 = pd.read_excel(
        "./6节点热网动态data.xls", sheet_name="Dynamic"
    )  # what are these sheets?
    # 水力参数
    L = tb2["length"].values * 1e3  # 管道长度
    D = tb2["diameter"].values  # 管道直径
    lam = tb2["fraction"].values  # 流量分数
    npipes, nnodes = len(tb2), len(tb1)  # 管道数、节点数
    As = np.array([np.pi * d**2 / 4 for d in D])  # 管道截面积
    mb = np.ones(npipes) * 50  # 基值平启动 #初始质量流量
    rho = 1000  # 流体密度
    Ah = np.zeros([nnodes, npipes], dtype=np.int32)  # 节点-管道关联矩阵
    for i, row in tb2.iterrows():
        Ah[row["from node"] - 1, i] = 1
        Ah[row["to node"] - 1, i] = -1
    fix_p = np.where(tb1.type1.values == "定压力")[0]  # 定压力节点索引
    fix_G = np.where(tb1.type1.values == "定注入")[0]  # 定注入节点索引
    # 热力参数
    c = 4200
    miu = tb2.disspation.values  # tb2中的disspation赋值给miu


with context("稳态水力计算"):
    err = []  # 失配误差记录
    mbs = [mb.copy()]  # 流量基值的迭代过程记录
    for itera in range(100):  # 最大迭代次数
        # 更新支路参数
        R = [lam[i] * mb[i] / rho / As[i] ** 2 / D[i] * L[i] for i in range(npipes)]
        E = [
            -lam[i] * mb[i] ** 2 / 2 / rho / As[i] ** 2 / D[i] * L[i]
            for i in range(npipes)
        ]
        # R 是各支路的导纳（reciprocal impedance），它是支路的电导 G（conductance）的倒数，因此有 R = 1/G。在这里，导纳是通过每根管道的基准流量 mb[i]，以及管道的长度 L[i]、横截面积 As[i]、摩擦阻力系数 D[i] 和流体密度 rho 来计算的。
        # E 是各支路的电位能，它是流体在支路中的动能和重力势能的和，通常用 J（焦耳）表示。在这里，电位能是通过每根管道的基准流量 mb[i]，以及管道的长度 L[i]、横截面积 As[i]、摩擦阻力系数 D[i] 和流体密度 rho 来计算的。
        # 追加各支路阀、泵的参数
        for i, row in tb2.iterrows():
            if row.pump > 0:
                kp1, kp2, kp3, w = tb3.loc["pump-%d" % int(row.pump), :]
                R[i] += -(2 * kp1 * mb[i] + kp2 * w)
                E[i] += kp1 * mb[i] ** 2 - kp3 * w**2
            # 对于带有泵的管路，需要考虑泵的影响，其中 kp1、kp2、kp3 分别表示泵的一次、二次和三次效率，w表示泵的转速，因此可根据公式计算泵的影响并加入到相应的管路中。
            if row.valve > 0:
                kv, _, _, _ = tb3.loc["valve-%d" % int(row.valve), :]
                R[i] += 2 * kv * mb[i] ** 2
                E[i] -= -kv * mb[i] ** 2
        # 对于带有阀门的管路，需要考虑阀门的影响，其中 kv 表示阀门的流量系数，因此可根据公式计算阀门的影响并加入到相应的管路中。
        E = np.array(E).reshape([-1, 1])  # E被重塑为[-1,1]的列向量
        yb = np.diag([1 / Ri for Ri in R])  # 用对角线上R值的倒数创建一个对角矩阵yb
        Y = np.matmul(
            np.matmul(Ah, yb), Ah.T
        )  # 导纳矩阵Y的计算公式为np.matmul( np.matmul ( Ah , yb)，Ah.T )，其中Ah为液压网络的关联矩阵。
        # 通过索引提取Y的子矩阵，生成Ygg、Ygp、Ypg和Ypp
        Ygg = Y[fix_G][:, fix_G]
        Ygp = Y[fix_G][:, fix_p]
        Ypg = Y[fix_p][:, fix_G]
        Ypp = Y[fix_p][:, fix_p]
        pp = (
            tb1["pressure(MPa)"].values[fix_p].reshape([1, 1]) * 1e6
        )  # 从tb1中提取与固定压力管道相连的节点处的压力，并将其整形为1x1阵列，单位为Pa
        G = tb1["injection(kg/s)"].values.reshape([-1, 1]) + np.matmul(
            np.matmul(Ah, yb), E
        )  # 从tb1中提取所有节点处的注入，并将其整形为以kg/s为单位的列向量。通过导纳矩阵Y和能量损失向量E相乘，再加上注入向量，计算出通过每根管道的液压流量。
        Gg = G[fix_G, :]  # 从G中提取具有固定压力的节点的液压流量，创建Gg。
        assert np.linalg.cond(Ygg) < 1e5  # 确认导纳矩阵非奇异
        pg = np.matmul(np.linalg.inv(Ygg), (Gg - np.matmul(Ygp, pp)))
        pn = np.concatenate((pp, pg), axis=0)
        Gb = np.matmul(yb, (np.matmul(Ah.T, pn) - E))
        err.append(np.linalg.norm(Gb.reshape(-1) - mb))
        mb = mb * 0.2 + Gb.reshape(-1) * 0.8
        mbs.append(mb.copy())
        # print('第%d次迭代，失配误差为%.5f'%(itera+1, err[-1]))
        if err[-1] < 1e-3:
            print("水力稳态潮流计算迭代%d次后收敛。" % (itera + 1))
            break


with context("时域激励分解"):
    # 时域激励
    # 10s一个点，共（x+12）*360个点，x为历史边界小时数
    # 构造时域激励TD_Tin和TD_E：根据历史边界数据，生成节点温度和管道温差的时域激励，其中每个点为10s一个，共有(x+12)*360个点，x为历史边界小时数。
    x = 12
    TD_Tin = np.zeros([nnodes, (x + 12) * 360])
    for i, supply in enumerate(tb1["T(Celsius)"].values):
        if isinstance(supply, str):
            TD_Tin[i, :] = np.concatenate(
                (
                    np.ones(360 * 9) * tb4[supply].values[0],
                    np.interp(
                        np.linspace(10, 3600 * 15, 360 * 15),
                        np.linspace(300, 3600 * 15, 12 * 15),
                        tb4[supply].values,
                    ),
                )
            )
    TD_E = np.zeros([npipes, (x + 12) * 360])
    for i, load in enumerate(tb2.deltaT.values):
        if isinstance(load, str):
            TD_E[i, :] = np.concatenate(
                (
                    np.ones(360 * 9) * tb4[load].values[0],
                    np.interp(
                        np.linspace(10, 3600 * 15, 360 * 15),
                        np.linspace(300, 3600 * 15, 12 * 15),
                        tb4[load].values,
                    ),
                )
            )
    # 转换为频域激励
    # 将时域激励转换为频域激励FD_Tin和FD_E：使用FFT将时域激励转换为频域激励，取前nf个频率分量，其中nf=100*3表示取前300个频率分量，nt为时域激励的总点数。转换后的频域激励FD_Tin和FD_E为复数，分别包含节点温度和管道温差的频域激励。
    nf = 100 * 3  # 频率分量
    nt = TD_E.shape[1]
    fr = 1 / (12 + x) / 3600
    FD_Tin = np.zeros([nnodes, nf], dtype="complex_")
    FD_E = np.zeros([npipes, nf], dtype="complex_")
    for i in range(nnodes):
        FD_Tin[i, :] = (fft(TD_Tin[i, :]) / nt * 2)[:nf]
        FD_Tin[i, 0] /= 2
    for i in range(npipes):
        FD_E[i, :] = (fft(TD_E[i, :]) / nt * 2)[:nf]
        FD_E[i, 0] /= 2


with context("动态热力计算"):
    m = list(Gb.reshape(-1))  # 各支路流量，由稳态水路计算获得
    A = Ah  # 水力、热力共享一个节点支路关联矩阵
    # 将其中的元素大于0的位置置为1，小于0的位置置为0
    Af = np.zeros(A.shape)
    Af[A > 0] = 1
    At_ = np.zeros(A.shape)
    At_[A < 0] = 1
    # 根据各支路流量和支路关联矩阵计算出传递矩阵At_，其中At_[i,j]表示第i个节点到第j个节点的热量传递系数
    for i in range(A.shape[1]):
        for j in range(A.shape[0]):
            At_[j, i] *= m[i]
    # 对传递矩阵At_进行归一化，使每个节点的所有出口热量传递系数之和为1
    for i in range(A.shape[0]):
        if sum(At_[i, :]) == 0:
            continue
        At_[i, :] /= sum(At_[i, :])

    # 单频网络方程求解
    # 这段代码是动态热力计算的主体，根据时域激励分解得到的频域激励，求解管路动态温度响应，最后将频域结果回归到时域。
    # 其中，首先根据管路的水力、热力参数计算出稳态时的水流流量、水温，作为时域激励分解得到的频域激励的参考，然后根据管路的热力参数和流量，得到频域下的温度响应，再将其回归到时域，即得到管路在不同时间段内的温度分布情况。
    ts = np.linspace(10, (12 + x) * 3600, nt)
    TD_Tt = np.zeros([npipes, nt])
    TD_Tf = np.zeros([npipes, nt])
    Rh = np.array([miu[j] / c**2 / m[j] ** 2 for j in range(A.shape[1])])
    Lh = np.array([rho * As[j] / c / m[j] ** 2 for j in range(A.shape[1])])
    for fi in range(nf):
        f = fi * fr
        w = 2 * np.pi * f
        Z = Rh + complex(0, 1) * w * Lh
        K = np.diag([np.exp(-c * m[j] * Z[j] * L[j]) for j in range(A.shape[1])])
        assert (
            np.linalg.cond(np.eye(A.shape[1]) - np.matmul(np.matmul(K, Af.T), At_))
            < 1e5
        )
        _m_ = np.linalg.inv(np.eye(A.shape[1]) - np.matmul(np.matmul(K, Af.T), At_))
        Tt = np.matmul(
            _m_,
            np.matmul(np.matmul(K, Af.T), FD_Tin[:, fi].reshape([-1, 1]))
            + FD_E[:, fi].reshape([-1, 1]),
        )
        Tf = np.matmul(np.linalg.inv(K), Tt - FD_E[:, fi].reshape([-1, 1]))
        # 频域回时域
        for j in range(npipes):
            TD_Tt[j, :] += abs(Tt[j, 0]) * np.cos(w * ts + phase(Tt[j, 0]))
            TD_Tf[j, :] += abs(Tf[j, 0]) * np.cos(w * ts + phase(Tf[j, 0]))
    #ts: 时间序列数组，单位为秒，表示模拟的时间范围。
#TD_Tt: 二维数组，大小为 (npipes, nt)，表示时域下的温度变化。
TD_Tf: 二维数组，大小为 (npipes, nt)，表示时域下的水力变化。
Rh: 一维数组，大小为 A.shape[1]，表示各支路的水力阻抗。
Lh: 一维数组，大小为 A.shape[1]，表示各支路的热力阻抗。
nf: 整数，表示频域离散点数。
fr: 实数，表示频域上的频率间隔。
f: 实数，表示当前的频率。
w: 实数，表示当前的角频率。
Z: 一维复数数组，大小为 A.shape[1]，表示各支路的复阻抗。
K: 对角矩阵，大小为 A.shape[1] x A.shape[1]，表示各支路上的热力传递因子。
_m_: 逆矩阵，大小为 A.shape[1] x A.shape[1]，表示模型中的系数矩阵的逆。
Tt: 二维数组，大小为 (A.shape[1], 1)，表示各支路上的温度变化。
Tf: 二维数组，大小为 (A.shape[1], 1)，表示各支路上的水力变化。


with context("可视化"):
    vis = 1
    # if vis:
    plt.figure(1)
    plt.plot(TD_Tf.T)
    plt.figure(2)
    plt.plot(TD_Tt.T)
    # sel = [0, 2, 7, 5]  # 仅查看部分管道
    # plt.figure(3)
    # plt.plot(TD_Tt[sel, :].T)
    plt.show()
