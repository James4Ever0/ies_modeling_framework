# test to setup celery task schedule.
# import sys

# not working.
# sys.argv.append('-E')

from celery import Celery

# app = Celery("tasks") # not using any broker? it is default!
# set up pyamqp.
# app = Celery("tasks", broker="pyamqp://guest@localhost//")
from passwords import redis_password

MAIN_NAME = "tasks"

app = Celery(
    MAIN_NAME,
    # we ignore the main, see if error persists?
    # the error persists. continue.
    broker="amqp://guest@localhost:5672//",
    backend=f"redis://:{redis_password}@localhost:6379",  # already running, don't know how.
)

# need authentication!


@app.task
def add(x, y):
    print("CALCULATING:", x, y)
    # but we plan to do this for 10 seconds.
    import time

    time.sleep(10)
    return x + y


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

if __name__ == "__main__":
    worker = app.Worker()
    # print(dir(worker))
    worker.start()  # blocking for sure.
    # breakpoint()
