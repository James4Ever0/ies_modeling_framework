# path = "device_params_intermediate.json"
path = "microgrid_device_params_intermediate.json"

import json

with open(path, "r") as f:
    data = json.load(f)

keys = list(data.keys())

import rich

rich.print(keys)

CHAR_TYPE = ["生产厂商", "设备型号"]

COMMENT_TYPE = ["从文件导入、保存数据、从典型库导入"]

META_TYPE = ["设备额定运行参数", "设备经济性参数", "设备运行约束"]

BASE_TRANSLATION_TABLE = {"Area": ["光伏板面积"]}  # EnglishName: [ChineseName, ...]

TRANSLATION_TABLE = {e: k for k, v in BASE_TRANSLATION_TABLE.items() for e in v}

LIST_TYPE = (
    []
)  # notice, list contains multiple headings, each heading may have its own unit.

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
            val = val.replace("（", "(").replace("）", ")").replace(" ", "")
            print(val)
            if val in CHAR_TYPE:
                print("CHAR_TYPE")
            elif val in META_TYPE:
                print("META_TYPE")
            else:
                # begin to parse it.
                import parse

                result = parse.parse("{val_name}({val_unit})", val)
                if result:
                    val_name, val_unit = result["val_name"], result["val_unit"]
                else:
                    val_name = val
                    val_unit = None
                if val_name in TRANSLATION_TABLE.keys():
                    print("TRANS", TRANSLATION_TABLE[val_name])
                raise Exception("Unknown Value:", val)
