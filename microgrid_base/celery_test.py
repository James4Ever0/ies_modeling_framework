import json

with open("template_input.json", "r") as f:
    mDictList = json.load(f)

# 修改为环保目标

mDictList[0]["graph"]["计算目标"] = "环保"

import requests

port = 9870
ip = "127.0.0.1"

# port = 9871
# ip = "192.168.3.10"

url = f"http://{ip}:{port}/calculate_async"
result_url = f"http://{ip}:{port}/get_calculation_result_async"
status_url = f"http://{ip}:{port}/get_calculation_state"

test = "create_task"
# test = "check_result"
# test = "check_status"

task_id = "914702ea-433c-4534-97ea-5cc619e37730"
# task_id = "2533b339-86db-45bb-8d03-5d38ff9ff52c"
check_data = dict(calculation_id=task_id)

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
    r = requests.get(result_url, params=check_data)
    print(r.status_code)
    print(r.content)
    output_path = "output_template.json"
    print(f"writing to: {output_path}")
    with open(output_path, "w+") as f:
        f.write(json.dumps(r.json(), indent=4, ensure_ascii=False))
elif test == "check_status":
    r = requests.get(status_url, params=check_data)
    print(r.status_code)
    print(r.content)
else:
    raise Exception("TEST IS NOT CREATED:", test)
# t = 设备节点.parse_obj(mdata)
# print(t)
