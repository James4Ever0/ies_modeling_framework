print("first line")
print("second line")

import sympy

# ref: https://github.com/sympy/sympy/issues/9861

# a, b= sympy.symbols("a b")
# a, b= sympy.symbols("a_b b")
# a, b= sympy.symbols("a^b b")
# r = sympy.Range(1,10)
b = sympy.symbols("b", positive=True, integer=True)
a = sympy.IndexedBase("a")
summation = sympy.Sum(
    a[b],
    (b, 1, 10),
)
# summation = sympy.Sum(a, (a, 1, b), r)
# summation = sympy.Sum(c[a], (a, 1, b), r)
# summation
with sympy.assuming(sympy.Q.integer(a)):
    sympy.pretty_print(summation)
    sympy.print_latex(summation)

sympy.pretty_print(sympy.Derivative(b, b))
sympy.print_latex(sympy.Derivative(b, b))

sympy.print_latex(sympy.Integral(b, b))
# sympy.print_latex(sympy.Q.negative(a))
# sympy.print_latex(b)
c, d = sympy.symbols("变量1 变量2")
# unacceptable form.
# sympy.print_latex(10>= c >=1)
sympy.print_latex(10 >= c)
sympy.print_latex(sympy.S.Reals) # working.
sympy.print_latex(sympy.Interval(0, 1).contains(c))

sympy.print_latex(sympy.S.Reals.contains(c))
print()
print(dir(c))
print()
print(dir(sympy.S.Reals))
sympy.print_latex(sympy.ceiling(c))
sympy.print_latex(sympy.Interval(0, 1))
# sympy.print_latex(c*d) # this is bad syntax.
sympy.print_latex(c*d, mul_symbol=r"\times")