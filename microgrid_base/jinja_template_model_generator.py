# serialized connectivity matrix -> connectivity matrix -> verify matrix -> calculation model -> calculate

# to generate the serialized connectivity matrix, you need structures.

# the test code may not be generated.
import json

def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)

type_sys_paths = {
    "类型分类表": read_json("microgrid_v2_all_types_structured.json"),  # （不包含设备名称）分类->能源->类型
    "连接类型映射表": read_json("microgrid_v2_connectivity_matrix.json"),  # "端点1_端点2"->生成连接类型
    "设备锚点类型表": read_json("microgrid_v2_device_port_type_mapping.json"),  # 设备分类->设备名称->锚点名称->锚点类型
}

for k, p in type_sys_paths.items():
    