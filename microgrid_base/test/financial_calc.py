def calc(i, a_arr: list, x):
    f = lambda i, n, a: a / ((1 + i) ** n)
    result = -x
    for n, a in enumerate(a_arr):
        result += f(i, n + 1, a)
    return result


a_arr = [
    -28197.28,
    -4789.57,
    6691,
    8706.48,
    8932.69,
    9605.62,
    11030.94,
    11281.97,
    11259.61,
    11236.13,
    11609.99,
    2075.55,
]
i = 0.05
x = 29695.24

ret = calc(i, a_arr, x)
print(ret)
