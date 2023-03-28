# test to setup celery task schedule.
# import sys

# not working.
# sys.argv.append('-E')

from celery import Celery

# app = Celery("tasks") # not using any broker? it is default!
# set up pyamqp.
# app = Celery("tasks", broker="pyamqp://guest@localhost//")
from passwords import redis_password

app = Celery(
    "tasks",
    broker="amqp://guest@localhost:5672//",
    backend=f"redis://:{redis_password}@localhost:6379", # already running, don't know how.
)

# need authentication!

@app.task
def add(x, y):
    print("CALCULATING:", x, y)
    return x + y

# well, how to set this up?

# what is this for anyway?
app.conf.update(task_track_started=True) # still off?
# print("APP CONF?", app.conf)
# breakpoint()

# just like the commandline config "-E"
app.conf.update(worker_send_task_events=True)

if __name__ == "__main__":
    worker = app.Worker()
    # print(dir(worker))
    worker.start()  # blocking for sure.
    # breakpoint()
