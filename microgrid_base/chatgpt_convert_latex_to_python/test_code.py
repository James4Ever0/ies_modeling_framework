print("first line")
print("second line")

import sympy
# ref: https://github.com/sympy/sympy/issues/9861

# a, b= sympy.symbols("a b")
# a, b= sympy.symbols("a_b b")
a, b= sympy.symbols("a^b b")
# r = sympy.Range(1,10)

summation = sympy.Sum(a, (b, 1, 10), )
# summation = sympy.Sum(a, (a, 1, b), r)
# summation = sympy.Sum(c[a], (a, 1, b), r)
# summation

sympy.pretty_print(summation)
sympy.print_latex(summation)

sympy.pretty_print(sympy.Derivative(b,b))
sympy.print_latex(sympy.Derivative(b,b))

sympy.print_latex(sympy.Integral(b,b))