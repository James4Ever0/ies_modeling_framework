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
from microgrid_base.solve_model import solveModelFromCalcParamList, mDictListToCalcParamList

# define the input structure here.
from pydantic import BaseModel
from typing import List
class mDict(BaseModel):

class EnergyFlowGraph(BaseModel):
    mDictList: List[mDict]

# solved or not?

class CalculationResult(BaseModel):
    resultList:List
    success:bool=True
    error_log:str=""

@app.task
def calculate_energyflow_graph(energyflow_graph: EnergyFlowGraph) -> dict:
    """
    能源系统仿真优化计算方法

    Args:
        energyflow_graph (EnergyFlowGraph): 能流拓扑图和计算所需信息

    Returns:
        calculation_result (dict): 计算结果
    """
    mDictList = energyflow_graph.dict()['mDictList']
    calcParamList = mDictListToCalcParamList(mDictList)
    
    calculation_result = dict(result = None)
    try:
        resultList = solveModelFromCalcParamList(calcParamList)
    except:
        import traceback
        ftb = traceback.format_exc()
        print(ftb)
    ...
    return calculation_result


app.conf.update(task_track_started=True)
app.conf.update(worker_send_task_events=True)
concurrent_tasks = 3
app.conf.update(worker_concurrency=concurrent_tasks)
memory_limit = 20_000_000  # kB
app.conf.update(worker_max_memory_per_child=memory_limit)
time_limit = 60 * 10  # sec
app.conf.update(worker_time_limit=time_limit)
# limits on ram usage, concurrency, execution time

if __name__ == "__main__":
    worker = app.Worker()
    worker.start()
