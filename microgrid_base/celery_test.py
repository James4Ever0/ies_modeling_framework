import json
from urllib import request
with open("template_input.json",'r') as f:
    mDictList = json.load(f)

import requests

port = 9870
url = f"http://127.0.0.1:{port}/calculate_async"
from fastapi_datamodel_template import EnergyFlowGraph
# from ies_optim import 设备节点
data = EnergyFlowGraph(mDictList=mDictList)
# mdata = mDictList[0]['nodes'][25] # 25-35
# import rich
# rich.print(mdata) # 设备
r = requests.post(url, json = data.dict())
print(r.json())
print(r.status_code)
# t = 设备节点.parse_obj(mdata)
# print(t)