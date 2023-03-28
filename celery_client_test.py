import requests

base_url = "http://localhost:8010"
url = f"{base_url}/add/2/1"

r = requests.get(url)
data = r.json()

print("DATA", data)
task_id = data["task_id"]

url_new = f"{base_url}/task_status"

import time
# import celery.states as S
# PENDING, RECEIVED, STARTED, SUCCESS, FAILURE, RETRY, REVOKED,

# how to limit the task threads?

for _ in range(20):
    r2 = requests.get(url_new, params=dict(task_id=task_id))
    data2 = r2.json()
    print("DATA2", data2) # STARTED. 
    # till: SUCCESS.
    # how many status indicators can it have?
    time.sleep(1)
