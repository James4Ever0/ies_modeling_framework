# path = "device_params_intermediate.json"
path = "microgrid_device_params_intermediate.json"

import json
from typing import ItemsView
import parse
import pint


unit_def_path = "../merged_units.txt"
ureg = pint.UnitRegistry(unit_def_path)

with open(path, "r") as f:
    data = json.load(f)

keys = list(data.keys())

import rich

rich.print(keys)

CHAR_TYPE = ["生产厂商", "设备型号"]

COMMENT_TYPE = ["从文件导入、保存数据、从典型库导入"]

META_TYPE = ["设备额定运行参数", "设备经济性参数", "设备运行约束"]

BASE_TRANSLATION_TABLE_WITH_BASE_UNIT = {
    "Area": (
        "m2",
        {"":["光伏板面积"],
        }
    ),
    "Efficiency": (
        "percent",
        {"":"电电转换效率"}
    ),
    "Power": ("kW", {""})
}  # EnglishName: (BaseUnit, [ChineseName, ...])

BASE_CLASS_TO_UNIT_TABLE = {
    k: v[0] for k, v in BASE_TRANSLATION_TABLE_WITH_BASE_UNIT.items()
}


def revert_dict(mdict: dict):
    result = {e: k for k, v in mdict.items() for e in v}
    return result


TRANSLATION_TABLE = revert_dict(
    {k: v[1] for k, v in BASE_TRANSLATION_TABLE_WITH_BASE_UNIT.items()}
)

LIST_TYPE = (
    []
)  # notice, list contains multiple headings, each heading may have its own unit.

BASE_UNIT_TRANSLATION_TABLE = {"percent": ["%"]}

UNIT_TRANSLATION_TABLE = revert_dict(BASE_UNIT_TRANSLATION_TABLE)

# you may copy this from the table, not parsing it though.

# you need to check for units.

for key in keys:
    rich.print(data[key].keys())
    # val_list = data[key]
    for subkey in data[key].keys():
        val_list = data[key][subkey]
        # rich.print(val_list)
        print("____" * 10 + "[{}-{}]".format(key, subkey))
        for val in val_list:
            print("____" * 10)
            val = val.replace("（", "(").replace("）", ")").replace(" ", "")
            val = val.strip("*").strip(":").strip("：").strip()
            print(val)
            if val in CHAR_TYPE:
                print("CHAR_TYPE")
            elif val in META_TYPE:
                print("META_TYPE")
            else:
                # begin to parse it.
                result = parse.parse("{val_name}({val_unit})", val)
                if result:
                    val_name, val_unit = (
                        result["val_name"].strip(),
                        result["val_unit"].strip(),
                    )
                else:
                    val_name = val
                    val_unit = None
                if val_name in TRANSLATION_TABLE.keys():
                    base_class = TRANSLATION_TABLE[val_name]
                    default_unit = BASE_CLASS_TO_UNIT_TABLE[base_class]
                    print("DEFAULT UNIT:", default_unit)
                    default_unit_real = ureg.Unit(default_unit)
                    default_unit_compatible = ureg.get_compatible_units(
                        default_unit_real
                    )
                    print("TRANS {} -> {}".format(val_name, base_class))
                    if val_unit:
                        for (
                            trans_source_unit,
                            trans_target_unit,
                        ) in UNIT_TRANSLATION_TABLE.items():
                            val_unit = val_unit.replace(
                                trans_source_unit, trans_target_unit
                            )
                        # parse this unit!
                    else:
                        val_unit = default_unit
                        print("USING DEFAULT UNIT")
                    print("UNIT", val_unit)
                    unit = ureg.Unit(val_unit)
                    compatible_units = ureg.get_compatible_units(val_unit)
                    # print("COMPATIBLE UNITS", compatible_units)
                    if not default_unit_compatible == compatible_units:
                        raise Exception(
                            "Unit {} not compatible with default unit {}".format(
                                val_unit, default_unit
                            )
                        )
                else:
                    raise Exception("Unknown Value:", val)
