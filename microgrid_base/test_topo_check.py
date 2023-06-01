import json
from topo_check import *
import rich
###############
# build from code.
###############

# FIXED: 加法器没有"output"

def print_with_banner(data, banner:str):
    print()
    print("="*40+f"[{banner}]")
    rich.print(data)
    print()

# you may need pydantic here. verify then import to compute graph.
topo = 拓扑图(计算步长="小时", 计算模式="典型日")  # with structure?

PV1 = 光伏发电(topo, 面积=2)  # 这种是增加新的光伏发电
PV2 = 光伏发电(topo, 面积=2)  # 这种是增加新的光伏发电
DEL1 = 变流器(topo)
DEL2 = 变压器(topo)
LOAD = 电负荷(topo, 功率=3000)

BAT = 锂电池(topo)

A1 = 母线(topo, "可连接供电端母线")
A2 = 母线(topo, "可连接供电端母线")
A3 = 母线(topo, "可连接电母线")

BC = 双向变流器(topo)

连接线(topo, "不可连接电储能端母线", BC.储能端, BAT.电接口)
连接线(topo, "不可连接电母线输入输出", BC.线路端, A3.id)

连接线(topo, "不可连接电母线输入", DEL1.电输出, A3.id)
连接线(topo, "不可连接电母线输出", A3.id, DEL2.电输入)

连接线(topo, "不可连接负荷电母线",DEL2.电输出, LOAD.电接口)

连接线(topo, "不可连接供电端母线输入", A1.id, PV1.电接口)
连接线(topo, "不可连接供电端母线输入", A2.id,  PV2.电接口)
连接线(topo, "不可连接供电端母线输出", A2.id, DEL1.电输入)

合并线(topo, "可合并供电端母线", A1.id, A2.id)

# L1 = 母线(graph)

# # walk over all connections.

# conn = 连接线(graph, PV.ports["电接口"], LOAD.ports["电接口"])

# conn_merge = 合并线(L0, L1)  # what do you do?
topo.check_consistency()
# shall raise error.

# methods for computing.

devs = topo.get_all_devices()
print_with_banner(devs, "设备")
# {
#     'type': '设备',
#     'subtype': '双向变流器',
#     'ports': {
#         '线路端': {'subtype': '双向变流器线路端输入输出', 'id': 18},
#         '储能端': {'subtype': '双向变流器储能端输入输出', 'id': 19}
#     }
# }

# device, ports, device_data

adders = topo.get_all_adders()
print_with_banner(adders, "加法器")
# input, output, io
# {
#     16: {'input': [6], 'output': [9], 'IO': [18]},
#     14: {'input': [1, 3], 'output': [5], 'IO': []},
#     -1: {'input': [], 'output': [], 'IO': [19, 13]},
#     -2: {'input': [8], 'output': [11], 'IO': []}
# }

###############
# dump to dict
###############

mdict = topo.to_json()
print_with_banner(mdict, "图序列化")
with open("template_input.json",'w+') as f:
    f.write(json.dumps(mdict, ensure_ascii=False, indent=4))

###############
# load from dict
###############

topo_load = topo.from_json(mdict)  # static method
print_with_banner(topo_load, "图对象")
# how to check error now?
# all connected?

topo_load.check_consistency() # may still be good.
## COMPUTE THIS GRAPH ##
# use devs, adders

graph_data = topo.get_graph_data()
print_with_banner(graph_data, "图元数据")
# objective is contained in the graph data.
# so all we need to pass to the compute function are: devs, adders, graph_data
import sys

def 

if sys.argv[-1] in ['-f',"--full"]:
    from ies_optim import compute
    from pyomo.environ import *
    model = ConcreteModel()
    obj_expr, devInstDict, PD= compute(devs, adders, graph_data, topo.G, model)
