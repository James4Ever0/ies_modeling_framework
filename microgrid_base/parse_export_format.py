excel_path = "设备信息库各参数.xlsx"

import json
from os import name
import pandas

table_name = "仿真结果"

table = pandas.read_excel(excel_path, sheet_name=table_name, header=None)

# print(table)
def is_empty(elem):
    if type(elem) is str:
        return elem.strip() == ""
    else:
        return True


trough = 0

data = {}

for i, r in table.iterrows():
    rlist = [(e.strip() if type(e) == str else "") for e in r.tolist()]
    first_elem, second_elem = rlist[0], rlist[1]

    if is_empty(first_elem):
        trough = 0
    elif not is_empty(first_elem) and is_empty(second_elem):
        if trough == 0:
            trough = 1
            key = first_elem
        elif trough == 2:
            device = rlist[0]
            data[key][-1]["devices"].append(device)
    elif not is_empty(first_elem) and not is_empty(second_elem):
        headings = rlist[: rlist.index("")]
        trough = 2
        data[key] = data.get(key, []) + [{"headings": headings, "devices": []}]

import rich

# need processing.
rich.print(data)

output_path = "export_format.json"

print("writing to:", output_path)

new_data = {k: {} for k in data.keys()}

default_unit_maps = {"平均效率/平均COP": "one", "设备台数": "one", "时间": "one"}

# None -> str
from unit_utils import (
    unitCleaner,
    unitParser,
    standard_units,
    unitFactorCalculator,
    ureg,
    translateUnit,
)


def convert_format(h_array):
    result_mapping = {}
    for elem in h_array:
        # elem = elem.strip()
        elem = unitCleaner(elem)
        result = unitParser(elem)
        if result:
            elem_name, unit = result["val_name"], result["val_unit"]
        else:
            elem_name = elem
            unit = default_unit_maps.get(elem, None)
        if unit:
            old_unit_name = translateUnit(unit)
            print("processing:", elem_name)
            mag, new_unit_name = unitFactorCalculator(
                ureg, standard_units, old_unit_name
            )
            unit = (mag, new_unit_name, old_unit_name)

        result_mapping[elem_name] = unit
    return result_mapping


new_data["仿真结果"]["ALL"] = convert_format(data["仿真结果"][0]["headings"])

from param_base import 设备接口集合

all_device_names = list(设备接口集合.keys())

print()
rich.print(all_device_names)

nonDevNames = ["柴油", "电负荷"]
commonDevParams = ["设备型号", "设备台数", "设备维护费用"]
commonParams = ["元件名称"]

simDevParam = {name: [] for name in all_device_names}

for k in simDevParam.keys():
    simDevParam[k].extend(commonParams)
    if k not in nonDevNames:
        simDevParam[k].extend(commonDevParams)

simParamLUT = {
    "产冷量": [],
    "冷负荷": [],
    "产热量": [],
    "热负荷": [],
    "产电量": ["光伏发电", "风力发电", "柴油发电"],
    "电负荷": ["电负荷"],
    "蒸汽产量": [],
    "蒸汽负荷": [],
    "氢气产量": [],
    "氢气消耗量": [],
    "柴油消耗量": ["柴油发电"],
    "柴油消耗费用": ["柴油"],
    "天然气消耗量": [],
    "天然气消耗费用": [],
    "平均效率/平均COP": ["柴油发电", "传输线", "变压器", "锂电池", "变流器", "双向变流器"],
    "冷收入": [],
    "热收入": [],
    "电收入": [],
    "蒸汽收入": [],
    "氢气收入": [],
}

all_devs_with_uniq_sim_param = [i for k in simParamLUT.values() for i in k]

all_sim_params = list(simParamLUT.keys()) + commonDevParams + commonParams

excel_sim_params = set(new_data["仿真结果"]["ALL"].keys())
assert (
    excel_sim_params == set(all_sim_params)
), f"参数不符合:\nEXCEL: {excel_sim_params}\nCODE: {all_sim_params}"

for dev in all_device_names:
    assert dev in all_devs_with_uniq_sim_param, f"'{dev}'没有仿真独有参数"

# simParamLUT.update({"设备维护费用": [d for d in all_device_names if d not in nonDevNames]})

# simDevParam =

for k, vlist in simParamLUT.items():
    for v in vlist:
        simDevParam[v].append(k)

tableRepr = {
    k: [
        ("x" if k in simDevParam[k1] else "") if k != commonParams[0] else k1
        for k1 in simDevParam.keys()
    ]
    for k in sorted(excel_sim_params, key = lambda x: 1 if x != commonParams[0]  else 0)
}

import pandas as pd

df = pd.DataFrame(tableRepr, index=None)

print(df.head())
filepath ="sim_param_export.xlsx"
print(f"writing to: {filepath}")
df.to_excel(filepath)

for d in all_device_names:
    new_data["仿真结果"][d] = convert_format(simDevParam[d])


print()
rich.print(new_data)
with open(output_path, "w+") as f:
    f.write(json.dumps(new_data, indent=4, ensure_ascii=False))

# type? sum or array.
# unit conversion? divide by conversion rate.
# in unit conversion exception list? check.
# matched to which port?
