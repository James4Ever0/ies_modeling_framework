from topo_check import ...

###############
# build from code.
###############
graph = 拓扑图()

PV = 设备(graph, "光伏发电", port_definition = {"电接口":"供电端输出"})

LOAD = 设备(graph, "电负荷", port_definition = {"电接口":"供电端输出"})

conn = 连接线(PV.ports['电接口'])

, 

###############
# dump to dict
###############


###############
# load from dict
###############