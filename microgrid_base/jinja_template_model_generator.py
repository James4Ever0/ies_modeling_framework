# serialized connectivity matrix -> connectivity matrix -> verify matrix -> calculation model -> calculate

# to generate the serialized connectivity matrix, you need structures.

# the test code may not be generated.
import json


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


type_sys = {
    "类型分类表": read_json("microgrid_v2_all_types_structured.json"),  # （不包含设备名称）分类->能源->类型
    "连接类型映射表": read_json("microgrid_v2_connectivity_matrix.json"),  # "端点1_端点2"->生成连接类型
    "设备锚点类型表": read_json(
        "microgrid_v2_device_port_type_mapping.json"
    ),  # 设备分类->设备名称->锚点名称->锚点类型
}

dparam_path = "microgrid_jinja_param_base.json"
dparam = read_json(dparam_path)


def code_and_template_path(base_name):
    code_path = f"{base_name}.py"
    template_path = f"{code_path}.j2"
    return code_path, template_path


topo_code_output_path, topo_code_template_path = code_and_template_path("topo_check")

ies_optim_code_output_path, ies_optim_code_template_path = code_and_template_path(
    "ies_optim"
)

import jinja2


def load_template(template_path):
    try:
        assert template_path.endswith(".j2")
    except:
        Exception(f"jinja template path '{template_path}' is malformed.")
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("./"),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=jinja2.StrictUndefined,
    )
    tpl = env.get_template(template_path)
    return tpl


tpl = load_template(topo_code_template_path)
设备接口集合 = {set((k, v)) for _, d in type_sys["设备锚点类型表"].items() for k, v in d.items()}
import rich
rich.print(设备接口集合)
breakpoint()
连接类型映射表 = {
    frozenset((c1, c2)): c
    for (c1, c2), c in [(k.split("_"), v) for k, v in type_sys["连接类型映射表"].items()]
}
result = tpl.render(type_sys=type_sys, 设备接口集合=设备接口集合, 连接类型映射表=连接类型映射表)
print()
print("______________________[{}]".format("TOPO CHECK CODE"))
print(result)

with open(topo_code_output_path, "w+") as f:
    f.write(result)

# tpl = load_template(ies_optim_code_output_path)
# result = tpl.render(type_sys=type_sys, dparam=dparam)
# print()
# print("______________________[{}]".format("IES CODE"))
# print(result)

# with open(ies_optim_code_output_path, "w+") as f:
#     f.write(result)
