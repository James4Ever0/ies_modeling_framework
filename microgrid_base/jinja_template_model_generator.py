# serialized connectivity matrix -> connectivity matrix -> verify matrix -> calculation model -> calculate

# to generate the serialized connectivity matrix, you need structures.

# the test code may not be generated.

import black
import jinja2
import subprocess

from param_base import *


def load_render_and_format(
    template_path: str, output_path: str, render_params: dict, banner: str
):
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


def code_and_template_path(base_name):
    code_path = f"{base_name}.py"
    template_path = f"{code_path}.j2"
    return code_path, template_path


def load_template(template_path):
    try:
        assert template_path.endswith(".j2")
    except:
        Exception(f"jinja template path '{template_path}' is malformed.")
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("./"),
        extensions=["jinja2_error.ErrorExtension", "jinja2.ext.do"],
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=jinja2.StrictUndefined,
    )
    tpl = env.get_template(template_path)
    return tpl


def test(cmd: list, exec="python3"):
    cmd = [exec] + cmd
    p = subprocess.run(cmd)
    p.check_returncode()


if __name__ == "__main__":

    topo_code_output_path, topo_code_template_path = code_and_template_path(
        "topo_check"
    )

    ies_optim_code_output_path, ies_optim_code_template_path = code_and_template_path(
        "ies_optim"
    )

    load_render_and_format(
        template_path=topo_code_template_path,
        output_path=topo_code_output_path,
        render_params=dict(类型集合分类=类型集合分类, 设备接口集合=设备接口集合, 连接类型映射表=连接类型映射表),
        banner="TOPO CHECK CODE",
    )

    # run test code.
    test(["test_topo_check.py"])

    render_params = dict(设备库=设备库, 设备接口集合=设备接口集合)
    load_render_and_format(
        template_path=ies_optim_code_template_path,
        output_path=ies_optim_code_output_path,
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
