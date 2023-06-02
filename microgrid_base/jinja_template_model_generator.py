# serialized connectivity matrix -> connectivity matrix -> verify matrix -> calculation model -> calculate

# to generate the serialized connectivity matrix, you need structures.

from jinja_utils import *
# the test code may not be generated.
from param_base import *

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
