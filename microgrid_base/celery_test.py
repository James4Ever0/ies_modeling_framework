import json

with open("template_input.json", "r") as f:
    mDictList = json.load(f)

import requests

port = 9870
ip = "127.0.0.1"
url = f"http://{ip}:{port}/calculate_async"
result_url = f"http://{ip}:{port}/get_calculation_result_async"

# test = "create_task"
test = "check_result"

if test == "create_task":
    from fastapi_datamodel_template import EnergyFlowGraph

    # from ies_optim import 设备节点
    data = EnergyFlowGraph(mDictList=mDictList)
    # mdata = mDictList[0]['nodes'][25] # 25-35
    # import rich
    # rich.print(mdata) # 设备
    r = requests.post(url, json=data.dict())
    print(r.json())
    print(r.status_code)
elif test == "check_result":
    task_id = "f909e827-4385-4e17-bad8-fc71670017e2"
    data = dict(calculation_id=task_id)
    r = requests.get(result_url, params=data)
    print(r.status_code)
    print(r.content)
else:
    raise Exception("TEST IS NOT CREATED:", test)
# t = 设备节点.parse_obj(mdata)
# print(t)
