input_path = ""

import json

with open(input_path,'r') as f:
    data = json.load(f)

from ies_optim import EnergyFlowGraph
from topo_check import 拓扑图

EFG = EnergyFlowGraph.parse_obj(data)