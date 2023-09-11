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

result = PersonFactory.build()
print(result)

# random.seed(100)

# result = PersonFactory.build()
# print(result)

##############################################################

from dataclasses import dataclass
from random import Random

from polyfactory.factories import DataclassFactory


@dataclass
class Person:
    name: str
    age: float
    height: float
    weight: float


class PersonFactory(DataclassFactory[Person]):
    __model__ = Person
    __random__ = Random(
        10
    )  # this is not really deterministic, unless you manually specify sampling logic

    # @classmethod
    # def name(cls) -> str:
    #     return cls.__random__.choice(["John", "Alice", "George"])


p = PersonFactory.build()
print(p)

p = PersonFactory.build()
print(p)


# def test_setting_random() -> None:
#     # the outcome of 'factory.__random__.choice' is deterministic, because Random is configured with a set value.
#     assert PersonFactory.build().name == "George"
#     assert PersonFactory.build().name == "John"
#     assert PersonFactory.build().name == "Alice"

from fastapi_datamodel_template import 单次计算结果

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
calcTarget = input_data.mDictList[0].计算目标

if calcTarget == "经济_环保":
    ...
elif calcTarget in ["经济", "环保"]:
    ...
else:
    raise Exception("Unknown calculation target: %s" % calcTarget)
# for _ in ...:
#     单次计算结果
