from topo_check import *

###############
# build from code.
###############

# you may need pydantic here. verify then import to compute graph.
topo = 拓扑图(计算步长="小时", 计算模式="典型日")  # with structure?

PV1 = 光伏发电(topo, 面积=2)  # 这种是增加新的光伏发电
LOAD = 电负荷(topo, 功率=3000)

连接线(topo, "", PV1.电接口, LOAD.电接口)  # connected?

L1 = 母线(graph)

# walk over all connections.

conn = 连接线(graph, PV.ports["电接口"], LOAD.ports["电接口"])

conn_merge = 合并线(L0, L1)  # what do you do?

# shall raise error.

# methods for computing.

devs = graph.get_all_devices()

# device, ports, device_data

adders = graph.get_all_adders()

# input, output, io

###############
# dump to dict
###############

mdict = graph.to_json()

###############
# load from dict
###############

graph_load = graph.from_json(mdict)  # static method

# how to check error now?
# all connected?

## COMPUTE THIS GRAPH ##
# use devs, adders

graph_data = graph.get_graph_data()

# objective is contained in the graph data.
# so all we need to pass to the compute function are: devs, adders, graph_data

from ies_optim import compute

result = compute(devs, adders, graph_data)
