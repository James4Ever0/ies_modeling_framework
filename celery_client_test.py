import requests

LOOP_COUNT = 5

base_url = "http://localhost:8010"
url = f"{base_url}/add/2/1"

r = requests.get(url)
data = r.json()

print("DATA", data)
task_id = data["task_id"]

r2 = requests.get(f'{base_url}/add/1/2')
data2 = r2.json()
task_id2 = data2['task_id']

url_new = f"{base_url}/task_status"

import time

# import celery.states as S
# PENDING, RECEIVED, STARTED, SUCCESS, FAILURE, RETRY, REVOKED,

# how to limit the task threads?

for _ in range(LOOP_COUNT):
    r2 = requests.get(url_new, params=dict(task_id=task_id))
    data2 = r2.json()
    print("DATA2", data2)  # STARTED.
    # till: SUCCESS.
    r3 = requests.get(url_new, params=dict(task_id=task_id))
    # how many status indicators can it have?
    time.sleep(1)

url_revoke = f"{base_url}/revoke"

r3 = requests.get(url_revoke, params=dict(task_id=task_id))
data3 = r3.json()
print("REVOKE RESULT?", data3)

r3 = requests.get(url_revoke, params=dict(task_id=task_id))
data3 = r3.json()
print("REVOKE RESULT?", data3)
time.sleep(1)
r2 = requests.get(url_new, params=dict(task_id=task_id))
data2 = r2.json()
print(
    "DATA2", data2
)  # SUCCESS if revoke after SUCCESS. but if revoke before SUCCESS it is REVOKED.
