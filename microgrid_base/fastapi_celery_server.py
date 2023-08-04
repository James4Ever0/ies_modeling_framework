from log_utils import logger_print, makeRotatingFileHandler, celery_log_filename

from celery import Celery
from passwords import redis_password
from typing import Union

MAIN_NAME = "fastapi_celery"

app = Celery(
    MAIN_NAME,
    broker="amqp://guest@localhost:5672//",
    backend=f"redis://:{redis_password}@localhost:6380",
    # backend=f"redis://:{redis_password}@localhost:6379",
)

# override format exception logic. (seems not working at all!)
# ref: https://poe.com/s/PV9zAO91vGQjHJuZ4toR (GPT4)

import better_exceptions
import sys
from celery.utils.log import ColorFormatter  # type: ignore

app.conf.update(CELERY_TIMEZONE="Asia/Shanghai", CELERY_ENABLE_UTC=False)


# class CustomFormatter(logging.Formatter):
class CustomFormatter(ColorFormatter):
    def formatException(self, exc_info):
        """
        Format the exception information and return the formatted string.

        Parameters:
            exc_info (tuple): The exception information tuple.

        Returns:
            str: The formatted exception string.
        """

        if exc_info and not isinstance(exc_info, tuple):
            exc_info = sys.exc_info()  # copied from `ColorFormatter.formatException`

        lines = better_exceptions.format_exception(*exc_info)
        return "".join(lines)


custom_formatter = CustomFormatter()
import logging

celery_logger = app.log.get_default_logger()
celery_logger.addHandler(
    makeRotatingFileHandler(celery_log_filename, level=logging.NOTSET)
)

for handler in celery_logger.handlers:
    handler.setFormatter(custom_formatter)

# you'd better import models from other datamodel only file
# you had not to pass anything like pydantic data model as parameter.

# from microgrid_base.ies_optim import EnergyFlowGraph
# from celery.exceptions import Ignore
from fastapi_celery_functions import calculate_energyflow_graph_base


@app.task()
# @app.task(bind=True)  # parse it elsewhere.
def calculate_energyflow_graph(energyflow_graph: dict) -> Union[None, dict]:
    ret = calculate_energyflow_graph_base(energyflow_graph)
    return ret


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
    worker.start()  # type:ignore
