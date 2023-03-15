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
ureg.define("m2 = meter * meter")  # working or not?

c = ureg.celsius
# you cannot do this: ureg['℃']
# this is not a valid name.
# ureg.__getattr__("°C")
print(c)  # invalid charactor: ℃
print(
    ureg.W, ureg.kW, ureg.kWh, ureg.年, ureg.MPa, ureg.m2, ureg.MVA, ureg.Ω, ureg.MΩ
)  # great.

val = b.to(ureg.万元)
print(val, val.magnitude)  # the float val.
# breakpoint()
val2 = ureg.Quantity(100, "元/kWh").to("万元/kWh")
print(val2, val2.magnitude)
print()

root_units = val2.to_root_units()
serialized_quantity = val2.to_tuple()

print(root_units)
print(serialized_quantity)

# (0.01, (('万元', 1), ('kilowatt_hour', -1)))
# how to detect and convert?
magnitude, unit_tuple = serialized_quantity

# how to parse the unit tuple?
# ureg.parse_units()
myUnit = ureg.UnitsContainer(unit_tuple)
print("MYUNIT:", myUnit)
# once you know the trick...

# convert to preferred unit system: https://pint.readthedocs.io/en/stable/user/systems.html
# how to create a unit system?
conversion_dict = {""}

# what is the target unit?
for 
