# recursive binsect method
# descent by: error area threshold or max section count
import pwlf
import numpy as np

x_start, x_end, sample_size = -500, 500, 100
# x_start, x_end, sample_size = 0, 5000, 100
x = np.linspace(x_start, x_end, sample_size)
# y = np.sin(x)
# y = np.sin(x) + np.random.normal(0, 0.2, 100)
y = x**2

# initialize piecewise linear fit with your x and y data
myPWLF = pwlf.PiecewiseLinFit(x, y)

# fit the function with four line segments
# force the function to go through the data points
# (0.0, 0.0) and (0.19, 0.16)
# where the data points are of the form (x, y)
# x_c = [0.0, 0.19]
# y_c = [0.0, 0.2]
# res = myPWLF.fitfast(20, pop=3)
res = myPWLF.fitfast(12, pop=3)
# res = myPWLF.fitfast(4, pop=3)

# this is slow. do not use
# res = myPWLF.fit(4, x_c, y_c)
# x_c = [x[0], x[-1]]
# y_c = [y[0], y[-1]]
# res = myPWLF.fit(12,x_c, y_c, atol=0.1)

# predict for the determined points
# xHat = np.linspace(min(x), 0.19, num=10000)
yHat = myPWLF.predict(x)

import matplotlib.pyplot as plt

# plot the results
plt.figure()
plt.plot(x, y, 'o')
plt.plot(x, yHat, '-', color='red')
plt.show()