from typing import Union
from ies_optim import 计算年化率

from solve_model import (
    solveModelFromCalcParamList,
    mDictListToCalcParamList,
)
from log_utils import logger_print

from fastapi_datamodel_template import CalculationResult

def calculate_energyflow_graph_base(energyflow_graph: dict) -> Union[None, dict]:
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
    resultList = solveModelFromCalcParamfList(calcParamList)
    # except Exception as ex:
    # import traceback

    # error_log = traceback.format_exc()
    # error_name = type(ex).__name__
    # logger_print("************CELERY ERROR************")
    # logger_print(error_log)

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
