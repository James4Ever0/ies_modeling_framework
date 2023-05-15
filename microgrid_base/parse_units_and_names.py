# path = "device_params_intermediate.json"
path = "microgrid_device_params_intermediate.json"

import json

with open(path,'r') as f:
    data = json.load(f)

keys = list(data.keys())

import rich

rich.print(keys)

CHAR_TYPE = []

META_TYPE = []

TRANSLATION_TABLE = {} # EnglishName: [ChineseName, ...]

LIST_TYPE = [] # notice, list contains multiple headings, each heading may have its own unit.

# you may copy this from the table, not parsing it though.

# you need to check for units. 

for key in keys:
    rich.print(data[key].keys())
    # val_list = data[key]
    for subkey in data[key].keys():
        val_list = data[key][subkey]
        rich.print(val_list)