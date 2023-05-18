path = "microgrid_device_params_intermediate.json"

# 电负荷 柴油原件需要单独列出来
microgrid_device_name_path = "microgrid_device_names.json"

import json

with open(path, 'r') as f:
    data = json.load(f)

