import pyomo
import pyomo.core.kernel.piecewise_library.util
from linearization_config import *

# func: z = x*sin(y)

from pyomo.core.kernel.variable import variable

x = variable(lb=x_lb, ub=x_ub)
y = variable(lb=y_lb, ub=y_ub)

delaunay = pyomo.core.kernel.piecewise_library.util.generate_delaunay(
    [x, y], num=x_sample_size
)

# print(delaunay) # what is it?
# breakpoint()
xy_points = delaunay.points  # (10000,2)

z_vals = z_func(xy_points[:, 0], xy_points[:, 1])

from pyomo.core.kernel.piecewise_library.transforms_nd import piecewise_nd

piecewise_z_func = piecewise_nd(delaunay, z_vals)

# breakpoint()
# can it be used in actual optimization?
print(piecewise_z_func(np.array([1,2])), np.sin(2))
