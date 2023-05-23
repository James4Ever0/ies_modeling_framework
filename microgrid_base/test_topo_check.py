from topo_check import ...

###############
# build from code.
###############
graph = 拓扑图()

PV1 = graph.光伏发电(**kwargs) # 这种是增加新的光伏发电

graph.连接线(PV1.电接口, LOAD.电接口) # connected?

PV = 设备(graph, "光伏发电", port_definition = {"电接口":"供电端输出"})

LOAD = 设备(graph, "电负荷", port_definition = {"电接口":"供电端输出"})

conn = 连接线(graph, PV.ports['电接口'], LOAD.ports['电接口'])
# walk over all connections.

L1 = 母线(graph)

连接线

conn_merge = 合并线(L0, L1)

# shall raise error.

###############
# dump to dict
###############

mdict = graph.to_json()

###############
# load from dict
###############

graph_load = graph.from_json(mdict) # static method

# how to check error now?
# all connected?