import math
# 差分仿真单摆 带初始条件和时变控制条件

import numpy as np
θ_0=0.01
ω_0=0.0
l = 1.0                             # length [m]
m = 1.0                             # mass [kg]
g = 9.81                            # gravitational acceleration [m/s²]
u_0=np.array([θ_0, ω_0])
tspan = ([0.0,10.0])                  # time interval