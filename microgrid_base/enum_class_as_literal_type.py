# from enum import StrEnum
# a = StrEnum('Color', ['RED', 'GREEN', 'BLUE'])
from enum import Enum
# a = Enum('Color', ['RED', 'GREEN', 'BLUE'])
from typing import Literal
class a(Enum):
    RED='red'
    GREEN='green'
    BLUE='blue'

b: a = a.BLUE # Color.BLUE
print(b, type(b))
# will be converted into lower case.
# assert (b == 'blue2') # false
assert (b == 'blue') # true

from pydantic import BaseModel
class A(BaseModel):
    a0: a
data = A(a0 = 'blue') # though static type error, still working
# data = A(a0 = "blue2") # validation error.
# data = A(a0 = a['BLUE']) # working
print('data',data, data.a0)