## suggestion: use fastapi for self-documented server, use cerely for task management.

## question: how to convert pydantic models to json?

# 在Python中，你可以使用 json.dumps() 函数将Pydantic模型转换为JSON字符串。以下是一个示例代码：

# python
# Copy code
# import json
# from pydantic import BaseModel
# class Item(BaseModel):
#     name: str
#     description: str = None
#     price: float
#     tax: float = None
# item = Item(name='test', price=9.99)
# json_str = json.dumps(item.dict())
# print(json_str)

# 在上述示例代码中，我们定义了一个名为 Item 的Pydantic模型，然后创建了一个 Item 实例对象。接下来，我们将 item 对象的字典形式转换为JSON字符串，通过 json.dumps() 函数实现，并打印输出结果。
# 需要注意的是，如果你的Pydantic模型中有可选字段，如示例代码中的 description 和 tax 字段，那么在将模型转换为字典时，这些可选字段将成为字典中的键值对。如果可选字段的值为 None，则在转换为JSON字符串时，这些键值对将不会出现在JSON字符串中。


port = 9870
host = "0.0.0.0"

appName = "IES Optim Server Template"
version = "0.0.1"
tags_metadata = []
description = f"""
IES系统仿真和优化算法服务器

OpenAPI描述文件：https://{host}:{port}/openapi.json
API文档：https://{host}:{port}/docs
"""


from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Mapping, List, Tuple

from fastapi_server_with_doc import Item


# to json: json.dumps(model.dict())
class EnergyFlowGraph(BaseModel):
    """
    用于仿真和优化计算的能流拓扑图，仿真和优化所需要的参数模型和变量定义会有所不同。
    """

    graph: Mapping = Field(title="能流拓扑图的附加属性", description="仿真和优化所需的整体模型参数字典", example={""})
    nodes: List[Mapping] = Field(
        title="节点", description="由所有节点ID和属性（可选）字典组成的列表", example=[{'id':1, 'node_type':"load"},{'id':2, 'node_type'}]
    )
    adjacency: List[List[Mapping]] = Field(
        title="边", description="由能流图中节点互相连接的边组成的列表", example=[]
    )

    def to_graph(cls):
        graph: List[Tuple] = [(k, v) for k, v in cls.graph.items()]
        graph_dict = dict(
            directed=False,
            multigraph=False,
            graph=graph,
            nodes=cls.nodes,
            adjacency=cls.adjacency,
        )
        return graph_dict


app = FastAPI(description=description, version=version, tags_metadata=tags_metadata)


@app.post("/items/")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


import uvicorn

uvicorn.run(app, host=host, port=port)
