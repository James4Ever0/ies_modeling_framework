from pydantic import BaseModel, Field
from networkx.readwrite import json_graph
from typing import Mapping, List, Tuple, Literal, Union
import networkx
# from celery.states import PENDING, RECEIVED, STARTED, SUCCESS, FAILURE, RETRY, REVOKED

# question: how to convert pydantic models to json?
# to json: json.dumps(model.dict())
from microgrid_base.ies_optim import EnergyFlowGraph

class CalculationResult(BaseModel):
    resultList:List
    success:bool
    error_log:str

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
    calculation_state: Literal[None, "PENDING", "RECEIVED", "STARTED", "SUCCESS", "FAILURE", "RETRY", "REVOKED", 'NOT_CREATED'] = Field(description="Celery内置任务状态，如果是null则表示不存在该任务", title="计算任务状态")
# would you transfer this thing over celery, or you need to build it?
# i'd rather build it.
class CalculationAsyncResult(CalculationStateResult):
    """
    异步计算任务查询返回结果
    """

    calculation_result: Union[None, dict] = Field(description="如果没有计算完或者不存在返回空，否则返回计算结果字典", title="计算结果")


class RevokeResult(CalculationStateResult):
    """
    撤销返回结果
    """

    revoke_result: Literal["success", "failed"] = Field(
        description='如果成功撤销任务，返回"success"，否则返回"failed"', title="撤销结果"
    )