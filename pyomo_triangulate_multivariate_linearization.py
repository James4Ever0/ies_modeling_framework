import pyomo
import pyomo.core.kernel.piecewise_library.util
from linearization_config import *

# func: z = x*sin(y)

from pyomo.core.kernel.variable import variable

x =variable(lb=x_lb,ub=x_ub)
y =variable(lb=y_lb,ub=y_ub)

delaunay = pyomo.core.kernel.piecewise_library.util.generate_delaunay([x,y],num=x_sample_size)

function = 