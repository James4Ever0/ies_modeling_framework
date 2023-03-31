import json
import requests

LOOP_COUNT = 20

base_url = "http://localhost:9870"
url = f"{base_url}/calculate_async"
with open("test_graph_data.json",'r') as f:
    test_graph = json.loads(f.read())
r = requests.post(url, json=test_graph)
data = r.json()

print("DATA", data)
calculation_id = data["calculation_id"]

r2 = requests.get(f'{base_url}/calculation_async')
data2 = r2.json()
calculation_id2 = data2['calculation_id']

url_new = f"{base_url}/get_calculation_state"

import time

# import celery.states as S
# PENDING, RECEIVED, STARTED, SUCCESS, FAILURE, RETRY, REVOKED,

# how to limit the task threads?

for i in range(LOOP_COUNT):
    print(i)
    r2 = requests.get(url_new, params=dict(calculation_id=calculation_id))
    data2 = r2.json()
    print("DATA2", data2)  # STARTED.
    # till: SUCCESS.
    r3 = requests.get(url_new, params=dict(calculation_id=calculation_id))
    data3 = r3.json()
    print("DATA3", data3)
    # how many status indicators can it have?
    time.sleep(1)

url_revoke = f"{base_url}/revoke_calculation"

r3 = requests.get(url_revoke, params=dict(calculation_id=calculation_id))
data3 = r3.json()
print("REVOKE RESULT?", data3)

r3 = requests.get(url_revoke, params=dict(calculation_id=calculation_id))
data3 = r3.json()
print("REVOKE RESULT?", data3)
time.sleep(1)
r2 = requests.get(url_new, params=dict(calculation_id=calculation_id))
data2 = r2.json()
print(
    "DATA2", data2
)  # SUCCESS if revoke after SUCCESS. but if revoke before SUCCESS it is REVOKED.
