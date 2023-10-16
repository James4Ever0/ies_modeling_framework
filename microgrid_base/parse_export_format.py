from log_utils import logger_print

excel_path = "设备信息库各参数_10_12.xlsx"
# excel_path = "设备信息库各参数.xlsx"
from lib_parse_params import repair_excel

repair_excel(excel_path)
from jinja_utils import code_and_template_path, load_render_and_format
import rich
import re

from constants import *

code_path, template_path = code_and_template_path("export_format_validate")

code_unit_path, template_unit_path = code_and_template_path(
    "export_format_units"
)  # TODO: mark this as dependency as "ies_optim.py"

# you may also need to render some other code to avoid circular importing issues.


设计规划结果输出CSV = "设备信息库各参数-规划方案及详情.csv"  # parse this thing first.

output_path = "export_format.json"

planning_output_path = f"planning_{output_path}"

MAKEFILE = dict(
    inputs=[template_path, template_unit_path, excel_path, 设计规划结果输出CSV],
    outputs=[output_path, code_path, code_unit_path, planning_output_path],
    args=[],
)

import json

# from os import name
import pandas

# --------------------------- #
#   设计规划导出数据格式准备    #
# --------------------------- #

设计规划结果输出格式表格 = pandas.read_csv(
    设计规划结果输出CSV, on_bad_lines="warn", header=None
)  # you can ignore bad lines.

# logger_print(设计规划结果输出格式表格)
# breakpoint()
subSchemas = []
# breakpoint()

for colIndex in (设计规划T := 设计规划结果输出格式表格.T):
    firstElem = (col := 设计规划T[colIndex].to_list())[0]
    if (
        isinstance(firstElem, str)
        and not isinstance(col[1], str)
        and len(firstElem) == 4
        and firstElem.startswith("方案")
    ):
        # logger_print(firstElem)
        # breakpoint()
        subSchemas.append((firstElem, colIndex))

planningResultSchema = {schemaName: {} for schemaName, _ in subSchemas}

from unit_utils import unitParserWrapper

# need to remove few terms before saving to disk.
removeTermRegexes = {
    "方案列表": [r"年平均.+", "方案名称"],  # use non-greedy modifier (backtracking)
    "方案详情": ["能源消耗费用", r"年.+?收入", "出力曲线"],
}
hitRecords = {k: {e: False} for k, v in removeTermRegexes.items() for e in v}
from typing import List


def checkIfMatchAListOfRegexes(term: str, regexList: List[str], key: str):
    for regex in regexList:
        if re.match(regex, term):
            hitRecords[key][term] = True
            return True
    return False


def getSchemaType(schemaHeader, schemaHeaderUnit):
    if schemaHeaderUnit:
        return "float"
    else:
        if schemaHeader in ["数量"]:
            return "int"
        elif schemaHeader in ["平均效率_平均COP"]:
            return "float"
        else:
            return "str"


for schemaName, index in subSchemas:  # why we have nan here?
    regexList = removeTermRegexes[schemaName]
    # Assignment expressions within a subscript are supported only in Python 3.10 and newer
    schemaHeaderIndex = index + 1
    schemaHeaders = 设计规划T[schemaHeaderIndex].to_list()
    # schemaHeaders = 设计规划T[schemaHeaderIndex := index + 1].to_list()
    # logger_print(schemaHeaders)
    # breakpoint()
    englishSchemaHeaderIndex = schemaHeaderIndex + 2

    englishSchemaHeaders = 设计规划T[
        englishSchemaHeaderIndex
        # englishSchemaHeaderIndex := schemaHeaderIndex + 2
    ].to_list()
    # breakpoint()
    # 去除了自来水消耗
    remove_isna = lambda it: filter(lambda e: not pandas.isna(e), it)
    for schemaHeader, englishSchemaHeader in zip(
        remove_isna(schemaHeaders), remove_isna(englishSchemaHeaders)
    ):
        schemaHeader = schemaHeader.replace("/", "_")  # for code generation
        strippedSchemaHeader, schemaHeaderUnit = unitParserWrapper(schemaHeader)
        if checkIfMatchAListOfRegexes(strippedSchemaHeader, regexList, schemaName):
            logger_print("SKIPPING:", strippedSchemaHeader)
            continue
        planningResultSchema[schemaName].update(
            {
                strippedSchemaHeader: {
                    "unit": schemaHeaderUnit,  # could be "None"
                    "englishName": englishSchemaHeader,
                    "type": getSchemaType(schemaHeader, schemaHeaderUnit),
                }
            }
        )

# check if all regexes have hits.
errors = []
for k, v in hitRecords.items():
    for e in v:
        if e is False:
            errors.append(f"Error: regex {e.__repr__()} with no match!")

if errors:
    raise Exception("\n".join(errors))

logger_print(planningResultSchema)
# breakpoint()
# store this to file. remember to mention this file in Makefile. automation tools like "dyndep" in ninja, or "submake" can be used.
with open(planning_output_path, "w+") as f:
    f.write(json.dumps(planningResultSchema, indent=4, ensure_ascii=False))

# -------------------------- #

table_name = "仿真结果"

table = pandas.read_excel(excel_path, sheet_name=table_name, header=None)


# logger_print(table)
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
        # breakpoint()
        last_empty_index = len(rlist)
        try:
            last_empty_index = rlist.index("")
        except:
            pass
        headings = rlist[:last_empty_index]
        trough = 2
        data[key] = data.get(key, []) + [{"headings": headings, "devices": []}]


# need processing.
logger_print(data)


logger_print("writing to:", output_path)

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
            logger_print("processing:", elem_name)
            mag, new_unit_name = unitFactorCalculator(
                ureg, standard_units, old_unit_name
            )
            unit = (mag, new_unit_name, old_unit_name)

        result_mapping[elem_name] = unit
    return result_mapping


new_data["仿真结果"]["ALL"] = convert_format(data["仿真结果"][0]["headings"])
from param_base import 设备接口集合

all_device_names = list(设备接口集合.keys())

logger_print()
logger_print(all_device_names)

# 外部能源 & 负荷类型
nonDevNames = ["柴油", "电负荷", "氢负荷", "冷负荷", "热负荷", "蒸汽负荷", "市政自来水", "天然气", "电网", "氢气"]
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
    "产热量": ["电解槽"],
    "热负荷": [],
    "产电量": ["光伏发电", "风力发电", "柴油发电"],
    "电负荷": ["电负荷", "电解槽"],
    "蒸汽产量": [],
    "蒸汽负荷": [],
    "氢气产量": ["电解槽"],
    "氢气消耗量": ["氢负荷"],
    "柴油消耗量": ["柴油发电", "柴油"],
    "柴油消耗费用": ["柴油"],
    "天然气消耗量": [],
    "天然气消耗费用": [],
    "平均效率/平均COP": ["柴油发电", "传输线", "变压器", "锂电池", "变流器", "双向变流器"],
    "冷收入": [],
    "热收入": [],
    "电收入": ["电负荷"],
    "蒸汽收入": [],
    "氢气收入": ["氢负荷"],
    "自来水消耗量": [],
    "自来水消耗费用": [],
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

logger_print(df.head())
filepath = "sim_param_export.xlsx"
logger_print(f"writing to: {filepath}")
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


logger_print()
logger_print(new_data)
with open(output_path, "w+") as f:
    f.write(json.dumps(new_data, indent=4, ensure_ascii=False))
logger_print("write to:", output_path)


model_names = [f"{n}模型" for n in all_device_names]

render_params = dict(
    main_data=new_data,
    nonDevNames=nonDevNames,
    nonCountableDevNames=nonCountableDevNames,
    每年小时数=每年小时数,
)
# render_params = dict(model_names=model_names, main_data=new_data)
from copy import deepcopy

load_render_and_format(
    template_path, code_path, deepcopy(render_params), banner="FORMAT_VALIDATE_CODE"
)

load_render_and_format(
    template_unit_path,
    code_unit_path,
    deepcopy(render_params),
    banner="FORMAT_UNIT_CODE",
)
