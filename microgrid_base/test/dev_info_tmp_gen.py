fpath = "device_info.yml.tmp"

import yaml
import sys
sys.path.append("../")

from ies_optim import *

for k, v in globals():
    # print(k)
    # print(k.__annotations__)
    if k.endswith("设备名称") and (not k.startswith("设备")):
        if issubclass(v, 设备信息):
            # 意味着有公共内容
            devName = k.strip("信息")
            设备名称 = devName,
            生产厂商 = "",
            设备型号 = f"{devName}1"
    # class/methods might have distinct annotations inside.