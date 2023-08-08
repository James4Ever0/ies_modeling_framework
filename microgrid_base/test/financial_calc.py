def calc(i, a_arr: list, x):
    f = lambda i, n, a: a / ((1 + i) ** n)
    result = -x
    for n, a in enumerate(a_arr):
        result += f(i, n, a)
    return result

