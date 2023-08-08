import sympy

def solve_eq(a_arr:list, build_time:int, business_time:int):
    i = sympy.symbols("i")
    expr = 0
    for n in range(build_time):
        expr += a_arr[n] / ((1+i)**n)
    for n in range(business_time):
        arr_index = n+build_time
        expr += a_arr[arr_index] /((i+i)**(arr_index+1))
    sympy.solve()