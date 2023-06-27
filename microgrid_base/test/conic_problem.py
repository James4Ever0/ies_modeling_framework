from sympy.abc import x, y
import numpy as np

expr = x*y - 2*x+3*y
# help(expr.evalf)
x_min, x_max = 1,5
y_min, y_max = 2,4


min_val = 1000
max_val = -1000
min_inputs = []
max_inputs = []
for _x in np.linspace(x_min, x_max, 100):
    for _y in np.linspace(y_min, y_max, 100):
        val = expr.evalf(subs = {x: _x, y:_y})
        if val < min_val:
            min_val = val
            min_inputs = [_x, _y]
        if val > max_val:
            max_val = val
            max_inputs = [_x, _y]
        

print(f"MIN: {min_val}, MAX: {max_val}")
print(f"MIN_INPUT: {min_inputs}, MAX_INPUT: {max_inputs}")