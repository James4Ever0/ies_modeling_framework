import piecewise_regression

import numpy as np

x_start, x_end, sample_size =0, 5000, 100
# x_start, x_end, sample_size = -500,500 , 100
x = np.linspace(x_start, x_end, sample_size)
# y = x**2
y = np.sin(x)

nb =12
# nb =5

# this is even.
# slow? before compilation
# sometimes the algo does not converge. dangerous.
pw_fit = piecewise_regression.Fit(x, y, n_breakpoints=nb)
# pw_fit.summary()

import matplotlib.pyplot as plt

# Plot the data, fit, breakpoints and confidence intervals
pw_fit.plot_data(color="grey", s=20)
# Pass in standard matplotlib keywords to control any of the plots
pw_fit.plot_fit(color="red", linewidth=4)
pw_fit.plot_breakpoints()
pw_fit.plot_breakpoint_confidence_intervals()
plt.xlabel("x")
plt.ylabel("y")
plt.show()
# plt.close()