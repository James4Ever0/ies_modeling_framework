# path = "device_params_intermediate.json"
path = "microgrid_device_params_intermediate.json"

import json

with open(path,'r') as f:
    data = json.load(f)

keys = list(data.keys())

import rich

rich.print(keys)

CHAR_TYPE = ["生产厂商","设备型号"]

COMMENT_TYPE = ["从文件导入、保存数据、从典型库导入"]

META_TYPE = ["设备额定运行参数",'设备经济性参数','设备运行约束']

TRANSLATION_TABLE = {} # EnglishName: [ChineseName, ...]

LIST_TYPE = [] # notice, list contains multiple headings, each heading may have its own unit.

# you may copy this from the table, not parsing it though.

# you need to check for units. 

for key in keys:
    rich.print(data[key].keys())
    # val_list = data[key]
    for subkey in data[key].keys():
        val_list = data[key][subkey]
        # rich.print(val_list)
        for val in val_list:
            val = val.strip("*").strip(":").strip("：").strip()
            val = val.replace("（","(").replace("）",")").replace(" ","")
            print(val)
            if val in CHAR_TYPE:
                print("CHAR_TYPE")
            elif val in META_TYPE:
                print("META_TYPE")
            else:
                raise Exception("Unknown Value:", val)