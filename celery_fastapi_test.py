from datetime import datetime
from fastapi import FastAPI, BackgroundTasks

# do not import the function. import the celery app.
from celery_test import app as celery_app

# from celery_test import add, app as celery_app
from celery.result import AsyncResult
import celery.states as S

from typing import Dict

taskDict: Dict[str, AsyncResult] = {}

# task_name = add.signature().name # working?
# print("TASK NAME?", task_name) # failed. man what is going on?

app = FastAPI()
# import logging

# log = logging.getLogger(__name__)
# do not use logging?
import datetime
from typing import Any

taskInfo: Dict[str, Dict[str, datetime.datetime]] = {}
taskResult: Dict[str, Any] = {}


def celery_on_message(body: dict):
    """
    """
    print("BODY TYPE?", type(body))
    print("ON MESSAGE?", body)

    task_id = body["task_id"]

    status = body["status"]
    if task_id not in taskInfo.keys():
        taskInfo[task_id] = {}

    if status not in taskInfo[task_id].keys():
        taskInfo[task_id][status] = datetime.datetime.now()

    ###
    # BODY TYPE? <class 'dict'>
    # ON MESSAGE? {'status': 'STARTED', 'result': {'pid': 74297, 'hostname': 'celery@MacBook-Air-M1.local'}, 'traceback': None, 'children': [], 'date_done': None, 'task_id': 'c7a5a013-36aa-4242-842a-46fb3bb8e9fa'}

    ###
    # BODY TYPE? <class 'dict'>
    # ON MESSAGE? {'status': 'SUCCESS', 'result': '14', 'traceback': None, 'children': [], 'date_done': '2023-03-28T09:26:50.382791', 'task_id': 'c7a5a013-36aa-4242-842a-46fb3bb8e9fa'}


def background_on_message(task: AsyncResult):
    """
    """
    value = task.get(on_message=celery_on_message, propagate=False)
    # shall you not check here.
    # and not the message callback.
    # status = task.status
    # print("TASK STATUS?", status)
    taskResult[task.id] = value
    print("VALUE TYPE?", type(value))  # str, '14'
    print("TASK VALUE?", value)


# can you check the task status, finished or not, unblockingly?

# backend does not support on_message callback?


# the celery backend must use both redis and rabbitmq.


# also, revoke tasks, if wanted.
# check the task creation time?


@app.get("/add/{a}/{b}")
def add_get(a, b, background_task: BackgroundTasks):
    """
    # apparently it is not calling celery.
    # val = add(a,b)
    args = [a, b]
    # print("")
    # never registered. use name instead?
    from celery_test import MAIN_NAME
    task_name = f"{MAIN_NAME}.add"
    task: AsyncResult = celery_app.send_task(task_name, args=args)
    # task:AsyncResult = add.apply_async(args=args)

    print("PENDING CELERY TASK:", task)  # this has the task id, but this is an object.
    # print("TASK TYPE?", type(task)) # <class 'celery.result.AsyncResult'>
    print("TASK ID?", type(task.id), task.id)  # autocompleted.
    # task.id is of type "str"
    if task.id:
        background_task.add_task(background_on_message, task)
        # return "RECEIVED"
        taskDict.update({task.id: task})
        task_status = task.status
        if task_status not in S.EXCEPTION_STATES:
            status = "RECEIVED"  # this is not the task status.
        else:
            print("TASK STATUS", task_status)
            status = "EXCEPTION"
    else:
        print("TASK ID IS NONE.")
        status = "ERROR"
    return {"task_id": task.id, "status": status, "task_status": task.status}


@app.get("/task_status")
def get_task_status(task_id: str):
    task_status = "MISSING"
    if task_id in taskDict.keys():
        task_status = taskDict[task_id].status
    print("CHECKING TASK:", task_id)
    print("TASK STATUS:", task_status)
    return task_status


@app.get("/revoke")
def revoke_task(task_id: str):
    if task_id in taskDict.keys():
        taskDict[task_id].revoke(terminate=True)
    else:
        return "MISSING"
    print("TERMINATING TASK:", task_id)
    return "REVOKED"


@app.get("/task_result", response_description="", response_model=..., description="", summary="")
def get_task_result(task_id: str):
    task_result = taskResult.get(task_id, None)
    task_status = "MISSING"
    if task_result:
        task_status = taskDict[task_id].status

    return dict(task_result=task_result, task_status=task_status)

import uvicorn

uvicorn.run(app, host="127.0.0.1", port=8010)
# background tasks will be executed even if interrupted.
