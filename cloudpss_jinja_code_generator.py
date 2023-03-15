encoding='utf-8'
template = open("cloudpss_model_template.py.j2",'r',encoding=encoding).read()

from jinja2 import Environment,FileSystemLoader
import jinja2
import json
import rich

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

for key, value in excelMap.items():
    if type(value) == dict:
        if "生产厂商" in value.keys():  # with or without unit?
            print("DEVICE NAME:", key)
            # this is a device for sure.
            # rich.print(value)
            for k, v in value.items():
                if type(v) == str:
                    if v.split(".")[0] in dataParams.keys():
                        k0 = dataParams[v.split(".")[0]]
                        print(k0, k, v.split(".")[-1])
                    else:
                        if v not in ["manufacturer", "equipType"]:
                            print(">> UNIDENTIFIED PARAM TYPE <<")
                        print(k, v)
                else:
                    print(">> UNIDENTIFIED VALUE TYPE <<")
                    print(k, type(v), v)
        elif "负荷名称" in value.keys():  # load for sure.
            for k, v in value.items():
                ...
        print("_" * 30)
def main():
    env = Environment(loader = FileSystemLoader('./'))
    tpl = env.get_template('jinja_test.j2')
    
    with open('page.txt','w+') as fout:
        render_content = tpl.render(mylist = ["光伏",2,3])
        fout.write(render_content)
output_path = "cloudpss_jinja_code_output.py"

#### GENERATE CODE, WRITE TO output_path, with encoding='utf-8'

