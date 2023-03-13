from fastapi import FastAPI
import time
from test_server_client_configs import *

GLOBAL_TASK_COUNT = 0


def mock_calculation(sleep_time: float = 20):
    """
    Mocking the heavy calculation of system optimization.

    Args:
        sleep_time (float): the duration of our fake task, in seconds
    """
    print(f"CALCULATING! TASK #{GLOBAL_TASK_COUNT}")
    time.sleep(sleep_time)
    print(f"TASK #{GLOBAL_TASK_COUNT} DONE!")
    return "CALCULATED RESULT"  # fake though.


app = FastAPI()
# where is the port?

# create some context manager? sure?

# of course we will set limit to max running time per task

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


def trick_or_treat():
    if add_one_task():
        result = mock_calculation()
        remove_one_task()
        return result
    return "MAX TASK LIMIT"


@app.post(f"/{endpoint_suffix.UPLOAD_GRAPH}")
def run_sync():
    return trick_or_treat()


RESULT_DICT = {}

import uuid


def execute_and_append_result_to_dict(unique_id: str):
    result = mock_calculation()
    RESULT_DICT.update({unique_id: result})


@app.post(f"/{endpoint_suffix.UPLOAD_GRAPH_ASYNC}")
def run_async():  # how do you do it async? redis cache?
    if add_one_task():
        unique_id = uuid.uuid4()
        threading.Thread(
            target=execute_and_append_result_to_dict, args=(unique_id,)
        ).run()
        return unique_id
    return "MAX TASK LIMIT"


@app.post(f"/{endpoint_suffix.CHECK_RESULT_ASYNC}")
def get_result_async(unique_id: str):
    return RESULT_DICT.get(unique_id, "NOTHING")


import uvicorn

uvicorn.run(app, port=port)
