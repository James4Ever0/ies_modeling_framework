import jinja2
import json
import rich

load_path = "cloudpss_inputs.json"

with open(load_path,'r',encoding='utf-8') as f:
    data = json.loads(f.read())
    # rich.print(data)

excelMap = data['excelMap']

dataParams = {"ratedParam":"","":"","":""}

for key, value in excelMap.items():
    if type(value) == dict:
        if "生产厂商" in value.keys():
            # this is a device for sure.
            # rich.print(value)
            for k,v in value.items():
                if v.split(".")[0] in dataParams.keys():
                    k0 = dataParams[v.split(".")[0]]
                    print(k0, k, v.split(".")[-1])
                else in ['manufacturer','equipType']:
                    print(k,v)
                else:
                    print(">> UNIDENTIFIED PARAM TYPE <<")
                    print(k,v)
            print("_"*30)