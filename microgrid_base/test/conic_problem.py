from sympy.abc import x, y
import numpy as np

expr = x*y - (x+y)
# help(expr.evalf)
x_min, x_max = 1,5
y_min, y_max = 2,4


min_val = 1000
max_val = -1000
for _x in np.linspace(x_min, x_max, 100):
    for _y in np.linspace(y_min, y_max, 100):
        val = expr.evalf(subs = {x: _x, y:_y})
        if 