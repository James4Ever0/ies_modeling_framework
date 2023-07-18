from pydantic import BaseModel, Field, validator, confloat
from networkx.readwrite import json_graph
from typing import Mapping, List, Tuple, Union, Dict, Any
import networkx
from constants import *

try:
    from typing import Literal
except:
    from typing_extensions import Literal


try:
    from typing import assert_never
except:
    from typing_extensions import assert_never


# from celery.states import PENDING, RECEIVED, STARTED, SUCCESS, FAILURE, RETRY, REVOKED

# question: how to convert pydantic models to json?
# to json: json.dumps(model.dict())
from ies_optim import EnergyFlowGraph, 仿真结果


class 曲线(BaseModel):
    x: List[str] = Field(title="x轴数据")
    y: List[float] = Field(title="y轴数据")

    @validator("x")
    def validate_x(cls, x: List[str]):
        """
        Validate the input list of strings `x` and return the validated list.

        Args:
            cls: The class of the validator.
            x (List[str]): The input list of strings to be validated.

        Returns:
            List[str]: The validated list of strings.

        Raises:
            Exception: If the input list `x` is not valid.
        """
        suffixMapping = {两小时秒数: "秒", 每年小时数: "时"}
        for suffix in suffixMapping.values():
            if x[0].endswith(suffix):
                return x
        len_x = len(x)
        if len_x in suffixMapping.keys():
            suffix = suffixMapping[len_x]
            x = [e + suffix for e in x]
            return x
        else:
            raise Exception("Non-standard x array length:", len_x)


class 出力曲线(BaseModel):
    name: str = Field(title="出力曲线标题")
    # device_name: str = Field(title = "设备名称")
    abbr: str = Field(title="出力曲线缩写")
    data: 曲线 = Field(title="曲线数据")


class 设备出力曲线(BaseModel):
    name: str = Field(title="设备名称")
    plot_list: List[出力曲线] = Field(title="出力曲线列表")


class ObjectiveResult(BaseModel):
    financialObjective: float = Field(title="经济目标值")
    environmentalObjective: float = Field(title="环保目标值")


class 单次计算结果(BaseModel):
    objectiveResult: ObjectiveResult = Field(
        title="计算目标值结果",
        description="存放例如经济目标值、环保目标值的计算结果",
        example={"financialObjective": 2000, "environmentalObjective": 3000},
    )
    planningResultTable: List[规划结果详情] = Field( title='规划结果详情列表', description = '方案内各机组信息') 
    planningSummary: List[规划方案概览] = Field(title= '规划方案概览', description = '包括方案类型，方案总参数等等')
    performanceDataList: List[设备出力曲线] = Field(
        title="设备出力曲线列表",
        description= "每个设备逐步长出力情况",
        example=[
            {
                "name": "Any",
                "plot_list": [
                    {
                        "name": "plotName",
                        "abbr": "plotAbbr",
                        "data": {"x": [], "y": []},
                    }
                ],
            }
        ],
    )
    simulationResultTable: List[仿真结果] = Field(
        title="仿真结果列表",
        example=[
            {
                "name": "Any",
                "modelNumber": "Any",
                "equiCounts": 1,
                "coolingCapacity": 1,
                "coolingLoad": 1,
                "electricSupply": 1,
                "electricLoad": 1,
                "heatingLoad": 1,
                "heatLoad": 1,
                "steamProduction": 1,
                "steamLoad": 1,
                "hydrogenProduction": 1,
                "hydrogenConsumption": 1,
                "dieselConsumption": 1,
                "dieselConsumptionCosts": 1,
                "naturalGasConsumption": 1,
                "naturalGasConsumptionCosts": 1,
                "averageEfficiency": 1,
                "equipmentMaintenanceCosts": 1,
                "coldIncome": 1,
                "hotIncome": 1,
                "eletricncome": 1,
                "steamIncome": 1,
                "hydrogenIncome": 1,
            }
        ],
    )

class ParetoCurve(BaseModel):
    x: List[float]
    x_label: str
    y: List[float]
    y_label: str


# you need to check if any "Field" is using "default" positional argument, which might leads to error.
class CalculationResult(BaseModel):
    resultList: List[单次计算结果]
    paretoCurve: Union[None, ParetoCurve] = None
    residualEquipmentAnnualFactor: confloat(ge=0) = Field(
        default=0, title="辅助设备年化系数", description="仿真模拟是0，设计规划为非0"
    )
    success: bool
    error_log: str


# class EnergyFlowGraph(BaseModel):
#     """
#     用于仿真和优化计算的能流拓扑图，仿真和优化所需要的参数模型和变量定义会有所不同。
#     """

#     graph: Mapping = Field(
#         title="能流拓扑图的附加属性",
#         description="仿真和优化所需的模型参数字典",
#         examples=dict(
#             建模仿真=dict(
#                 summary="建模仿真所需参数",
#                 description="建模仿真需要知道仿真步长和起始时间",
#                 value={
#                     "模型类型": "建模仿真",
#                     "仿真步长": 60,
#                     "开始时间": "2023-3-1",  # shall you parse this into `datetime.datetime`
#                     "结束时间": "2024-3-1",
#                 },
#             ),
#             规划设计=dict(
#                 summary="规划设计所需参数",
#                 description="规划设计不需要知道仿真步长和起始时间,会根据不同优化指标事先全部计算，不需要在此指出",
#                 value={"模型类型": "规划设计"},
#             ),
#         ),
#     )
#     nodes: List[Mapping] = Field(
#         title="节点",
#         description="由所有节点ID和属性字典组成的列表",
#         example=[
#             {"id": "a", "node_type": "load"},
#             {"id": "b", "node_type": "device"},
#             {"id": "c", "node_type": "load"},
#             {"id": "d", "node_type": "port", "port_type": "AC"},
#             {"id": "e", "node_type": "port", "port_type": "AC"},
#             {"id": "f", "node_type": "port", "port_type": "AC"},
#         ],
#     )
#     adjacency: List[List[Mapping]] = Field(
#         title="边",
#         description="由能流图中节点互相连接的边组成的列表",
#         example=[
#             [{"id": "b"}, {"id": "d"}],
#             [{"id": "a"}, {"id": "e"}],
#             [{"id": "c"}, {"id": "f"}],
#             [{"id": "d"}, {"id": "e"}],
#             [{"id", "d"}, {"id": "f"}],
#         ],
#     )

#     def to_graph(self, directed=False) -> networkx.Graph:
#         """
#         输出`networkx`计算图

#         Arguments:
#             directed (bool): 是否返回有向图

#         Returns:
#             G (Graph): `networkx`计算图
#         """
#         graph: List[Tuple] = [(k, v) for k, v in self.graph.items()]
#         graph_dict = dict(
#             directed=directed,
#             multigraph=False,
#             graph=graph,
#             nodes=self.nodes,
#             adjacency=self.adjacency,
#         )

#         G = json_graph.adjacency_graph(graph_dict, directed=directed)

#         return G


class CalculationAsyncSubmitResult(BaseModel):
    """
    异步计算提交结果返回类
    """

    calculation_id: Union[None, str] = Field(
        description="如果成功注册计算任务，返回ID，否则为空", title="计算ID"
    )
    submit_result: Literal["success", "failed"] = Field(
        description='如果成功提交，返回"success"，否则返回"failed"', title="提交结果"
    )


class CalculationStateResult(BaseModel):
    """
    包含计算任务状态的数据类
    """

    calculation_state: Literal[
        None,
        "PENDING",
        "RECEIVED",
        "STARTED",
        "SUCCESS",
        "FAILURE",
        "RETRY",
        "REVOKED",
        "NOT_CREATED",
    ] = Field(description="Celery内置任务状态，如果是null则表示不存在该任务", title="计算任务状态")


# would you transfer this thing over celery, or you need to build it?
# i'd rather build it.
class CalculationAsyncResult(CalculationStateResult):
    """
    异步计算任务查询返回结果
    """

    calculation_result: Union[None, CalculationResult] = Field(
        description="如果没有计算完或者不存在返回空，否则返回计算结果字典", title="计算结果"
    )


class RevokeResult(CalculationStateResult):
    """
    撤销返回结果
    """

    revoke_result: Literal["success", "failed"] = Field(
        description='如果成功撤销任务，返回"success"，否则返回"failed"', title="撤销结果"
    )
