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

topo_code_output_path = "topo_check.py"
topo_code_template_path = "topo_check.py.j2"

import jinja2

def load_template(template_path):
    try:
        assert template_path.endswith(".j2")
    except:
        Exception(f"jinja template path '{template_path}' is malformed.")
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("./"),trim_blocks=True, lstrip_blocks=True, undefined=jinja2.StrictUndefined)
    tpl = env.get_template(template_path)
    return tpl

tpl = load_template(topo_code_template_path)
