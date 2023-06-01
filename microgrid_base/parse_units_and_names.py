# main_path = "device_params_intermediate.json" # data parse here. since we are changing the main table.
# device_name_path = "microgrid_device_params_intermediate.json" # just for reference.

device_data_path_base = "device_params_intermediate.json"

import pint

import json
import rich

from unit_utils import (
    unitFactorCalculator,
    ureg,
    standard_units,
    getSingleUnitConverted,
    translateUnit
)

EXCEL = "嵌套"

MEASURE = "调度"


def get_table_format(k, u):
    try:
        t = {
            "燃油消耗率": {str(ureg.Unit("m3 / kWh")): ("负载率", "%")},
        }
        return t[k][str(u)]  # name, unit
    except:
        raise Exception("No table format for", k, u)


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
    if type(e) != str:
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
                if val == "-":
                    continue
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


# rich.print(data_is_excel)
# breakpoint()
# cat -> name -> [bool]

# 锂电池
# 年放电量需求(kWh) * 换芯周期(年) <= 电池机组容量(kWh) * 循环寿命(年) * 0.85
# 作为电池数量限制的一部分

import parse

# import pint


# with open(path, "r") as f:
#     data = json.load(f)

keys = list(data.keys())

rich.print(keys)
rich.print(data)

CHAR_TYPE = ["生产厂商", "设备型号"]

COMMENT_TYPE = ["从文件导入、保存数据、从典型库导入"]

META_TYPE = [
    "设备额定运行参数",
    "设备经济性参数",
    "设备运行约束",
]  # parse this?

SKIP_TYPE = ["设计规划拓扑图右侧菜单", "设计规划系统-拓扑图右侧菜单"]

BASE_TRANSLATION_TABLE_WITH_BASE_UNIT = {
    "Area": (
        "m2",
        {"": ["光伏板面积"], "MaxInstall-": ["最大安装面积"], "MinInstall-": ["最小安装面积"]},
    ),
    "Load": ("percent", {"": ["负载率"]}),
    "Efficiency": (
        "one",
        {
            "PowerConversion-": ["电电转换效率"],
            "Charge-": ["充能效率"],
            "Discharge-": ["放能效率"],
            "": ["效率"],
        },
    ),
    "Parameter": ("one", {"Power-": ["功率因数"], "LoadRedundancy-": ["变压器冗余系数"]}),
    "Count": (
        "台",
        {"Device-": ["安装台数"], "MaxDevice-": ["最大安装台数"], "MinDevice-": ["最小安装台数"]},
    ),
    "Length": ("km", {"": ["长度"]}),
    "Power": (
        "kW",
        {"Rated-": ["额定功率", "变压器容量"], "UnitRated-": ["组件额定功率"], "Max-": ["最大发电功率"]},
    ),
    "WindSpeed": ("m/s", {"Rated-": ["额定风速"], "Min-": ["切入风速"], "Max-": ["切出风速"]}),
    "DieselToPower": ("L/kWh", {"": ["燃油消耗率"]}),
    "StartupLimit": ("percent", {"Power-": ["启动功率百分比"]}),
    "DeltaLimit": (
        "one/second",
        {
            "": [],
            "Power-": [
                "发电爬坡率",
            ],
            "Battery-": ["电池充放电倍率"],
        },
    ),  # two unit system.
    "SOC": ("percent", {"Min-": ["最小SOC"], "Max-": ["最大SOC"], "Init-": ["初始SOC"]}),
    "StorageDecay": ("percent/hour", {"Battery-": ["存储衰减"]}),
    "TransferDecay": ("kW/km", {"Power-": ["能量衰减系数"]}),
    "BuildBaseCost": ("万元", {"": ["建设费用基数"]}),
    "CostPerKilowatt": ("万元/kW", {"": ["采购成本"], "Build-": ["建设费用系数"]}),
    "CostPerCapacity": ("万元/kWh", {"": ["采购成本"], "Build-": ["建设费用系数"]}),
    "CostPerKilometer": ("万元/km", {"": ["采购成本"], "Build-": ["建设费用系数"]}),
    "CostPerMachine": ("万元/台", {"": ["采购成本"], "Build-": ["建设费用系数"]}),
    "CostPerYearPerMachine": (
        "万元/(台*年)",
        {
            "": ["固定维护成本"],
        },
    ),
    "CostPerYearPerKilowatt": ("万元/(kW*年)", {"": ["固定维护成本"]}),
    "CostPerYearPerCapacity": ("万元/(kWh*年)", {"": ["固定维护成本"]}),
    "VariationalCostPerWork": ("元/kWh", {"": ["可变维护成本"]}),
    "CostPerYearPerKilometer": ("万元/(km*年)", {"": ["维护成本"]}),
    "Life": ("年", {"": ["设计寿命"], "Battery-": ["电池换芯周期"]}),
    "Capacity": (
        "kWh",
        {
            "Rated-": ["额定容量"],
            "MaxTotal-": ["最大设备容量"],
            "MinTotal-": ["最小设备容量"],
            "TotalDischarge-": ["生命周期总放电量"],
        },
    ),
}  # EnglishName: (ReferenceBaseUnit, {convert_string:[ChineseName, ...], ...})

# checking these units.
# they shall never be going too far.

# for k, v in BASE_TRANSLATION_TABLE_WITH_BASE_UNIT.items():
#     v_unit = v[0]
#     mag, munit = unitFactorCalculator(ureg, standard_units, v_unit)
#     if mag != 1:
#         print("-"*20)
#         print("ERROR! MAGNITUDE:", mag)
#         print("KEY:", k)
#         print("ORIGINAL UNIT:", v_unit)
#         print("CONVERTED UNIT:", munit)
#         print("-"*20)
#         raise Exception("Standard Unit Error")

# TODO: check if units are compatible. set standard units.
##################

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


TRANSLATION_TABLE = {}
# BASE_TRANSLATION_TABLE = {}
BASE_CLASS_TO_UNIT_TABLE = {}

for k, v in BASE_TRANSLATION_TABLE_WITH_BASE_UNIT.items():
    for k1, v1 in v[1].items():
        prefix, suffix = parse_convert_string(k1)
        k0 = prefix + k.strip() + suffix

        # BASE_TRANSLATION_TABLE.update({k0: v1})
        # BASE_CLASS_TO_UNIT_TABLE.update({k0: v[0]})

        BASE_CLASS_TO_UNIT_TABLE[k0] = v[0]
        for v2 in v1:
            TRANSLATION_TABLE[v2] = TRANSLATION_TABLE.get(v2, []) + [k0]
        # BASE_CLASS_TO_UNIT_TABLE[k] = BASE_CLASS_TO_UNIT_TABLE.get(k0, []) + [v[0]]

# print()
# rich.print(BASE_CLASS_TO_UNIT_TABLE)
# breakpoint()
# print()
# rich.print(TRANSLATION_TABLE)
# breakpoint()

# BASE_CLASS_TO_UNIT_TABLE = {
#     k: v[0] for k, v in BASE_TRANSLATION_TABLE_WITH_BASE_UNIT.items()
# }


# rich.print(BASE_TRANSLATION_TABLE)
# rich.print(TRANSLATION_TABLE)
# breakpoint()
# TRANSLATION_TABLE = revert_dict(BASE_TRANSLATION_TABLE)
# TRANSLATION_TABLE = revert_dict({k: v for k, v in BASE_TRANSLATION_TABLE.items()})

# LIST_TYPE = [
#     "嵌套表格"
# ]  # check this in the 2nd index  # notice, list contains multiple headings, each heading may have its own unit.


def add_range_translation(mdict, source, target):
    mdict.update(
        {
            f"最大{source}": f"Max{target}",
            f"最小{source}": f"Min{target}",
        }
    )


META_TRANSLATION_TABLE = {
    "设计规划": "DesignParams",
    "仿真模拟": "SimulationParams",
    "设备选型": "DeviceModel",
}
add_range_translation(META_TRANSLATION_TABLE, "安装面积", "Area")
add_range_translation(META_TRANSLATION_TABLE, "安装台数", "DeviceCount")
# you may copy this from the table, not parsing it though.

# you need to check for units.

# output_data = {"unit_conversion", ""}

output_data = {}  # category -> device_name -> {设备参数, 设计规划, 仿真模拟}


def getUnitConverted(val_name, val_unit):
    base_classes = TRANSLATION_TABLE[val_name]
    has_exception = False
    
    _val_unit = val_unit

    if _val_unit:
        _val_unit = translateUnit(_val_unit)

    for base_class in base_classes:
        default_unit = BASE_CLASS_TO_UNIT_TABLE[base_class]
        # iterate through all base classes.
        
        val_unit = _val_unit
        
        has_exception, val_unit = getSingleUnitConverted(default_unit=default_unit, val_unit=val_unit)
        
        if has_exception:
            continue
        elif val:
            # get factor:
            mag, standard = unitFactorCalculator(ureg, standard_units, val_unit)
            print("STANDARD:", standard)
            print("MAGNITUDE TO STANDARD:", mag)
            has_exception = False
            return has_exception, (base_class, val_unit, mag, standard)
    return True, (None, None, None, None)  # has_exception, uc


def getValueParam(uc, val_name):
    (base_class, val_unit, mag, standard) = uc
    vparam = [
        base_class,
        val_name,
        val_unit,
        standard,
        mag,
    ]  # to list. instead of tuple, for serialization
    # vparam = (base_class, val_name, val_unit, standard, mag)
    return vparam


def wrapper_uc_vp(val_name, val_unit):
    has_exception, uc = getUnitConverted(val_name, val_unit)
    if has_exception:
        raise Exception(f"No compatibie unit found for {val_name} with unit {val_unit}")
    vparam = getValueParam(uc, val_name)
    return vparam


for key in keys:
    rich.print(data[key].keys())
    # val_list = data[key]
    output_data[key] = {}
    # print(key)
    # breakpoint()
    for subkey in data[key].keys():
        output_data[key][subkey] = {"设备参数": [], "设计规划": [], "仿真模拟": []}
        val_list = data[key][subkey]
        # rich.print(val_list)
        print("____" * 10 + "[{}-{}]".format(key, subkey))
        meta_type = None
        for index, val in enumerate(val_list):
            val_is_table = data_is_excel[key][subkey][
                index
            ]  # TODO: USE THIS VALUE TO CHECK IF IS TABLE! (also the data format)
            print("____" * 10)
            val = (
                val.replace("（", "(")
                .replace("）", ")")
                .replace(" ", "")
                .replace(";", "")
                .replace("；", "")
            )
            val = val.strip("*").strip(":").strip("：").strip()
            print(val)
            if val in CHAR_TYPE:
                print("CHAR_TYPE")
                output_data[key][subkey]["设备参数"].append(val)
            elif val in META_TYPE or val in SKIP_TYPE:
                print("META_TYPE")
                meta_type = val
                # appending values, presumed.
                if meta_type in SKIP_TYPE:
                    params = {"设计规划": [], "仿真模拟": []}
                    ## 设计规划
                    dkey = "设计规划"
                    # extra
                    if subkey in ["变压器"]:
                        params[dkey].append(wrapper_uc_vp("功率因数", "one"))
                        params[dkey].append(wrapper_uc_vp("变压器冗余系数", "one"))
                    # override
                    if subkey in ["锂电池"]:
                        params[dkey].append(wrapper_uc_vp("初始SOC", "percent"))
                        params[dkey].append("循环边界条件")
                        params[dkey].append(wrapper_uc_vp("最大设备容量", "kWh"))  # 总容量
                        params[dkey].append(
                            wrapper_uc_vp("最小设备容量", "kWh")
                        )  # from excel.
                    elif subkey in ["光伏发电"]:  # solar power.
                        params[dkey].append(wrapper_uc_vp("最大安装面积", "m2"))
                        params[dkey].append(
                            wrapper_uc_vp("最小安装面积", "m2")
                        )  # from excel.
                    elif subkey in ["传输线"]:  # transfer lines, pipes
                        params[dkey].append(wrapper_uc_vp("长度", "km"))
                    else:
                        params[dkey].append(wrapper_uc_vp("最大安装台数", "台"))
                        params[dkey].append(wrapper_uc_vp("最小安装台数", "台"))

                    ## 仿真模拟
                    dkey = "仿真模拟"
                    # extra
                    if subkey in ["变压器"]:
                        params[dkey].append(wrapper_uc_vp("功率因数", "one"))
                    # override
                    if subkey in ["传输线"]:
                        params[dkey].append(wrapper_uc_vp("长度", "km"))
                    else:
                        params[dkey].append(wrapper_uc_vp("安装台数", "台"))

                    params["设计规划"].append("设备选型")  # you may set the calculation mode.
                    params["仿真模拟"].append("设备选型")

                    output_data[key][subkey].update(params)

                    rich.print(params)
                    # str? -> str
                    # tuple -> number with unit
                    # dict -> table
                    # breakpoint()
            else:
                # begin to parse it.
                if val in COMMENT_TYPE:
                    continue

                result = parse.parse("{val_name}({val_unit})", val)
                if result:
                    val_name, val_unit = (
                        result["val_name"].strip(),
                        result["val_unit"].strip(),
                    )
                else:
                    val_name = val
                    val_unit = None

                if meta_type in SKIP_TYPE:
                    # TODO: checking metadata.
                    continue
                elif val_name in TRANSLATION_TABLE.keys():
                    has_exception, uc = getUnitConverted(val_name, val_unit)
                    # base_classes = TRANSLATION_TABLE[val_name]
                    # has_exception = False
                    # for base_class in base_classes:
                    #     default_unit = BASE_CLASS_TO_UNIT_TABLE[base_class]
                    #     # iterate through all base classes.
                    #     print("DEFAULT UNIT:", default_unit)
                    #     default_unit_real = ureg.Unit(default_unit)
                    #     default_unit_compatible = ureg.get_compatible_units(
                    #         default_unit_real
                    #     )
                    #     print("TRANS {} -> {}".format(val_name, base_class))
                    #     if val_unit:
                    #         for (
                    #             trans_source_unit,
                    #             trans_target_unit,
                    #         ) in UNIT_TRANSLATION_TABLE.items():
                    #             val_unit = val_unit.replace(
                    #                 trans_source_unit, trans_target_unit
                    #             )
                    #         # parse this unit!
                    #     else:
                    #         val_unit = default_unit
                    #         print("USING DEFAULT UNIT")
                    #     print("UNIT", val_unit)
                    #     unit = ureg.Unit(val_unit)
                    #     compatible_units = ureg.get_compatible_units(val_unit)
                    #     # print("COMPATIBLE UNITS", compatible_units)
                    #     if not default_unit_compatible == compatible_units:
                    #         has_exception = True
                    #         print(
                    #             "Unit {} not compatible with default unit {}".format(
                    #                 val_unit, default_unit
                    #             )
                    #         )
                    #         continue
                    #     else:
                    #         # get factor:
                    #         mag, standard = unitFactorCalculator(
                    #             ureg, standard_units, val_unit
                    #         )
                    #         print("STANDARD:", standard)
                    #         print("MAGNITUDE TO STANDARD:", mag)
                    #         has_exception = False
                    #         break
                    if has_exception:
                        raise Exception(f"No compatibie unit found for {val_name}")
                        # raise Exception(f"No compatibie unit found for {val_unit}")
                    else:

                        v_param = getValueParam(uc, val_name)
                        if val_is_table:
                            (_, _, _, standard) = uc
                            print("TABLE VALUE:", val_name, standard)
                            table_format = get_table_format(  # 基本上都是负载率
                                val_name, standard
                            )  # unit vs

                            t_name, t_unit = table_format

                            has_exception, t_uc = getUnitConverted(t_name, t_unit)

                            if has_exception:
                                raise Exception(
                                    "No table format found for:", val_name, val_unit
                                )

                            t_param = getValueParam(t_uc, t_name)
                            new_param = {"MAIN": v_param, "SUB": t_param}
                            # new_param = {v_param: t_param}
                            # (name, original_name, original_unit, standard_unit, magnitude)
                        else:
                            # normal values.
                            new_param = v_param
                        output_data[key][subkey]["设备参数"].append(new_param)
                else:
                    raise Exception("Unknown Value:", val)

print()
rich.print(output_data)

# write documents for api?
# or just a whole bunch of generated documents inserted into places?
output_path = "microgrid_jinja_param_base.json"
with open(output_path, "w+") as f:
    f.write(json.dumps(output_data, indent=4, ensure_ascii=False))

print("SAVED TO:", output_path)
