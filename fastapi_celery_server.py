from celery import Celery
from passwords import redis_password
MAIN_NAME = "fastapi_celery"

app = Celery(
    MAIN_NAME,
    broker="amqp://guest@localhost:5672//",
    backend=f"redis://:{redis_password}@localhost:6379",
)
# you'd better import models from other datamodel only file
# you had not to pass anything like pydantic data model as parameter.

@app.task
def calculate_energyflow_graph(energyflow_graph:dict) -> dict:
    """
    """
    calculation_result = {} # dummy result.
    return calculation_result


app.conf.update(task_track_started=True)
app.conf.update(worker_send_task_events=True)

# limits on ram usage, concurrency, execution time

if __name__ == "__main__":
    worker = app.Worker()
    worker.start()
