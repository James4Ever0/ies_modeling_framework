additionalUnitDefinitions="""
元 = [currency]
百- = 100
千- = 1000
万- = 10000
亿- = 100000000
"""

output_path="merged_units.txt"


import pint
import os

directory_path = os.path.dirname(pint.__file__)
default_unit_file = os.path.join(directory_path,"default_en.txt") # there are some file we must have.

constant_file = "constants_en.txt"
import shutil
shutil.copy(os.path.join(directory_path,constant_file), constant_file)

with open(default_unit_file,'r') as f0:
    default_units_definitions = f0.read()
with open(output_path,'w+', encoding='utf-8') as f:
    f.write(default_units_definitions)
    f.write(additionalUnitDefinitions)

# we are going to check this.

ureg = pint.UnitRegistry(output_path)

compat_units_0 = ureg.get_compatible_units(ureg.万元)
compat_units_1 = ureg.get_compatible_units(ureg.元) # there are no base units?

print(compat_units_0)
print("_"*20)
print(compat_units_1)