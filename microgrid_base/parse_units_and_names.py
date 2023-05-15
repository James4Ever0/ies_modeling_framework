# path = "device_params_intermediate.json"
path = "microgrid_device_params_intermediate.json"

import json

with open(path,'r') as f:
    data = json.load(f)

keys = list(data.keys())

import rich

rich.print(keys)

for key in keys:
    rich.print(data[key].keys())
    