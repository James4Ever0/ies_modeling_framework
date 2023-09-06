import sympy
import numpy as np
from typing import cast


def solve_eq(a_arr: list, build_time: int, business_time: int):
    assert len(a_arr) == build_time + business_time
    i = sympy.symbols("i")
    expr = cast(sympy.Expr, 0)
    for n in range(build_time + business_time):
        expr += a_arr[n] / ((1 + i) ** (n + (0 if n < build_time else 1)))
    print("[expr]", expr)
    try:
        sol = sympy.nsolve(
            sympy.Eq(expr, 0), i, (0, 1), solver="bisect", verify=True
        )  # will raise exception if no solution exists.
        return sol
    except:
        vals = [expr.evalf(subs={i: v}) for v in np.linspace(0, 1, 100)]
        print("possible vals:", vals)


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

# a_arr = [
#     -7075.02,
#     1105.57,
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

# a_arr = [
#     -5947.12,
#     1462.36,
#     5714.22,
#     2077.78,
#     25721.82,
#     9883.89,
#     1920.25,
#     1920.25,
#     1920.25,
#     1920.25,
#     1920.25,
#     511.45,
# ]

# a_arr = [
#     -6524.35,
#     1270.69,
#     5700.94,
#     7840.94,
#     -14813.62,
#     1777.67,
#     10778.77,
#     10778.77,
#     10778.77,
#     10778.77,
#     11177.28,
#     2330.32,
# ]

# a_arr = [
#     -6497.79,
#     191.68,
#     5727.5,
#     7867.5,
#     14638.02,
#     1904.55,
#     10805.33,
#     10805.33,
#     10805.33,
#     10805.33,
#     11203.84,
#     2356.88,
# ]

# a_arr = [
#     -62130034399.855,
#     -62130034399.855,
#     966.026,
#     859.026,
#     869.026,
#     859.026,
#     6307364303.757,
# ]

# a_arr = [
#     -62130034399.855,
#     -62130034399.855,
#     4793596993.616,
#     4793596890.016,
#     4793596898.016,
#     4793596890.016,
#     11100960332.746,
# ]

# a_arr = [
#     -43491024079.899,
#     -43491024079.90,
#     -3860929680.735,
#     -3931808967.953,
#     -4006232097.503,
#     -4084376399.929,
#     2140935528.653,
# ]

# a_arr = [-68.291, -68.291, 796.343, 687.631, 695.514, 687.392, 705.167]
a_arrs = [
    [-609.991, -609.991, 585.69, 478.69, 488.69, 478.69, 555.616],
    [-609.991, -609.991, 529.815, 426.215, 434.215, 426.215, 501.141],
    [ -426.994, -426.994, 449.726, 340.43, 347.699, 338.932, 408.052],
]

build_time = 2
business_time = 5
# business_time = 10

for i, a_arr in enumerate(a_arrs):
    print(f"SOLVING ARR #{i}".center(70, "="))
    sol = solve_eq(a_arr, build_time, business_time)
    if sol:
        print("[sol]", sol)  # float
    else:
        print("no solution.")
