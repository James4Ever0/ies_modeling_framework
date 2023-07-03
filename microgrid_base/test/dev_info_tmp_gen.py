# fpath = "device_info.yml.tmp"

import yaml
import sys
import rich

sys.path.append("../")
import jinja_utils
import ies_optim
import inspect

# import copy

exportData = {}


for k, v in ies_optim.__dict__.items():
    # for k, v in mglobals.items():
    # print(k)
    # print(k.__annotations__)
    if k == "计算参数":
        sig = inspect.signature(v)
        commonParams = {}
        for sigkey in sig.parameters.keys():
            commonParams[sigkey] = None
        exportData[k] = commonParams
        # breakpoint()
    elif k.endswith("信息") and (not k.startswith("设备")):
        if issubclass(v, ies_optim.设备基础信息):
            devName = k.strip("信息")
            commonParams = dict(设备名称=devName)
            if issubclass(v, ies_optim.设备信息):
                # 意味着有公共内容
                commonParams.update(生产厂商="Any", 设备型号=f"{devName}1")
            sig = inspect.signature(v)
            # print(sig)
            # breakpoint()
            print()
            print(devName.center(30, "="))
            for sigkey in sig.parameters.keys():
                # print(sigkey)
                if sigkey in commonParams.keys():
                    continue
                else:
                    commonParams.update({sigkey: None})
            rich.print(commonParams)
            exportData[k] = commonParams
    # class/methods might have distinct annotations inside.

# with open(fpath, "w+") as f:
#     content = yaml.safe_dump(exportData, allow_unicode=True)
#     f.write(content)

code_path, template_path = jinja_utils.code_and_template_path(
    base_name := "common_fixtures"
)
jinja_utils.load_render_and_format(
    template_path, code_path, render_params := dict(data = exportData), banner := "TEST FIXTURES"
)
