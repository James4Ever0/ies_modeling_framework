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

# override format exception logic.
# ref: https://poe.com/s/PV9zAO91vGQjHJuZ4toR (GPT4)

import better_exceptions
import sys
from celery.utils.log import ColorFormatter  # type: ignore

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
            exc_info = sys.exc_info() # copied from `ColorFormatter.formatException`
    
        lines = better_exceptions.format_exception(*exc_info)
        return "".join(lines)

custom_formatter = CustomFormatter()

for handler in app.log.get_default_logger().handlers:
    handler.setFormatter(custom_formatter)

# you'd better import models from other datamodel only file
# you had not to pass anything like pydantic data model as parameter.
from solve_model import (
    solveModelFromCalcParamList,
    mDictListToCalcParamList,
)

from fastapi_datamodel_template import CalculationResult

# from microgrid_base.ies_optim import EnergyFlowGraph
# from celery.exceptions import Ignore
from ies_optim import 计算年化率

@app.task()
# @app.task(bind=True)  # parse it elsewhere.
def calculate_energyflow_graph(energyflow_graph: dict) -> Union[None, dict]:
    # def calculate_energyflow_graph(self, energyflow_graph: dict) -> Union[None, dict]:
    # raise Exception("ERROR MSG")
    # error_name = "ERROR_NAME"; error_log = 'ERROR_LOG'
    # self.update_state(
    #     state="FAILURE", meta={"exc_type": error_name, "exc_message": error_log, 'custom':'...'}
    # )  # https://distributedpython.com/posts/custom-celery-task-states/
    # raise Ignore()
    """
    能源系统仿真优化计算方法

    Args:
        energyflow_graph (dict): 能流拓扑图和计算所需信息

    Returns:
        calculation_result (dict): 计算结果
    """
    mDictList = energyflow_graph["mDictList"]
    辅助设备寿命 =  energyflow_graph['residualEquipmentLife']
    贴现率 = mDictList[0]['graph']['贴现率']
    辅助设备年化系数 = 计算年化率(贴现率, 辅助设备寿命)

    calcParamList = mDictListToCalcParamList(mDictList)

    resultList = []
    # error_log = ""
    # success = False
    # error_name = None
    # try:
    resultList = solveModelFromCalcParamList(calcParamList)
    # except Exception as ex:
    # import traceback

    # error_log = traceback.format_exc()
    # error_name = type(ex).__name__
    # print("************CELERY ERROR************")
    # print(error_log)

    if resultList != []:
        # success = True
        calculation_result = CalculationResult(
            resultList=resultList, success=True, error_log="",residualEquipmentAnnualFactor = 辅助设备年化系数 # TODO: 计算辅助设备年化参数
        ).dict()
        return calculation_result
    else:
        raise Exception("Empty result list.")
        # calculation_result = CalculationResult(
        #     error_log = "Empty result list.", resultList=resultList, success=False,
        # )
        # self.update_state(
        #     state="FAILURE", meta={"exc_type": error_name, "exc_message": error_log, 'custom':'...'}
        # )  # https://distributedpython.com/posts/custom-celery-task-states/
        # raise Ignore()


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
