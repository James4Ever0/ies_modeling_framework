print("first line")
print("second line")

import sympy

a, b = sympy.symbols("a b")

summation = sympy.Sum(a, (a, 1, b), assumptions=dict(cond1=b > 1))

# summation

sympy.pretty_print(summation)
sympy.print_latex(summation)
