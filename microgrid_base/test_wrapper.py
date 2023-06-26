from ies_optim import ModelWrapperContext
from celery.app.task import Task
Task.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls) # type: ignore[attr-defined]

def func():
    def func2():
        with ModelWrapperContext() as m:
            raise Exception("error")
    func2()


# func()

from celery import Celery
from passwords import redis_password
from typing import Union

MAIN_NAME = "test_wrapper"

app = Celery(
    MAIN_NAME,
    broker="amqp://guest@localhost:5672//",
    backend=f"redis://:{redis_password}@localhost:6380",
    # backend=f"redis://:{redis_password}@localhost:6379",
)

@app.task(store_errors_even_if_ignored=True)
def mfunc():
    func()

app.conf.update(task_track_started=True)
app.conf.update(worker_send_task_events=True)
concurrent_tasks = 3
app.conf.update(worker_concurrency=concurrent_tasks)
memory_limit = 20_000_000  # kB -> 20GB
app.conf.update(worker_max_memory_per_child=memory_limit)
time_limit = 60 * 25  # sec, 25 minutes.
app.conf.update(worker_time_limit=time_limit)
# limits on ram usage, concurrency, execution time

if __name__ == "__main__":
    worker = app.Worker()
    worker.start()
