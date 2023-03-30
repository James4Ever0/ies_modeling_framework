# suggestion: use fastapi for self-documented server, use celery for task management.
# celery reference: https://github.com/GregaVrbancic/fastapi-celery/blob/master/app/main.py

port = 9870
host = "0.0.0.0"
import traceback

appName = "IES Optim Server Template"
version = "0.0.1"
tags_metadata = [
    {"name": "async", "description": "异步接口，调用后立即返回"},
    {"name": "sync", "description": "同步接口，调用后需等待一段时间才返回"},
]
description = f"""
IES系统仿真和优化算法服务器

OpenAPI描述文件(可导入Apifox): https://{host}:{port}/openapi.json
API文档: https://{host}:{port}/docs
"""

import traceback
from fastapi import FastAPI
from fastapi_datamodel_template import (
    CalculationAsyncResult,
    CalculationAsyncSubmitResult,
    EnergyFlowGraph,
    RevokeResult,
    CalculationStateResult,
)

import datetime
from celery.result import AsyncResult
from typing import Dict, Any, Union
from fastapi_celery_server import app as celery_app

# remember these things won't persist.
# remove any task without any update for 24 hours.
# celery has the default of 24 hours. you handle it again here.
# also has default task time of 1200 seconds. you may experiment.
taskDict: Dict[str, AsyncResult] = {}
taskInfo: Dict[str, datetime.datetime] = {}
taskResult: Dict[str, Any] = {}


def remove_stale_tasks():
    """
    遍历并清除24小时未更新的任务
    """
    now = datetime.datetime.now()
    remove_keys = []
    for key, value in taskInfo.items():
        if (now - value).total_seconds() > 3600 * 24:
            remove_keys.append(key)
    for key in remove_keys:
        if key in taskDict.keys():
            del taskDict[key]
        if key in taskInfo.keys():
            del taskInfo[key]
        if key in taskResult.keys():
            del taskResult[key]

def remove_stale_tasks_decorator(function):
    def inner_function(*args, **kwargs):
        remove_stale_tasks()
        return function(*args, **kwargs)
    return inner_function


def celery_on_message(body: dict):
    print("BODY TYPE?", type(body))
    print("ON MESSAGE?", body)

    task_id = body["task_id"]
    status = body["status"]
    print("TASK STATUS?", status)

    taskInfo[task_id] = datetime.datetime.now()

    ###
    # BODY TYPE? <class 'dict'>
    # ON MESSAGE? {'status': 'STARTED', 'result': {'pid': 74297, 'hostname': 'celery@MacBook-Air-M1.local'}, 'traceback': None, 'children': [], 'date_done': None, 'task_id': 'c7a5a013-36aa-4242-842a-46fb3bb8e9fa'}

    ###
    # BODY TYPE? <class 'dict'>
    # ON MESSAGE? {'status': 'SUCCESS', 'result': '14', 'traceback': None, 'children': [], 'date_done': '2023-03-28T09:26:50.382791', 'task_id': 'c7a5a013-36aa-4242-842a-46fb3bb8e9fa'}


def background_on_message(task: AsyncResult):
    value = task.get(on_message=celery_on_message, propagate=False)
    # shall you not check here.
    # and not the message callback.
    # status = task.status
    # print("TASK STATUS?", status)
    taskResult[task.id] = value
    print("VALUE TYPE?", type(value))  # str, '14'
    print("TASK VALUE?", value)


app = FastAPI(description=description, version=version, tags_metadata=tags_metadata)

@remove_stale_tasks_decorator
@app.post(
    "/calculate_async",
    tags=["async"],
    description="填写数据并提交拓扑图，如果还有计算资源，提交状态为成功，返回计算ID，否则不返回计算ID，提交状态为失败",
    summary="异步提交能流拓扑图",
    response_description="提交状态以及模型计算ID,根据ID获取计算结果",
    response_model=CalculationAsyncSubmitResult,
)
def calculate_async(graph: EnergyFlowGraph) -> CalculationAsyncSubmitResult:
    # use celery
    submit_result = "failed"
    calculation_id = None
    try:
        calculation_id = ...
    except:
        traceback.print_exc()
    submit_result = "success"
    return CalculationAsyncSubmitResult(
        calculation_id=calculation_id, submit_result=submit_result
    )

@remove_stale_tasks_decorator
@app.get(
    "/get_calculation_state",
    tags=['async'],
    response_model=CalculationStateResult,
    response_description="Celery内置任务状态，如果是null则表示不存在该任务",
    summary="获取计算状态",
    description="根据计算ID获取计算状态",
)
def get_calculation_state(calculation_id: str) -> CalculationStateResult:
    """
    根据计算ID获取计算状态

    Args:
        calculation_id (str): 计算ID

    Returns:
        calculation_state (CalculationStateResult): 计算状态
    """
    calculation_state = None
    task = taskDict.get(calculation_id, None)
    if task is not None:
        calculation_state = task.state
    return CalculationStateResult(calculation_state=calculation_state)

@remove_stale_tasks_decorator
@app.get(
    "/get_calculation_result_async",
    tags=["async"],
    description="提交计算ID，返回计算状态，如果计算完毕会一起返回数据，否则数据为空",
    summary="异步获取能流拓扑计算结果",
    response_description="计算状态和计算结果",
    response_model=CalculationAsyncResult,
)
def get_calculation_result_async(calculation_id: str):
    calculation_result = taskResult.get(calculation_id, None)

    return CalculationAsyncResult(
        calculation_state=get_calculation_state(calculation_id).calculation_state,
        calculation_result=calculation_result,
    )

@remove_stale_tasks_decorator
@app.get(
    "/revoke_calculation",
    tags=["async"],
    description="提交计算ID，撤销计算",
    summary="撤销计算任务",
    response_description="返回撤销计算状态",
    response_model=RevokeResult,
    # different code and different response models.
    # so you would return in different models and the api will handle the code.
    # by default there are some reserved code, for every api. no need to define your own? or the system will merge the custom response code with default ones automatically?
    # responses={"200": {"description": "撤销成功", "model": RevokeResult}},
)
def revoke_calculation(calculation_id: str):

    revoke_result = "failed"
    calculation_state = None
    if calculation_id in taskDict.keys():
        print("TERMINATING TASK:", calculation_id)
        taskDict[calculation_id].revoke(terminate=True)
        revoke_result = "success"
        calculation_state = get_calculation_state(calculation_id).calculation_state
    else:
        print("TASK DOES NOT EXIST:", calculation_id)
    return RevokeResult(
        revoke_result=revoke_result, calculation_state=calculation_state
    )
from typing import List
@app.get("/get_calculation_ids",response_model = List[str], response_description='', description='' summary='')
def get_calculation_ids()->  List[str]:
    calculation_ids = list(taskDict.keys())
    return calculation_ids

import uvicorn

uvicorn.run(app, host=host, port=port)
