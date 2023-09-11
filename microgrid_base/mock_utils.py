"""
This library mocks algorithm response.

Hash input parameters for random seeds.
"""
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

import ran
# random.seed(100)

# result = PersonFactory.build()
# print(result)