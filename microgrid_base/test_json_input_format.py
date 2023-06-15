input_path = ""

import json

with open(input_path,'r') as f:
    data = json.load(f)

from ies_optim import EnergyFlowGraph
from topo_check import 拓扑图

EFG = EnergyFlowGraph.parse_obj(data)

EFG_dict = EFG.dict()

EFG2 = EnergyFlowGraph.parse_obj(EFG_dict)

import rich
for index, mDict in enumerate(EFG.mDictList):
    print(f'parsing mDict #{index}')
    topo = 拓扑图.from_json(mDict.dict())