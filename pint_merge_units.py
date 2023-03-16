additionalUnitDefinitions = """
元 = [currency]
万元 = 10000 元

年 = year
m2 = meter ** 2
"""

# by not using prefixes, you have all the units.

output_path = "merged_units.txt"


import pint
import os

directory_path = os.path.dirname(pint.__file__)
default_unit_file = os.path.join(
    directory_path, "default_en.txt"
)  # there are some file we must have.

constant_file = "constants_en.txt"
import shutil

shutil.copy(os.path.join(directory_path, constant_file), constant_file)

with open(default_unit_file, "r") as f0:
    default_units_definitions = f0.read()
with open(output_path, "w+", encoding="utf-8") as f:
    f.write(default_units_definitions)
    f.write(additionalUnitDefinitions)

# we are going to check this.

ureg = pint.UnitRegistry(output_path)

compat_units_0 = ureg.get_compatible_units(ureg.万元)
compat_units_1 = ureg.get_compatible_units(ureg.元)  # there are no base units?

# it will be converted to base units?

print(compat_units_0)
print("_" * 20)
print(compat_units_1)  # frozen set.

# breakpoint()
# print(list(compat_units_0))

## now, the classic test?
quantity = ureg.Quantity(1, "元/kWh")
# quantity = ureg.Quantity(1, ureg.元/ureg.kWh)
magnitude, units = quantity.to_tuple()

standard_units = frozenset([ureg.万元])

new_units_list = []
for unit, power in units:
    # if type(unit)!=str:
    print("UNIT?", unit, "POWER?", power)
    compat_units = ureg.get_compatible_units(unit)  # frozen set.
    intersection = compat_units.intersection(standard_units)
    if len(intersection) != 0:
        if len(intersection) == 1:
            # ready to convert?
            unit = list(intersection)[0]
        else:
            raise Exception("Too many intersections with standard units:", intersection)
    new_units_list.append((unit, power))

print("NEW UNITS LIST:", new_units_list)
new_unit = ureg.UnitsContainer(tuple(new_units_list))

new_quantity = quantity.to(new_unit)

print("OLD QUANTITY:", quantity)
print("NEW QUANTITY:", new_quantity)
