from fastapi import FastAPI, Request
import time
from test_server_client_configs import *

GLOBAL_TASK_COUNT = 0

import datetime


def get_current_time_string():
    time_string = " ".join(datetime.datetime.now().isoformat().split(".")[0].split("T"))
    return time_string


def mock_calculation(data: str, sleep_time: float = 20):
    """
    Mocking the heavy calculation of system optimization.

    Args:
        sleep_time (float): the duration of our fake task, in seconds
    """
    print(f"TIME: {get_current_time_string()}")
    print(f"DATA RECEIVED: {len(data)}")
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


def trick_or_treat(data: str):
    if add_one_task():
        result = mock_calculation(data)  # you should put error code here. no exception?
        remove_one_task()
        return result
    return server_error_code.MAX_TASK_LIMIT


@app.post(f"/{endpoint_suffix.UPLOAD_GRAPH}")
def run_sync(data: str):
    return trick_or_treat(data)


RESULT_DICT = {}
TASK_LIST = []

import uuid


def execute_and_append_result_to_dict(unique_id: str, data: str):
    print(f"ASYNC TASK ASSIGNED: {unique_id}")
    result = mock_calculation(data)
    RESULT_DICT.update({unique_id: result})
    TASK_LIST.remove(unique_id)


@app.post(f"/{endpoint_suffix.UPLOAD_GRAPH_ASYNC}")
def run_async(data: str):  # how do you do it async? redis cache?
    if add_one_task():
        unique_id = uuid.uuid4()
        TASK_LIST.append(unique_id)
        threading.Thread(
            target=execute_and_append_result_to_dict, args=(unique_id, data)
        ).run()
        return unique_id
    return server_error_code.MAX_TASK_LIMIT


@app.post(f"/{endpoint_suffix.CHECK_RESULT_ASYNC}")
def get_result_async(unique_id: str):
    return RESULT_DICT.get(
        unique_id,
        server_error_code.PENDING
        if unique_id in TASK_LIST
        else server_error_code.NOTHING,
    )


import uvicorn

uvicorn.run(app, port=port)
