# there involves multiplication, division, scale factors.
import pint
# similar projects: https://pint.readthedocs.io/en/stable/getting/faq.html
ureg = pint.UnitRegistry()

a = ureg.cm
print(a) # centimeter?

# either load from definition file or just here.
# https://pint.readthedocs.io/en/stable/advanced/defining.html
ureg.define("元 = [currency]")
ureg.define("百元 = 100 * 元")
ureg.define("千元 = 1000 * 元")
ureg.define("万元 = 10000 * 元")
ureg.define("亿元 = 10000 * 万元")
# b = ureg.dollar # not defined? let's define new units?
# print(b)