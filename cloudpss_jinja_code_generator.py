encoding = "utf-8"
template_path = "cloudpss_model_template.py.j2"
template = open(template_path, "r", encoding=encoding).read()

from jinja2 import Environment, FileSystemLoader

# import jinja2
import json

# import rich

load_path = "cloudpss_inputs.json"

with open(load_path, "r", encoding="utf-8") as f:
    data = json.loads(f.read())
    # rich.print(data)

excelMap = data["excelMap"]

dataParams = {
    "ratedParam": "设备额定运行参数",
    "operationalConstraints": "设备运行约束",
    "economicParam": "设备经济性参数",
    "OperateParam": "设备工况",
}

# 设备额定运行参数
# 设备运行约束
# 设备经济性参数
# 设备工况

# unknown property:
# 燃气轮机 -> 挡位 -> dict ({"route": "OperateParams.params"})
# 这个参数没有用于建模仿真或者优化
from pint_convert_units import unitFactorCalculator
from typing import Union, List
from pint import UnitRegistry
from functools import lru_cache


@lru_cache(maxsize=1)
def getUnitRegistryAndStandardUnits(
    unit_definition_file_path: str = "merged_units.txt",
    standard_units_name_list: List[str] = [
        "万元",
        "kWh",
        "km",
        "kW",
        "年",
        "MPa",
        "V",
        "Hz",
        "ohm",
        "one",
        '台'
    ],
):
    ureg = UnitRegistry(unit_definition_file_path)
    standard_units = frozenset(
        [ureg.Unit(unit_name) for unit_name in standard_units_name_list]
    )
    return ureg, standard_units


@lru_cache(maxsize=1)
def getStandardUnits():
    standard_units = frozenset([])
    return standard_units


def convertToStandardUnit(unit: Union[str, None]):
    factor_string = unit_hint = ""
    # times factor, not division!
    # numeric_conversion_dict = {"percent": 0.01}
    if unit:
        unit = unit.replace("%", 'percent').replace("m²",'m2')
        # if unit in numeric_conversion_dict.keys():
        #     unit_hint = f"([]) <- ({unit})"
        #     factor_string = f" * {numeric_conversion_dict[unit]}"
        ureg, standard_units = getUnitRegistryAndStandardUnits()
        try:
            unit_hint = f"({str(ureg.Unit(unit))})"
        except:
            raise Exception("Invalid unit string:", unit)
        new_magnitude, new_unit_name = unitFactorCalculator(
            ureg, standard_units=standard_units, old_unit_name=unit
        )
        if new_magnitude != 1:
            unit_hint = f"({new_unit_name}) <- {unit_hint}"
            factor_string = f" * {new_magnitude}"
    return unit_hint, factor_string


import re

mylist = []

for key, value in excelMap.items():
    if type(value) == dict:
        if "生产厂商" in value.keys():  # with or without unit?
            mylist_elem = []
            mylist_dict_elem = {
                key: [] for key in ["设备额定运行参数", "设备运行约束", "设备经济性参数", "设备工况"]
            }

            print("DEVICE NAME:", key)
            mylist_elem.append(key)
            # this is a device for sure.
            # rich.print(value)
            for k, v in value.items():
                if type(v) == str:
                    if v.split(".")[0] in dataParams.keys():
                        k0 = dataParams[v.split(".")[0]]
                        print("K0", k0, "K", k, "V", v.split(".")[-1])
                        value_name = k.split("(")[0]
                        unit = k.replace(value_name, "").strip()
                        if unit.startswith("(") and unit.endswith(")"):
                            unit = unit[1:-1].strip()
                            if len(unit) == 0:
                                raise Exception("Invalid Unit:", unit)
                        else:
                            if len(unit) > 0:
                                raise Exception("Invalid Unit:", unit)
                            else:
                                unit = None
                        # pattern = r"(\w+)\((\w+)\)"
                        # result = re.findall(pattern, k)
                        # if len(result) > 0:
                        #     value_name, unit = result[0]
                        #     print(f"value_name={value_name}\nunit={unit}")
                        # else:
                        #     value_name = k
                        #     unit = None
                        #     print(f"value_name={value_name}")
                        # return value_name, unit
                        unit_hint, factor = convertToStandardUnit(unit)
                        comment = f"单位：{unit_hint} {k0}" if unit else f"{k0}"
                        melem = [value_name, comment, factor]
                        mylist_dict_elem[k0].append(melem)
                    else:
                        if v not in ["manufacturer", "equipType"]:
                            print(">> UNIDENTIFIED PARAM TYPE <<")
                        print(k, v)
                else:
                    print(">> UNIDENTIFIED VALUE TYPE <<")
                    print(k, type(v), v)
            mylist_elem.append(mylist_dict_elem)
            mylist.append(mylist_elem)
        elif "负荷名称" in value.keys():  # load for sure.
            for k, v in value.items():
                ...
        print("_" * 30)


output_path = "cloudpss_jinja_code_output.py"


#### GENERATE CODE, WRITE TO output_path, with encoding='utf-8'
def main():
    env = Environment(loader=FileSystemLoader("./"))
    tpl = env.get_template(template_path)

    with open(output_path, "w+", encoding=encoding) as fout:
        render_content = tpl.render(mylist=mylist)
        # render_content = tpl.render(mylist = ["光伏","风机","燃气轮机"])
        fout.write(render_content)
        # render_content1 = tpl.render(mylist2=[("单个光伏板面积","单位：(m²)",""),("最大发电功率","单位：(kW)",""),"采购成本","单位：(万元/台)","固定维护成本","单位：(万元/年)","可变维护成本","单位：(万元/kWh) <- (元/kWh)","设计寿命","单位：(年)"])
        # fout.write(render_content1)


if __name__ == "__main__":
    main()
