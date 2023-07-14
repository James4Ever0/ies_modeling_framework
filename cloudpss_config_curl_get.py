sources_curl_get = dict(simu="cloudpss_simu.mjson",optim="cloudpss_optim.mjson", )
# almost the same as `cloudpss_config2.py`, with slight alternation.
# choice = "optim"
choices = sources_curl_get.keys()

param_translate_maps = dict(
    simu=dict(
        参数分类=[],
        中文名称=[],  # create it later. join with "/"
        有关设备=[],  # join with ", "
    ),
    optim=dict(参数分类=[], 中文名称=[], 有关设备=[]),
)

prelude = """
# 建模仿真和规划设计的输入参数和区别

规划设计在设备信息库内添加了经济性参数，而建模仿真对某些设备将额定工况变为了多工况的输入。
<br><br>根据布尔表达式，有的输入项所填写的值决定其他参数是否能够填写。
<br><br>下面介绍在能流拓扑图中两种模式的输入项区别：

"""

print(prelude)

simu_format_string = """

## 建模仿真参数

### 参数分类

{table}

#### 基础参数
要指定设备台数
#### 仿真参数
配电传输设备除模块化多电平变流器都不具备仿真参数，及管道、采暖制冷负荷、电负荷都不具备
#### 优化参数
具备优化参数的设备可选是否优化，部分设备优化参数具有其他参数，例如柔性电负荷的最大负荷
#### 运行约束
采暖制冷负荷具备运行约束，供热/制冷最大、最小出口温度。

### 详细说明

{detail}
"""

optim_format_string = """
## 规划设计参数

{table}

### 机组参数
在没有选择具体设备时，不能指定设备台数，但可以指定设备额定运行参数。指定了设备类型时，可以指定设备台数，但是不能指定额定运行参数。
部分参数
### 运行参数组
不能指定部分参数，或者可选指定部分参数
### 计算参数组
有的设备没有计算参数组，例如吸收式制冷机，余热锅炉
### 负荷设置
负荷元件特有的设置

### 详细说明

{detail}
"""

format_strings = {"simu": simu_format_string,"optim": optim_format_string, }


import json
import pandas as pd

print_list = []
def append_candidate(*args):
    global print_list
    if len(args) == 0:
        print_list.append("")
    else:
        print_list.append(" ".join(args))

for choice in choices:
    mjson_path = sources_curl_get[choice]

    # question: convert pandas dataframe to markdown table.
    headliner = lambda level: "#" * level

    with open(mjson_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    level_shift = 1

    param_class_name_dict = {}

    existing_keys = []
    for line in lines:
        try:
            data = json.loads(line.strip())
            param = data["ele"]["param"]
            key_prefix = name = param["name"]

        except:
            # obviously we've hit something hard.
            continue
        if key_prefix not in existing_keys:
            existing_keys.append(key_prefix)

            append_candidate()
            append_candidate(headliner(level_shift + 2), key_prefix)
            append_candidate()

            append_candidate(headliner(level_shift + 3), "设备信息")
            append_candidate()

            info_keys = [
                "classname",
                "name",
                "type",
                "thutype",
                "ver",
                "id",
                "sym",
            ]

            info_markdown = pd.DataFrame([{k: param[k] for k in info_keys}]).to_html()
            append_candidate(info_markdown)
            append_candidate()

            pin = [v for _, v in param["pin"].items()]  # iterate through keys.
            pin_df = pd.DataFrame(pin)
            append_candidate(headliner(level_shift + 3), "针脚定义")
            append_candidate()
            append_candidate(pin_df.to_html())
            # you can also get conditional pins and connection types.
            existing_keys = []

            append_candidate()
            append_candidate(headliner(level_shift + 3), "参数填写")
            # shall create this table for every device.
            params = param["param"]
            input_types = list(params.keys())
            for input_type in input_types:
                if input_type not in param_class_name_dict.keys():
                    param_class_name_dict[input_type] = {
                        "chinese_names": set(),
                        "related_devices": [],
                    }
                component_info = []
                input_data = params[input_type]

                param_class_name_dict[input_type]["chinese_names"].add(
                    input_data["desc"]
                )
                param_class_name_dict[input_type]["related_devices"].append(key_prefix)

                for k, v in input_data["params"].items():
                    valDict = {"ID": k}
                    valDict.update({k0: v0 for k0, v0 in v.items()})
                    component_info.append(valDict)

                df = pd.DataFrame(component_info)
                append_candidate()
                append_candidate(headliner(level_shift + 4), input_type)
                append_candidate()
                markdown_table = df.to_html(index=False)
                append_candidate(markdown_table)
        else:
            continue
        append_candidate()

    param_translate_maps[choice]["参数分类"] = list(param_class_name_dict.keys())
    param_translate_maps[choice]["中文名称"] = [
        ", ".join(param_class_name_dict[k]["chinese_names"])
        for k in param_translate_maps[choice]["参数分类"]
    ]
    param_translate_maps[choice]["有关设备"] = [
        ", ".join(param_class_name_dict[k]["related_devices"])
        for k in param_translate_maps[choice]["参数分类"]
    ]

    table = pd.DataFrame(param_translate_maps[choice]).to_html(index=False)
    
    detail = "\n".join(print_list)
    
    formatted_string = format_strings[choice].format(table=table, detail=detail)
    print(formatted_string)
    
    print_list = []