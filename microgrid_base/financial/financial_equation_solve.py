import sympy


def solve_eq(a_arr: list, build_time: int, business_time: int) -> float:
    assert len(a_arr) == build_time + business_time
    i = sympy.symbols("i")
    expr = 0
    for n in range(build_time):
        expr += a_arr[n] / ((1 + i) ** (n + (0 if n < build_time else 1)))
    sol = sympy.nsolve(
        sympy.Eq(expr, 0), i, (0, 1), solver="bisect", verify=True
    )  # will raise exception if no solution exists.
    return sol


a_arr = [
    -6511.07,
    1283.97,
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
print(sol)  # float
