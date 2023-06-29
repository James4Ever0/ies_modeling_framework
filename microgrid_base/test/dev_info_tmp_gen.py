fpath = "device_info.yml.tmp"

import yaml
import sys
sys.path.append("../")

from ies_optim import *

for k, v in globals():
    print(k)
    # print(k.__annotations__)
    # class/methods might have distinct annotations inside.