# main_path = "device_params_intermediate.json" # data parse here. since we are changing the main table.
# device_name_path = "microgrid_device_params_intermediate.json" # just for reference.

device_data_path_base = "device_params_intermediate.json"

import json
import rich

EXCEL = "嵌套"

MEASURE = "调度"

with open(device_data_path_base, "r") as f:
    device_data = json.load(f)

microgrid_device_port_path = "microgrid_device_port_type_mapping.json"

with open(microgrid_device_port_path, "r") as f:
    port_dict = json.load(f)

data = {}

all_microgrid_device_keys = []

for k, v in port_dict.items():
    for k1, v1 in v.items():
        k0 = f"{k}-{k1}"
        all_microgrid_device_keys.append(k0)

data = {}
data_is_excel = {}

def none_fallback(e):
    if type(e)!=str:
        return ""
    return e

for k, v in device_data.items():
    for k1, v1 in v.items():
        k0 = f"{k}-{k1}"
        if k0 in all_microgrid_device_keys:
            vlist = []
            v_is_excel_list = []
            for v2 in v1:
                v2 = [none_fallback(e) for e in v2]
                val = v2[0].strip()
                if val == "-": continue
                v_is_excel = (EXCEL in v2[1]) or (EXCEL in v2[2])
                
                v_is_measured = MEASURE in v2[2]
                
                if not v_is_measured:
                    vlist.append(val)
                    v_is_excel_list.append(v_is_excel)

            data[k] = data.get(k, {})
            data[k][k1] = vlist

            data_is_excel[k] = data_is_excel.get(k, {})
            data_is_excel[k][k1] = v_is_excel_list
        else:
            continue
# 没有其他类元件：母线和母线接口

# 锂电池
# 年放电量需求 * 换芯周期 <= 电池机组容量 * 循环寿命 * 0.85
# 作为电池数量限制的一部分

import parse
import pint


unit_def_path = "../merged_units.txt"
ureg = pint.UnitRegistry(unit_def_path)

# with open(path, "r") as f:
#     data = json.load(f)

keys = list(data.keys())

rich.print(keys)
rich.print(data)

CHAR_TYPE = ["生产厂商", "设备型号"]

COMMENT_TYPE = ["从文件导入、保存数据、从典型库导入"]

META_TYPE = ["设备额定运行参数", "设备经济性参数", "设备运行约束"]

BASE_TRANSLATION_TABLE_WITH_BASE_UNIT = {
    "Area": (
        "m2",
        {
            "": ["光伏板面积"],
        },
    ),
    "Efficiency": ("percent", {"": ["电电转换效率"]}),
    "Power": ("kW", {"": [], "Unit-": ["组件额定功率"], "MaxUnit-": ["最大发电功率"]}),
    "DeltaLimit": ("percent/second", {"": [], "Power-": ["发电爬坡率"]}),
    "Cost": ("万元/kW", {"": ["采购成本"]}),
    "CostPerYear": ("万元/(kW*年)", {"":["固定维护成本"]}),
    "VariationalCost": ("/", {"": [""]})
}  # EnglishName: (BaseUnit, {convert_string:[ChineseName, ...], ...})


# convert_string: "[prefix][-][suffix]"
# contain either 1 or no hyphen.
# if contain no hyphen, it must be empty string.


def parse_convert_string(convert_string: str):
    convert_string = convert_string.strip()
    hyphen_count = convert_string.count("-")
    prefix = ""
    suffix = ""
    if hyphen_count == 1:
        if convert_string.startswith("-"):
            suffix = convert_string.strip("-")
        elif convert_string.endswith("-"):
            prefix = convert_string.strip("-")
        else:  # in the middle!
            prefix, suffix = convert_string.split("-")
        prefix = prefix.strip()
        suffix = suffix.strip()
    elif hyphen_count == 0:
        if len(convert_string) != 0:
            raise Exception("You should pass an empty string this time")
    else:
        raise Exception("Invalid convert string:", convert_string)
    return prefix, suffix


BASE_TRANSLATION_TABLE = {}
BASE_CLASS_TO_UNIT_TABLE = {}

for k, v in BASE_TRANSLATION_TABLE_WITH_BASE_UNIT.items():
    for k1, v1 in v[1].items():
        prefix, suffix = parse_convert_string(k1)
        k0 = prefix + k.strip() + suffix
        BASE_TRANSLATION_TABLE.update({k0: v1})
        BASE_CLASS_TO_UNIT_TABLE.update({k0: v[0]})

# BASE_CLASS_TO_UNIT_TABLE = {
#     k: v[0] for k, v in BASE_TRANSLATION_TABLE_WITH_BASE_UNIT.items()
# }


def revert_dict(mdict: dict):
    result = {e: k for k, v in mdict.items() for e in v}
    return result


TRANSLATION_TABLE = revert_dict(BASE_TRANSLATION_TABLE)
# TRANSLATION_TABLE = revert_dict({k: v for k, v in BASE_TRANSLATION_TABLE.items()})

LIST_TYPE = [
    "嵌套表格"
]  # check this in the 2nd index  # notice, list contains multiple headings, each heading may have its own unit.

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
