from sympy.abc import x, y
import numpy as np

expr = x*y - (x+y)
# help(expr.evalf)
print(expr.evalf(subs = {x: 1, y:2}))