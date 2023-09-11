# import os
# import random

# def urandom_deterministic(__size:int):
#     return random.randbytes(__size)

# # override system rng.
# os.urandom = urandom_deterministic

from datetime import date, datetime
from typing import List, Union

from pydantic import BaseModel, UUID4

from pydantic_factories import ModelFactory


class Person(BaseModel):
    id: UUID4
    name: str
    hobbies: List[str]
    age: Union[float, int]
    birthday: Union[datetime, date]


class PersonFactory(ModelFactory):
    __model__ = Person
    # not working!
    # __random_seed__ = 100


# not working.
# import random

# random.seed(100)
PersonFactory.seed_random(100)  # working again!

result = PersonFactory.build()
print(result)
# exit()
# random.seed(100)

# result = PersonFactory.build()
# print(result)

##############################################################

from dataclasses import dataclass

# from random import Random

from polyfactory.factories import DataclassFactory


@dataclass
class Person:
    name: str
    age: float
    height: float
    weight: float


class PersonFactory(DataclassFactory[Person]):
    __model__ = Person
    # __random__ = Random(
    #     10
    # )  # this is not really deterministic, unless you manually specify sampling logic

    # @classmethod
    # def name(cls) -> str:
    #     return cls.__random__.choice(["John", "Alice", "George"])


PersonFactory.seed_random(b"\x00\x01")
# PersonFactory.seed_random(100) # working!
p = PersonFactory.build()
print(p)

p = PersonFactory.build()
print(p)

# exit()
# def test_setting_random() -> None:
#     # the outcome of 'factory.__random__.choice' is deterministic, because Random is configured with a set value.
#     assert PersonFactory.build().name == "George"
#     assert PersonFactory.build().name == "John"
#     assert PersonFactory.build().name == "Alice"

from fastapi_datamodel_template import (
    单次计算结果,
    CalculationResult,
    ObjectiveResult,
    规划结果详情_翻译,
    规划方案概览_翻译,
    设备出力曲线,
    仿真结果,
    出力曲线,
    曲线,
)

# not working. but we can do this later.
# class 单次计算结果工厂(ModelFactory):
#     __model__ = 单次计算结果

# cr = 单次计算结果工厂.build()
# print(cr)

# create output based on input.
from ies_optim import EnergyFlowGraph


# class EnergyFlowGraphFactory(ModelFactory):
#     __model__ = EnergyFlowGraph

# input_data = EnergyFlowGraphFactory.build()
# print(input_data)

# with open(mock_input:='mock_data_energy_flow_graph.json', 'w+') as f:
#     f.write(input_data.json())
# print('write to:', mock_input)


mock_input = "mock_data_energy_flow_graph.json"
input_data = EnergyFlowGraph.parse_file(mock_input)
print(input_data)

# seed input

import random
from config import ies_env


firstMDict = input_data.mDictList[0]
calcTarget = firstMDict.计算目标

if calcTarget == "经济_环保":
    mDictCount = 9
elif calcTarget in ["经济", "环保"]:
    mDictCount = 1
else:
    raise Exception("Unknown calculation target: %s" % calcTarget)
from solve_model import targetTypeAsTargetName

planType = targetTypeAsTargetName(calcTarget)
resultList = []

class 规划方案概览_翻译_工厂(DataclassFactory[规划方案概览_翻译]):
    __model__ = 规划方案概览_翻译

class 规划结果详情_翻译_工厂(DataclassFactory[规划结果详情_翻译]):
    __model__ = 规划结果详情_翻译

class 仿真结果工厂(DataclassFactory[仿真结果]):
    __model__ = 仿真结果

if ies_env.DETERMINISTIC_MOCK:
    import hashlib

    input_bytes = input_data.json().encode("utf-8")
    input_hash = hashlib.sha1(input_bytes).digest()
    random.seed(input_hash)
    规划方案概览_翻译_工厂.seed_random(input_hash)
    规划结果详情_翻译_工厂.seed_random(input_hash)
    仿真结果工厂.seed_random(input_hash)

for _ in range(mDictCount):
    obj_r = ObjectiveResult(
        financialObjective=random.uniform(10, 1000),
        environmentalObjective=random.uniform(10, 1000),
    )
    prt = []
    ps = 规划方案概览_翻译_工厂.build()
    ps.planType = planType
    pdl = []
    srt = []

    for elem in firstMDict.nodes:
        if elem.get("type") == "设备":
            subtype = elem.get("subtype")
            param = elem.get("param")
            设备名称, 生产厂商, 设备型号 = (
                param.get("设备名称", "未知"),
                param.get("生产厂商", "未知"),
                param.get("设备型号", "未知"),
            )
            px = []
            py = []
            pcurve = 曲线(x=px, y=py)
            pl = [出力曲线(name=..., abbr=..., data=pcurve)]
            pr = 规划结果详情_翻译_工厂.build()
            pr.deviceName = 设备名称
            pr.deviceModel = 设备型号
            pd = 设备出力曲线(name=..., plot_list=pl)
            sr = 仿真结果工厂.build()
            sr.name = 设备名称
            sr.type = 设备型号
            prt.append(pr)
            pdl.append(pd)
            srt.append(sr)

    result = 单次计算结果(
        objectiveResult=obj_r,
        plannintResultTable=prt,
        planningSummary=ps,
        performanceDataList=pdl,
        simulationResultTable=srt,
    )
    resultList.append(result)

cr = CalculationResult(
    resultList=resultList,
    residualEquipmentAnnualFactor=random.uniform(0, 5),
    success=True,
    error_log="",
)

# finally, pass to the number manipulation routines.

from reduce_demo_data_size import modifyValueIfNumber, modifyIfIsDeviceCount
from json_utils import jsonApply

processed_cr = jsonApply(cr.dict(), modifyValueIfNumber, modifyIfIsDeviceCount)
pcr_obj = CalculationResult.parse_obj(processed_cr)
print(pcr_obj)