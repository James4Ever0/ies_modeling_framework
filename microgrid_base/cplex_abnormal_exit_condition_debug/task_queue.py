import time
import os
if os.name == 'nt':
    import dill
    import multiprocessing.reduction
    multiprocessing.reduction.dump = dill.dump
from huey import SqliteHuey
# huey = RedisHuey(port=6380)

huey = SqliteHuey(filename='demo.db')

@huey.task(retries=3)
def task_success():
    print("running task success")
    time.sleep(1)
    print("end running task success")

@huey.task(retries=3)
def task_fail():
    print("running task fail")
    time.sleep(2)
    print("end running task fail")

