fpath = "device_info.yml.tmp"

import yaml
import sys
sys.path.append("../")

from ies_optim import *

for k, v in globals():
    # print(k)
    # print(k.__annotations__)
    if k.endswith("信息") and (not k.startswith("设备")):
        ...
    # class/methods might have distinct annotations inside.