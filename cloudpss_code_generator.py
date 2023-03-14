import jinja2
import json
import rich

load_path = "cloudpss_inputs.json"

with open(load_path,'r',encoding='utf-8') as f:
    data = json.loads(f.read())
    # rich.print(data)

excelMap = data['excelMap']

for key, value in excelMap.items():
    if type(value) == dict:
        if "生产厂商" in value.keys():
            # this is a device for sure.
            rich.print(value)
            print("_"*30)