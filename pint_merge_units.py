additionalUnitDefinitions="""

"""

output_path="merged_units.txt"


import pint
import os

directory_path = os.path.dirname(pint.__file__)
default_unit_file = os.path.join(directory_path,"default_en.txt")

with open(default_unit_file,'r') as f0:
    default_units_definitions = f0.read()
with open(output_path,'w+', encoding='utf-8') as f:
    f.write(default_units_definitions)
    f.write(additionalUnitDefinitions)

# we are going to check this.

ureg = pint.UnitRegistry(output_path)
ureg.