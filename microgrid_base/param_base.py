import json


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


frontend_translation_table = read_json("frontend_sim_param_translation.json")

type_sys = {
    "类型分类表": read_json("microgrid_v2_all_types_structured.json"),  # （不包含设备名称）分类->能源->类型
    "连接类型映射表": read_json("microgrid_v2_connectivity_matrix.json"),  # "端点1_端点2"->生成连接类型
    "设备锚点类型表": read_json(
        "microgrid_v2_device_port_type_mapping.json"
    ),  # 设备分类->设备名称->锚点名称->锚点类型
}

dparam_path = "microgrid_jinja_param_base.json"
dparam = read_json(dparam_path)


类型集合分类 = [
    (mkey.replace("设备", "锚点"), [e for (k, v) in mdata.items() for e in v])
    for mkey, mdata in type_sys["类型分类表"].items()
]

类型集合分类.append(
    ("设备", [dev for cat, devs in type_sys["设备锚点类型表"].items() for dev in devs.keys()])
)

设备接口集合 = {
    dev_name: set([(port_name, port_type) for port_name, port_type in ports.items()])
    for cat0, devs in type_sys["设备锚点类型表"].items()
    for dev_name, ports in devs.items()
}
#########################
# rich.print(设备接口集合)
# breakpoint()
#########################
连接类型映射表 = {
    frozenset((c1, c2)): c
    for (c1, c2), c in [(k.split("_"), v) for k, v in type_sys["连接类型映射表"].items()]
}

设备库 = []

for super_class, v0 in dparam.items():
    for class_name, v1 in v0.items():
        mstrs = []
        mdigits = []
        mtables = []
        for param_super_class, v2 in v1.items():
            # if param_super_class == "仿真模拟":
            #     continue
            for item in v2:
                if item == "设备选型":
                    continue
                else:
                    if type(item) == str:
                        mstrs.append((param_super_class, item))
                    elif type(item) == list:
                        mdigits.append((param_super_class, item))
                    elif type(item) == dict:
                        main = item["MAIN"]
                        sub = item["SUB"]
                        mtables.append((param_super_class, main, sub))
        设备库.append((super_class, class_name, mstrs, mdigits, mtables))
