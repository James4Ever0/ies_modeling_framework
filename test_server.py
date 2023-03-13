from fastapi import FastAPI
import time
from test_server_client_configs import *


def mock_calculation(sleep_time: float = 20):
    """
    Mocking the heavy calculation of system optimization.

    Args:
        sleep_time (float): the duration of our fake task, in seconds
    """
    time.sleep(sleep_time)


app = FastAPI()
# where is the port?

# create some context manager? sure?

# of course we will set limit to max running time per task

GLOBAL_TASK_COUNT = 0

# could there be multiple requests? use lock please?
import threading

LOCK = threading.Lock()


def add_one_task():
    global GLOBAL_TASK_COUNT, LOCK
    with LOCK:
        if GLOBAL_TASK_COUNT < MAX_TASK_COUNT:
            GLOBAL_TASK_COUNT += 1
            return True
    return False


def remove_one_task():
    global GLOBAL_TASK_COUNT, LOCK
    with LOCK:
        if GLOBAL_TASK_COUNT >= 0 and GLOBAL_TASK_COUNT <= MAX_TASK_COUNT:
            GLOBAL_TASK_COUNT -= 1
            return True
    return False


class MaxTaskLimit:
    def __init__(self):
        if not add_one_task():
            WARNING = "Max Running Tasks!"
            print(WARNING)
            raise Exception(WARNING)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        ...


@app.post(f"/{endpoint_suffix.UPLOAD_GRAPH}")
def run_sync():
    with MaxTaskLimit():
        


@app.post(f"/{endpoint_suffix.UPLOAD_GRAPH_ASYNC}")
def run_async():
    ...


@app.post(f"/{endpoint_suffix.CHECK_RESULT_ASYNC}")
def get_result_async():
    ...


import uvicorn

uvicorn.run(app, port=port)
