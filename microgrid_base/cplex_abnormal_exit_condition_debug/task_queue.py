import time

from redis import Redis
from rq import Queue, Retry

port = 6380
print("Connecting to Redis at port " + port)
q = Queue(connection=Redis(port=port))

def task_success():
    print("running task success")
    time.sleep(1)
    print("end running task success")

def task_fail():
    print("running task fail")
    time.sleep(2)
    print("end running task fail")