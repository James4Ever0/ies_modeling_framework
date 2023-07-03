fpath = "device_info.yml.tmp"

import yaml
import sys

sys.path.append("../")

from ies_optim import *
import inspect
for k, v in globals():
    # print(k)
    # print(k.__annotations__)
    if k.endswith("信息") and (not k.startswith("设备")):
        if issubclass(v, 设备基础信息):
            devName = k.strip("信息")
            commonParams = dict(设备名称=devName)
            if issubclass(v, 设备信息):
                # 意味着有公共内容
                commonParams.update(生产厂商="Any", 设备型号=f"{devName}1")
            sig = inspect.signature(v)
            print(sig)
    # class/methods might have distinct annotations inside.
