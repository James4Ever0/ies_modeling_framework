import numpy as np

x_lb, x_ub = 0,3
y_lb, y_ub = 0, 2*np.pi

x_sample_size = y_sample_size = 100

z_func = lambda x,y:x*np.sin(y)