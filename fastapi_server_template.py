# suggestion: use fastapi for self-documented server, use celery for task management.
# celery reference: https://github.com/GregaVrbancic/fastapi-celery/blob/master/app/main.py

port = 9870
host = "0.0.0.0"

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

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Mapping, List, Tuple


# question: how to convert pydantic models to json?
# to json: json.dumps(model.dict())
#
class EnergyFlowGraph(BaseModel):
    """
    用于仿真和优化计算的能流拓扑图，仿真和优化所需要的参数模型和变量定义会有所不同。
    """

    graph: Mapping = Field(
        title="能流拓扑图的附加属性",
        description="仿真和优化所需的模型参数字典",
        examples=dict(
            建模仿真=dict(
                summary="建模仿真所需参数",
                description="建模仿真需要知道仿真步长和起始时间",
                value={
                    "模型类型": "建模仿真",
                    "仿真步长": 60,
                    "开始时间": "2023-3-1",
                    "结束时间": "2024-3-1",
                },
            ),
            规划设计=dict(
                summary="规划设计所需参数",
                description="规划设计不需要知道仿真步长和起始时间,会根据不同优化指标事先全部计算，不需要在此指出",
                value={"模型类型": "规划设计"},
            ),
        ),
    )
    nodes: List[Mapping] = Field(
        title="节点",
        description="由所有节点ID和属性字典组成的列表",
        example=[
            {"id": "a", "node_type": "load"},
            {"id": "b", "node_type": "device"},
            {"id": "c", "node_type": "load"},
            {"id": "d", "node_type": "port", "port_type": "AC"},
            {"id": "e", "node_type": "port", "port_type": "AC"},
            {"id": "f", "node_type": "port", "port_type": "AC"},
        ],
    )
    adjacency: List[List[Mapping]] = Field(
        title="边",
        description="由能流图中节点互相连接的边组成的列表",
        example=[
            [{"id": "b"}, {"id": "d"}],
            [{"id": "a"}, {"id": "e"}],
            [{"id": "c"}, {"id": "f"}],
            [{"id": "d"}, {"id": "e"}],
            [{"id", "d"}, {"id": "f"}],
        ],
    )

    def to_graph(self) -> Mapping:
        """
        输出可加载到`networkx`生成计算图的字典
        
        转换代码：
        ```python
        import networkx as nx
        from networkx.readwrite import json_graph
        
        ```
        
        Returns:
            graph_dict(Mapping): 字典，键值为`["directed", "multigraph", "graph", "nodes", "adjacency"]`
        """
        graph: List[Tuple] = [(k, v) for k, v in self.graph.items()]
        graph_dict = dict(
            directed=False,
            multigraph=False,
            graph=graph,
            nodes=self.nodes,
            adjacency=self.adjacency,
        )
        return graph_dict


app = FastAPI(description=description, version=version, tags_metadata=tags_metadata)

class CalculationAsyncSubmitResult(BaseModel):
    """
    """
    calculation_id: ... = Field(description="", title="")
    submit_state: ...= Field(description="", title="")

@app.post(
    "/calculate_async",
    tags=["async"],
    description="填写数据并提交拓扑图，如果还有计算资源，提交状态为成功，返回计算ID，否则不返回计算ID，提交状态为失败",
    summary="异步提交能流拓扑图",
    response_description="提交状态以及模型计算ID,根据ID获取计算结果",
    response_model = CalculationAsyncSubmitResult
)
def calculate_async(graph: EnergyFlowGraph):
    # use celery
    return calculation_id



class CalculationAsyncResult(BaseModel):
    """
    """
    calculation_result: ... = Field(description="", title="")
    calculation_state: ...= Field(description="", title="")


@app.get(
    "/get_calculation_result_async",
    tags=["async"],
    description="提交计算ID，返回计算状态，如果计算完毕会一起返回数据，否则数据为空",
    summary="异步获取能流拓扑计算结果",
    response_description="计算状态和计算结果",
    response_model = CalculationAsyncResult
)
def get_calculation_result_async(calculation_id):
    return calculation_result


import uvicorn

uvicorn.run(app, host=host, port=port)
