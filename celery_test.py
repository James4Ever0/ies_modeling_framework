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

MAIN_NAME = "celery_test"
# MAIN_NAME = "tasks"

app = Celery(
    MAIN_NAME,
    # we ignore the main, see if error persists?
    # the error persists. continue.
    broker="amqp://guest@localhost:5672//",
    backend=f"redis://:{redis_password}@localhost:6379",  # already running, don't know how.
)

# need authentication!

from pydantic import BaseModel


class AddResult(BaseModel):
    data: int


class AddResultNested(BaseModel):
    nested_addresult: AddResult


@app.task
def add(x, y):
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

# better run this with celery commandline.
# if __name__ == "__main__":
#     worker = app.Worker()
#     # print(dir(worker))
#     worker.start()  # blocking for sure.
#     # breakpoint()
