path = "device_params_intermediate.json"

import json

with open(path,'r') as f:
    data = json.load(f)

keys = list(data.keys())