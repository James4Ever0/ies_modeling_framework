import numpy as np
import matplotlib.pyplot as plt

l = 1.0                             # length [m]
m = 1.0                             # mass [kg]
g = 9.81                            # gravitational acceleration [m/s²]
θ0 = 0.01                          # initial angular deflection [rad]
ω0 = 0.0                            # initial angular velocity [rad/s]
t_span = (0.0, 10.0)                # time interval
dt = 0.01                           # time step
M = lambda t: 0.1*np.sin(t)         # external torque [Nm], function

# initialize arrays to store results
n = int((t_span[1] - t_span[0])/dt) + 1
θ = np.zeros(n)
ω = np.zeros(n)
t = np.linspace(t_span[0], t_span[1], n)

# set initial values
θ[0] = θ0
ω[0] = ω0

# iterate over time steps and update values using finite difference method
for i in range(1, n):
    θ[i] = θ[i-1] + dt*ω[i-1]
    ω[i] = ω[i-1] - 3*g/(2*l)*np.sin(θ[i-1])*dt + 3/(m*l**2)*M(t[i-1])*dt

# plot results
plt.plot(t, θ, label='θ [rad]')
plt.plot(t, ω, label='ω [rad/s]')
plt.xlabel('t')
plt.legend()
plt.show()