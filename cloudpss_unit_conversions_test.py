# there involves multiplication, division, scale factors.
import pint

# similar projects: https://pint.readthedocs.io/en/stable/getting/faq.html
ureg = pint.UnitRegistry()

a = 1 * ureg.cm
print(a)  # centimeter?

# either load from definition file or just here.
# https://pint.readthedocs.io/en/stable/advanced/defining.html
ureg.define("元 = [currency]")
ureg.define("百- = 100")
ureg.define("千- = 1000")
ureg.define("万- = 10000")
ureg.define("亿- = 100000000")
# b = ureg.dollar # not defined? let's define new units?
b = 1 * ureg.元
print(b)

ureg.define("年 = year")
ureg.define("m2 = meter * meter") # working or not?

c = ureg.celsius
# you cannot do this: ureg['℃']
print(c)  # invalid charactor: ℃
print(ureg.W, ureg.kW,ureg.kWh,ureg.年,ureg.MPa,ureg.m2) # great.