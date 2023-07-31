print("first line")
print("second line")

import sympy

a, b, c= sympy.symbols("a b c")

summation = sympy.Sum(c[a], (a, 1, b))

# summation

sympy.pretty_print(summation)
sympy.print_latex(summation)
