encoding='utf-8'
template_path = "cloudpss_model_template.py.j2"
template = open(template_path,'r',encoding=encoding).read()

from jinja2 import Environment,FileSystemLoader
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
from typing import Union

def convertToStandardUnit(unit:Union[str,None]):
    factor_string = ""
    # times factor, not division!
    return unit_hint, factor_string

import re

mylist =[]

for key, value in excelMap.items():
    if type(value) == dict:
        if "生产厂商" in value.keys():  # with or without unit?
            mylist_elem = []
            mylist_dict_elem = {key: [] for key in ["设备额定运行参数","设备运行约束","设备经济性参数","设备工况"]}

            print("DEVICE NAME:", key)
            mylist_elem.append(key)
            # this is a device for sure.
            # rich.print(value)
            for k, v in value.items():
                if type(v) == str:
                    if v.split(".")[0] in dataParams.keys():
                        k0 = dataParams[v.split(".")[0]]
                        print(k0, k, v.split(".")[-1])
                        pattern = r'(\w+)\((\w+)\)'
                        result = re.findall(pattern, k)
                        if len(result) > 0:
                            value_name, unit = result[0]
                            print(f"value_name={value_name}\nunit={unit}")
                        else:
                            value_name=result
                            unit = None
                            print(f"value_name={value_name}")
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
    env = Environment(loader = FileSystemLoader('./'))
    tpl = env.get_template(template_path)
    
    with open(output_path,'w+',encoding=encoding) as fout:

        render_content = tpl.render(mylist = mylist)
        # render_content = tpl.render(mylist = ["光伏","风机","燃气轮机"])
        fout.write(render_content)
        # render_content1 = tpl.render(mylist2=[("单个光伏板面积","单位：(m²)",""),("最大发电功率","单位：(kW)",""),"采购成本","单位：(万元/台)","固定维护成本","单位：(万元/年)","可变维护成本","单位：(万元/kWh) <- (元/kWh)","设计寿命","单位：(年)"])
        # fout.write(render_content1)
if __name__ == '__main__':
    main()

