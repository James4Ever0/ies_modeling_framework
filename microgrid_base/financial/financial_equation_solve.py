import sympy
import numpy as np
from typing import cast
def solve_eq(a_arr: list, build_time: int, business_time: int):
    assert len(a_arr) == build_time + business_time
    i = sympy.symbols("i")
    expr= cast(sympy.Expr,0)
    for n in range(build_time+business_time):
        expr += a_arr[n] / ((1 + i) ** (n + (0 if n < build_time else 1)))
    print('[expr]',expr)
    try:
        sol = sympy.nsolve(
            sympy.Eq(expr, 0), i, (0, 1), solver="bisect", verify=True
        )  # will raise exception if no solution exists.
        return sol
    except:
        vals = [expr.evalf(subs={i:v}) for v in np.linspace(0, 1, 100)]
        print(vals)

# a_arr = [
#     -6511.07,
#     1283.97,
#     5714.22,
#     7854.22,
#     -14725.82,
#     1841.11,
#     10792.05,
#     10792.05,
#     10792.05,
#     10792.05,
#     11190.56,
#     2343.6,
# ]

a_arr = [
    -7075.02,
    1105.57,
    5714.22,
    7854.22,
    -14725.82,
    1841.11,
    10792.05,
    10792.05,
    10792.05,
    10792.05,
    11190.56,
    2343.6,
]

build_time = 2
business_time = 10

sol = solve_eq(a_arr, build_time, business_time)
if sol:
    print('[sol]',sol)  # float
else:
    print("no solution.")