# there involves multiplication, division, scale factors.
import pint
# similar projects: https://pint.readthedocs.io/en/stable/getting/faq.html
ureg = pint.UnitRegistry()

a = ureg.cm
print(a) # centimeter?
# b = ureg.dollar # not defined? let's define new units?
# print(b)