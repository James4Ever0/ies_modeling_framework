# input_path = "test_data.json"
input_path = "test/test_topo.json"
# input_path = "template_input.json"
# input_path = "test/missing_param_input_dieselgenerator.json"
# input_path = "test/lithion_battery.json"
import json

with open(input_path, "r") as f:
    data = json.load(f)
    # data = dict(mDictList=json.load(f))

from ies_optim import EnergyFlowGraph
from topo_check import 拓扑图

EFG = EnergyFlowGraph.parse_obj(data)

EFG_dict = EFG.dict()

EFG2 = EnergyFlowGraph.parse_obj(EFG_dict)

import rich

from solve_model import mDictListToCalcParamList, solveModelFromCalcParamList

for index, mDict in enumerate(EFG.mDictList):
    rich.print(mDict)
    print()
    print(f"_____parsing mDict #{index}_____")
    topo = 拓扑图.from_json(mDict.dict())
    topo.check_consistency()

mDictList = EFG.dict()["mDictList"]
calcParamList = mDictListToCalcParamList(mDictList)
resultList = solveModelFromCalcParamList(calcParamList)
# breakpoint()
rich.print(resultList[0]["simulationResultTable"])

with open("export_format_test.json", "w") as f:
    f.write(json.dumps(resultList, indent=4, ensure_ascii=False))
