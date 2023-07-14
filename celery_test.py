# hashicorp nomad?

# test to setup celery task schedule.
# import sys

# not working.
# sys.argv.append('-E')
# import os
# os.environ['CELERYD_CONCURRENCY']='1'
from celery import Celery

# app = Celery("tasks") # not using any broker? it is default!
# set up pyamqp.
# app = Celery("tasks", broker="pyamqp://guest@localhost//")
from passwords import redis_password

redis_url = f"redis://:{redis_password}@localhost:6379"
# MAIN_NAME = "celery_test"
MAIN_NAME = "tasks"

app = Celery(
    MAIN_NAME,
    # we ignore the main, see if error persists?
    # the error persists. continue.
    broker="amqp://guest@localhost:5672//",
    backend=redis_url,  # already running, don't know how.
)

# need authentication!

from pydantic import BaseModel


class AddResult(BaseModel):
    data: int


class AddResultNested(BaseModel):
    nested_addresult: AddResult


# import filelock # best way of limiting concurrency? or not?

# LOCK_FILE = ".celery.lock"

# working.
# import multiprocessing
# lock = multiprocessing.Lock()


# use redis lock.
# from redis import Redis
# from redis.lock import Lock as RedisLock

# redis_instance = Redis.from_url(redis_url)

REDIS_TASK_KEY = "current_task"

# import portalocker


@app.task
def add(x, y):
    # with portalocker.Lock('.celery.lock','r+', portalocker.LOCK_EX):
    # with lock:  #the lock is simply working.

    # with filelock.FileLock(LOCK_FILE): # this lock is not sharing.
    # with lock:
    # why not working?
    # with lock:
    # still the same?
    # with RedisLock(redis_instance, name="task_id"): # no one will have the lock.
    print("CALCULATING:", x, y)
    # but we plan to do this for 10 seconds.
    import time

    time.sleep(10)
    obj = AddResultNested(
        nested_addresult=AddResult(data=x + y)
    ).dict()  # it is also dict. just to make it json serializable. do not pass pydantic data models directly.
    # what about nested data models?
    # it also handles the serialization correctly. nevertheless.
    
    return AddResultNested.parse_obj(obj).dict() # still being correct.
    # so you can parse it and dump it.

    # json in, json out.


# print(dir(add))
# breakpoint()
# well, how to set this up?

# what is this for anyway?
app.conf.update(task_track_started=True)  # still off?
# print("APP CONF?", app.conf)
# breakpoint()
# how to limit the number of concurrencies?

# just like the commandline config "-E"
app.conf.update(worker_send_task_events=True)
app.conf.update(worker_concurrency=1) # having the same effect of holding the process-wide lock, but showing the status of "PENDING" instead.
# import pint
# ureg = pint.UnitRegistry()
# # 2000_000
memory_limit = 20_000_000
# memory_limit = (20*ureg.GB).to(ureg.kB).magnitude # in kB
# memory_limit is None by default, means no limit on ram
app.conf.update(worker_max_memory_per_child=memory_limit)

# better run this with celery commandline.
if __name__ == "__main__":
    worker = app.Worker()
    # print(dir(worker))
    worker.start()  # blocking for sure.
    # breakpoint()
