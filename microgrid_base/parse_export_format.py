excel_path = "设备信息库各参数.xlsx"

from jinja_utils import code_and_template_path, load_render_and_format
import rich

from constants import *

code_path, template_path = code_and_template_path("export_format_validate")

设计规划结果输出CSV = "设备信息库各参数-规划方案及详情.csv"  # parse this thing first.

output_path = "export_format.json"

MAKEFILE = dict(
    inputs=[template_path, excel_path, 设计规划结果输出CSV],
    outputs=[output_path, code_path],
    args=[],
)

import json

# from os import name
import pandas

设计规划结果输出格式表格 = pandas.read_csv(
    设计规划结果输出CSV, on_bad_lines="warn", header=None
)  # you can ignore bad lines.

# rich.print(设计规划结果输出格式表格)
# breakpoint()
subSchemas = []
breakpoint()
for colIndex in enumerate(设计规划T := 设计规划结果输出格式表格.T):
    firstElem = (col := 设计规划T[colIndex].to_list())[0]
    if isinstance(firstElem, str) and len(firstElem) == 4:
        mtable = firstElem
        subSchemas.append((firstElem, colIndex))

planningResultSchema = {schemaName: {} for schemaName, _ in subSchemas}

for schemaName, index in subSchemas:
    schemaHeaders = 设计规划T[schemaHeaderIndex := index + 1].to_list()
    englishSchemaHeaders = 设计规划T[
        englishSchemaHeaderIndex := schemaHeaderIndex + 2
    ].to_list()
    for schemaHeader, englishSchemaHeader in zip(schemaHeaders, englishSchemaHeaders):
        planningResultSchema[schemaName].update(
            {
                strippedSchemaHeader: {
                    "unit": schemaHeaderUnit,
                    "englishName": englishSchemaHeader,
                }
            }
        )
    breakpoint()


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


# need processing.
rich.print(data)


print("writing to:", output_path)

new_data = {k: {} for k in data.keys()}

revmap = {
    "one": ["平均效率/平均COP", "设备台数", "时间"],
    # "万元": ["设备维护费用", "柴油消耗费用"],
    # "kWh": ["电负荷", "产电量"],
}
default_unit_maps = {k: v for v, klist in revmap.items() for k in klist}
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
commonParams = ["元件名称", "元件类型"]
for paramName in commonParams:
    if paramName not in (dictALL := new_data["仿真结果"]["ALL"]).keys():
        dictALL.update({paramName: None})

simDevParam = {name: [] for name in all_device_names}
nonCountableDevNames = ["传输线"]
for k in simDevParam.keys():
    simDevParam[k].extend(commonParams)
    if k not in nonDevNames:
        simDevParam[k].extend(
            [
                e
                for e in commonDevParams
                if (e != "设备台数" if k in nonCountableDevNames else True)
            ]
        )

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
    "柴油消耗量": ["柴油发电", "柴油"],
    "柴油消耗费用": ["柴油"],
    "天然气消耗量": [],
    "天然气消耗费用": [],
    "平均效率/平均COP": ["柴油发电", "传输线", "变压器", "锂电池", "变流器", "双向变流器"],
    "冷收入": [],
    "热收入": [],
    "电收入": ["电负荷"],
    "蒸汽收入": [],
    "氢气收入": [],
}

all_devs_with_uniq_sim_param = [i for k in simParamLUT.values() for i in k]

all_sim_params = list(simParamLUT.keys()) + commonDevParams + commonParams

excel_sim_params = set(new_data["仿真结果"]["ALL"].keys())

assert (setEXC := set(excel_sim_params)) == (
    setALL := set(all_sim_params)
), f"参数不符合:\nEXCEL UNIQ: {setEXC.difference(setALL)}\nCODE UNIQ: {setALL.difference(setEXC)}"
# ), f"参数不符合:\nEXCEL UNIQ: {setEXC.difference(setALL)}\nCODE UNIQ: {setALL.difference(setEXC)}"

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
    for k in sorted(excel_sim_params, key=lambda x: 1 if x != commonParams[0] else 0)
}

import pandas as pd

df = pd.DataFrame(tableRepr, index=None)

print(df.head())
filepath = "sim_param_export.xlsx"
print(f"writing to: {filepath}")
df.to_excel(filepath, index=False)

for d in all_device_names:
    # new_data["仿真结果"][d] = convert_format(simDevParam[d])
    new_data["仿真结果"][d] = {e: new_data["仿真结果"]["ALL"][e] for e in simDevParam[d]}

# type? sum or array.
# unit conversion? divide by conversion rate.
# in unit conversion exception list? check.
# matched to which port?
k = "设备出力曲线"

for elem in data[k]:
    h, dlist = elem["headings"], elem["devices"]
    for d in dlist:
        assert d not in new_data[k].keys(), f"错误：'{d}'在{k}中重复定义"
        new_data[k][d] = convert_format(h)


print()
rich.print(new_data)
with open(output_path, "w+") as f:
    f.write(json.dumps(new_data, indent=4, ensure_ascii=False))
print("write to:", output_path)


model_names = [f"{n}模型" for n in all_device_names]

render_params = dict(
    main_data=new_data,
    nonDevNames=nonDevNames,
    nonCountableDevNames=nonCountableDevNames,
    每年小时数=每年小时数,
)
# render_params = dict(model_names=model_names, main_data=new_data)

load_render_and_format(
    template_path, code_path, render_params, banner="FORMAT_VALIDATE_CODE"
)
