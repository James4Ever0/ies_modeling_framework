# serialized connectivity matrix -> connectivity matrix -> verify matrix -> calculation model -> calculate

# to generate the serialized connectivity matrix, you need structures.

# the test code may not be generated.
import json
from numpy import append
import rich
import black


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
        loader=jinja2.FileSystemLoader("./"),extensions=['jinja2_error.ErrorExtension', 'jinja2.ext.do'],
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=jinja2.StrictUndefined,
    )
    tpl = env.get_template(template_path)
    return tpl


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


def load_render_and_format(template_path: str, output_path:str,render_params: dict, banner: str):
    tpl = load_template(template_path)
    result = tpl.render(**render_params)

    print()
    print("______________________[{}]".format(banner))
    print(result)

    # import black.Mode
    with open(output_path, "w+") as f:
        f.write(result)
    try:
        result = black.format_str(result, mode=black.Mode())
        with open(output_path, "w+") as f:
            f.write(result)
        print("Syntax Ok.")
    except:
        import traceback

        traceback.print_exc()
        raise Exception("Syntax Failed.")
    print("=" * 40)


load_render_and_format(
    template_path=topo_code_template_path,
    output_path = topo_code_output_path, 
    render_params=dict(类型集合分类=类型集合分类, 设备接口集合=设备接口集合, 连接类型映射表=连接类型映射表),
    banner="TOPO CHECK CODE",
)

import subprocess


def test(cmd: list, exec="python3"):
    cmd = [exec] + cmd
    p = subprocess.run(cmd)
    p.check_returncode()


# run test code.
test(["test_topo_check.py"])

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
                        mstrs.append((param_super_class,item))
                    elif type(item) == list:
                        mdigits.append((param_super_class,item))
                    elif type(item) == dict:
                        main = item['MAIN']
                        sub = item['SUB']
                        mtables.append((param_super_class,main, sub))
        设备库.append((super_class, class_name, mstrs, mdigits, mtables))

render_params = dict(设备库=设备库, 设备接口集合=设备接口集合)
load_render_and_format(
    template_path=ies_optim_code_template_path,
    output_path = ies_optim_code_output_path,
    render_params=render_params,
    banner="IES OPTIM CODE",
)

# test(["test_topo_check.py", "-f"])

# tpl = load_template(ies_optim_code_output_path)
# result = tpl.render(type_sys=type_sys, dparam=dparam)
# print()
# print("______________________[{}]".format("IES CODE"))
# print(result)

# with open(ies_optim_code_output_path, "w+") as f:
#     f.write(result)
