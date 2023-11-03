from log_utils import logger_print

# suggestion: use fastapi for self-documented server, use celery for task management.
# celery reference: https://github.com/GregaVrbancic/fastapi-celery/blob/master/app/main.py

import traceback
from fastapi import BackgroundTasks, FastAPI
from fastapi_datamodel_template import (
    CalculationAsyncResult,
    CalculationAsyncSubmitResult,
    CalculationResult,
    EnergyFlowGraph,
    RevokeResult,
    CalculationStateResult,
)

port = 9870
host = "0.0.0.0"
import logging
from log_utils import (
    fastapi_log_filename,
    stdout_handler,
    makeRotatingFileHandler,
    # Formatter
)
from log_utils import logger_print as lp

fastapi_log_handler = makeRotatingFileHandler(fastapi_log_filename)
logger = logging.getLogger("fastapi")
logger.setLevel("DEBUG")
logger.addHandler(fastapi_log_handler)
logger.addHandler(stdout_handler)
# import celery


def logger_print(*args):  # override this.
    lp(*args, logger=logger)


from config import *

# import os

# MOCK = ies_env.STATIC_MOCK
# changed to MOCK_TEST in config.py
# MOCK = os.environ.get("MOCK", None)  # if this is mock test.
import json
from mock_utils import mock_calculation_result

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


# from fastapi.utils import is_body_allowed_for_status_code
# from starlette.exceptions import HTTPException
from starlette.requests import Request

# from starlette.responses import JSONResponse  # , Response
# from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


# define the input structure here.
# from pydantic import BaseModel
from typing import List  # , Union , Literal, Dict

# solved or not?

import datetime
from celery.result import AsyncResult
from typing import Dict, Any

if ies_env.STATIC_MOCK is None:
    from fastapi_celery_server import app as celery_app

# remember these things won't persist.
# remove any task without any update for 24 hours.
# celery has the default of 24 hours. you handle it again here.
# also has default task time of 1200 seconds. you may experiment.
taskDict: Dict[str, AsyncResult] = {}
"""
任务ID和任务对象的字典
"""
taskInfo: Dict[str, datetime.datetime] = {}
"""
任务ID和任务最近更新时间的字典
"""
taskResult: Dict[str, Any] = {}
"""
任务ID和任务结果的字典
"""


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
    """
    清除过期任务装饰器
    """

    def inner_function(*args, **kwargs):
        remove_stale_tasks()
        return function(*args, **kwargs)

    return inner_function


error_log_dict = {}


def celery_on_message(body: dict):
    """
    Celery任务信息更新回调函数

    Args:
        body (dict): 更新的任务信息
    """
    logger_print("BODY TYPE?", type(body))
    logger_print("ON MESSAGE?", body)

    task_id = body["task_id"]
    status = body["status"]

    logger_print("TASK STATUS?", status)
    if status == "FAILURE":
        error_log_dict[task_id] = body.get("traceback", "")

    taskInfo[task_id] = datetime.datetime.now()

    ###
    # BODY TYPE? <class 'dict'>
    # ON MESSAGE? {'status': 'STARTED', 'result': {'pid': 74297, 'hostname': 'celery@MacBook-Air-M1.local'}, 'traceback': None, 'children': [], 'date_done': None, 'task_id': 'c7a5a013-36aa-4242-842a-46fb3bb8e9fa'}

    ###
    # BODY TYPE? <class 'dict'>
    # ON MESSAGE? {'status': 'SUCCESS', 'result': '14', 'traceback': None, 'children': [], 'date_done': '2023-03-28T09:26:50.382791', 'task_id': 'c7a5a013-36aa-4242-842a-46fb3bb8e9fa'}


def background_on_message(task: AsyncResult):
    """
    后台获取任务计算结果的方法

    Args:
        task (AsyncResult): 任务对象
    """
    value = task.get(on_message=celery_on_message, propagate=False)
    # shall you not check here.
    # and not the message callback.
    status = task.status
    logger_print("TASK STATUS?", status)
    logger_print()

    logger_print("VALUE TYPE?", type(value))  # str, '14'
    logger_print("TASK VALUE?", value)
    if status == "SUCCESS":
        logger_print("TASK RESULT SET")
        taskResult[task.id] = value  # this will be exception.
    else:
        logger_print("NOT SETTING TASK RESULT")


# Reference: https://github.com/tiangolo/fastapi/issues/459

# from typing import Any
# import orjson
# from starlette.responses import JSONResponse


# class ORJSONResponse(JSONResponse):
#     media_type = "application/json"

#     def render(self, content: Any) -> bytes:
#         return orjson.dumps(content)
import fastapi

app = FastAPI(
    debug=True,
    description=description,
    version=version,
    tags_metadata=tags_metadata,
    # default_response_class=ORJSONResponse,
    default_response_class=fastapi.responses.ORJSONResponse,
)
# let us use this instead.
# ref; https://fastapi.tiangolo.com/advanced/custom-request-and-route/
from fastapi import FastAPI, Request, Response
from fastapi.routing import APIRoute
from typing import Callable
from log_utils import terminal_column_size
import json


class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            # except RequestValidationError as exc:
            except Exception as e:
                is_json = False
                try:
                    body = await request.json()
                    body = json.dumps(body, indent=4, ensure_ascii=False)
                    is_json = True
                except:
                    body = await request.body()
                logger_print(
                    "request{}".format("_json" if is_json else "")
                    .upper()
                    .center(terminal_column_size, "_"),
                    body,
                )
                logger_print("exception".upper().center(terminal_column_size, "_"), e)
                # detail = {"errors": exc.errors(), "body": body.decode()}
                # raise HTTPException(status_code=422, detail=detail)
                raise e

        return custom_route_handler


app.router.route_class = ValidationErrorLoggingRoute

# @app.exception_handler(RequestValidationError)
# async def request_validation_exception_handler(
#     request: Request, exc: RequestValidationError
# ) -> JSONResponse:
#     # TODO: log request body
#     # logger_print("request", await request.body(), logger=logger)
#     logger_print("exception", exc.raw_errors, exc.body, logger=logger)
#     return JSONResponse(
#         status_code=HTTP_422_UNPROCESSABLE_ENTITY,
#         content={"detail": jsonable_encoder(exc.errors())},
#     )

import uuid


@remove_stale_tasks_decorator
@app.post(
    "/calculate_async",
    tags=["async"],
    description="填写数据并提交拓扑图，如果还有计算资源，提交状态为成功，返回计算ID，否则不返回计算ID，提交状态为失败",
    summary="异步提交能流拓扑图",
    response_description="提交状态以及模型计算ID,根据ID获取计算结果",
    response_model=CalculationAsyncSubmitResult,
)
def calculate_async(
    graph: EnergyFlowGraph if not (ies_env.FAILSAFE or ies_env.STATIC_MOCK) else dict,
    background_task: BackgroundTasks,
) -> CalculationAsyncSubmitResult:
    # use celery
    calculation_id = None
    submit_result = "failed"

    if ies_env.STATIC_MOCK:
        submit_result = "success"
        calculation_id = uuid.uuid4().__str__()
    else:
        try:
            function_id = "fastapi_celery.calculate_energyflow_graph"
            task = celery_app.send_task(
                function_id, args=(graph if isinstance(graph, dict) else graph.dict(),)
            )  # async result?
            taskInfo[task.id] = datetime.datetime.now()
            taskDict[task.id] = task
            background_task.add_task(background_on_message, task)
            calculation_id = task.id
            submit_result = "success"
        except:
            traceback.print_exc()
    if ies_env.FAILSAFE:
        if calculation_id is None:
            calculation_id = uuid.uuid4().__str__()
        if submit_result is not "success":
            submit_result = "success"
    return CalculationAsyncSubmitResult(
        calculation_id=calculation_id,
        submit_result="success",
    )


@remove_stale_tasks_decorator
@app.get(
    "/get_calculation_state",
    tags=["async"],
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
    if ies_env.STATIC_MOCK or ies_env.FAILSAFE:
        calculation_state = "SUCCESS"
        # return CalculationStateResult(calculation_state="SUCCESS")
    else:
        # calculation_state = None
        # task = taskDict.get(calculation_id, None)
        if task := taskDict.get(calculation_id, None):
            calculation_state = task.state
        else:
            calculation_state = "NOT_CREATED"
    return CalculationStateResult(calculation_state=calculation_state)


# from fastapi_datamodel_template import ParetoCurve

from log_utils import logger_traceback


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
    if ies_env.STATIC_MOCK:
        calculation_result, calculation_state = getStaticCalculationResultAndState()
    else:
        try:
            calculation_result = taskResult.get(calculation_id, None)
            calculation_state = get_calculation_state(calculation_id).calculation_state
            if calculation_result is None:
                if calculation_state == "FAILURE":
                    if ies_env.FAILSAFE:
                        (
                            calculation_result,
                            calculation_state,
                        ) = getStaticCalculationResultAndState()
                    else:
                        error_log = error_log_dict.get(calculation_id, None)
                        if error_log:
                            calculation_result = CalculationResult(
                                resultList=[], success=False, error_log=error_log
                            ).dict()
            else:
                calculation_result = CalculationResult.parse_obj(calculation_result)
        except Exception as exc:
            if ies_env.FAILSAFE:
                (
                    calculation_result,
                    calculation_state,
                ) = getStaticCalculationResultAndState()
                logger_traceback()
            else:
                raise exc
        # calculation_result = (
        #     CalculationResult.parse_obj(calculation_result)
        #     if calculation_result
        #     else None
        # )

    # this is for generating pareto curve. since we cannot persist it, leave it to frontend.

    # if isinstance(calculation_result, CalculationResult):
    #     if len(RL:=calculation_result.resultList)>1:
    #         plotList = []
    #         for result in RL:
    #             OR = result.objectiveResult
    #             plotList.append((OR.financialObjective,OR.environmentalObjective))
    #         plotList.sort(lambda x: x[0])
    #         calculation_result.paretoCurve = ParetoCurve(x=[e[0] for e in plotList],x_label='经济', y=[e[1] for e in plotList], y_label='环保')

    return CalculationAsyncResult(
        calculation_state=calculation_state,
        calculation_result=calculation_result,
    )


def getStaticCalculationResultAndState():
    calculation_result = mock_calculation_result.copy()
    calculation_state = "SUCCESS"
    return calculation_result, calculation_state


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

    if ies_env.STATIC_MOCK:
        revoke_result = "success"
        calculation_state = "REVOKED"
    else:
        if calculation_id in taskDict.keys():
            logger_print("TERMINATING TASK:", calculation_id)
            taskDict[calculation_id].revoke(terminate=True)
            revoke_result = "success"
            calculation_state = get_calculation_state(calculation_id).calculation_state
        else:
            logger_print("TASK DOES NOT EXIST:", calculation_id)
            calculation_state = "NOT_CREATED"

    if ies_env.FAILSAFE:
        if revoke_result is not "success":
            revoke_result = "success"
        if calculation_state is not "REVOKED":
            calculation_state = "REVOKED"
    return RevokeResult(
        revoke_result=revoke_result, calculation_state=calculation_state
    )


from typing import List


@app.get(
    "/get_calculation_ids",
    tags=["async"],
    response_model=List[str],
    response_description="缓存中可查询的任务ID列表",
    description="任务如果24小时内没有状态更新会被清出缓存，检查缓存中的所有可查询任务ID",
    summary="查询任务ID",
)
def get_calculation_ids() -> List[str]:
    if ies_env.STATIC_MOCK:
        calculation_ids = []
    else:
        calculation_ids = list(taskDict.keys())
    return calculation_ids


import uvicorn

uvicorn.run(app, host=host, port=port)
