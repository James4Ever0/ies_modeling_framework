文件内容:

|  文件名                                  |  文件内容                      |
|------------------------------------------|-------------------------------|
| integratedEnergySystemPrototypes.py      | 线性能源规划模型               |
| cloudpss_inputs.json                     |  IESLab输入参数               |
| cloudpss_ieslab_connectivity_matrix.xlsx | IESLab设备连接矩阵（不含蒸汽） |

问题:

1. 如何对有管道厚度$t$的水管管道的温度下降方程进行非线性建模？<br>无管道厚度的温度降方程为：$$e^{\frac{{\lambda}L}{c_{p}m}} = \frac{T_{start}-T_a}{T_{end}-T_a}$$
其中$\lambda$是管段单位长度总传热系数，$L$是管段长度，$m$是管段质量流率，$T_a$是环境空气温度，$T_{start}$和$T_{end}$是管段起点和终点的水温。
2. 如何对含有蒸汽的管道的温度下降方程和压力下降方程进行非线性建模？
3. 如何根据`cloudpss_inputs.json`文件内的参数和`cloudpss_ieslab_connectivity_matrix.xlsx`内的设备连接矩阵对每个设备和任意合理的设备间端口相连形成的拓扑结构利用`pyomo`进行Python建模以及根据目标函数（例如总成本最小）求最小值，不涉及微分方程，只有非线性和线性约束？
4. 如何将非线性模型转化为如同`integratedEnergySystemPrototypes.py`的线性模型？
5. 
附录:

