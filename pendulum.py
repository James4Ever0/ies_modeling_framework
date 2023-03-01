from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

l = 1.0                             # length [m]
m = 1.0                             # mass [kg]
g = 9.81                            # gravitational acceleration [m/s²]

def pendulum(t, u, M):
    θ, ω = u
    return [ω, -3*g/(2*l)*np.sin(θ) + 3/(m*l**2)*M(t)]

θ_0 = 0.01                          # initial angular deflection [rad]
ω_0 = 0.0                            # initial angular velocity [rad/s]
u_0 = [θ_0, ω_0]                       # initial state vector
t_span = (0.0, 10.0)                # time interval
M = lambda t: 0.1*np.sin(t)         # external torque [Nm], function

sol = solve_ivp(lambda t, y: pendulum(t, y, M), t_span, u_0, method='RK45')

angular_deflections = sol.y[0]
angular_velocities = sol.y[1]

plt.plot(sol.t, angular_deflections, label='θ [rad]')
plt.plot(sol.t, angular_velocities, label='ω [rad/s]')
plt.xlabel('t')
plt.legend()
plt.show()