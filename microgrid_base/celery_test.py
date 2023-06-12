import json
from urllib import request
with open("template_input.json",'r') as f:
    mDictList = json.load(f)

import requests

port = 9870
url = f"http://127.0.0.1:{port}/calculate_async"
from fastapi_datamodel_template import EnergyFlowGraph
from ies_optim import 设备节点
# data = EnergyFlowGraph(mDictList=mdictList)
mdata = mDictList[0]['nodes'][0]
import rich
rich.print(mdata) # 设备
# requests.get(url, json=...)