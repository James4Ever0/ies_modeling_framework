from log_utils import logger_print

# serialized connectivity matrix -> connectivity matrix -> verify matrix -> calculation model -> calculate

# to generate the serialized connectivity matrix, you need structures.

from jinja_utils import *
import constants

constants_dict = {k: v for k, v in constants.__dict__.items() if not k.startswith("_")}
# the test code may not be generated.
from param_base import *
from render_type_utils import *

# topo_code_output_path, topo_code_template_path = code_and_template_path("topo_check_v1")
topo_code_v2_output_path, topo_code_v2_template_path = code_and_template_path(
    "topo_check_v2"
)

ies_optim_code_output_path, ies_optim_code_template_path = code_and_template_path(
    "ies_optim"
)

MAKEFILE = dict(
    inputs=[
        topo_code_v2_template_path,
        ies_optim_code_template_path,
        (PEF := "planning_export_format.json"),
        TYPE_UTILS_MICROGRID_PORTS,
        TYPE_UTILS_EXTRA_PORTS,
    ],
    outputs=[topo_code_v2_output_path, ies_optim_code_output_path],
    args=[],
)

import json


# delegate consistency checks to type utils. (not implemented yet)
# make portname mappings being used in topo parsing & modeling
# migrate to topo_check_v2

with open(PEF, "r") as f:
    planningExportFormat = json.loads(f.read())

if __name__ == "__main__":
    # you need to stop rendering it here.

    # TYPE_UTILS_MICROGRID_PORTS_DATA
    # TYPE_UTILS_EXTRA_PORTS_DATA

    设备类型 = []
    设备接口名称集合 = {}
    directionTranslationTable = dict(进="输入", 出="输出", 进出="输入输出")
    directionLookupTable = {}
    for dat in [TYPE_UTILS_MICROGRID_PORTS_DATA, TYPE_UTILS_EXTRA_PORTS_DATA]:
        for supertype, devDict in dat.items():
            for deviceTypeName, devData in devDict.items():
                设备类型.append(deviceTypeName)
                ports = devData["ports"]
                portNames = ports.keys()
                设备接口名称集合[deviceTypeName] = set(portNames)
                portDirectionLookupTable = {}
                for portName, portDef in ports.items():
                    energyFlowDirection = portDef["能流方向"]
                    direction = directionTranslationTable[energyFlowDirection]
                    portDirectionLookupTable[portName] = direction
                directionLookupTable[deviceTypeName] = portDirectionLookupTable
    topo_check_v2_render_params = dict(
        设备类型=设备类型, 设备接口名称集合=设备接口名称集合, directionLookupTable=directionLookupTable
    )

    load_render_and_format(
        template_path=topo_code_v2_template_path,
        output_path=topo_code_v2_output_path,
        render_params=topo_check_v2_render_params,
        banner="TOPO CHECK CODE V2",
    )

    # load_render_and_format(
    #     template_path=topo_code_template_path,
    #     output_path=topo_code_output_path,
    #     render_params=dict(类型集合分类=类型集合分类, 设备接口集合=设备接口集合, 连接类型映射表=连接类型映射表),
    #     banner="TOPO CHECK CODE",
    # )

    planningExportFormatList = list(planningExportFormat.items())
    planningExportFormatList.sort(key=lambda x: 0 if x[0] == "方案详情" else 1)

    render_params = dict(
        设备库=设备库,
        设备接口集合=设备接口集合, # if you want more device models, you have to change here, maybe.
        # but at least you can pass the topology check now, even if with extra non-existant models.
        frontend_translation_table=frontend_translation_table,
        planningExportFormatList=planningExportFormatList,
        **constants_dict,
        constants=constants_dict,
    )
    load_render_and_format(
        template_path=ies_optim_code_template_path,
        output_path=ies_optim_code_output_path,
        render_params=render_params,
        banner="IES OPTIM CODE",
    )

    # test(["test_topo_check.py", "-f"])

    # run test code.
    test(["test_topo_check.py"])

    # tpl = load_template(ies_optim_code_output_path)
    # result = tpl.render(type_sys=type_sys, dparam=dparam)
    # logger_print()
    # logger_print("______________________[{}]".format("IES CODE"))
    # logger_print(result)

    # with open(ies_optim_code_output_path, "w+") as f:
    #     f.write(result)
