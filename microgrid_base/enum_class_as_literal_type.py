from enum import StrEnum
a = StrEnum('Color', ['RED', 'GREEN', 'BLUE'])
# from enum import Enum
# a = Enum('Color', ['RED', 'GREEN', 'BLUE'])

b: a = a.BLUE # Color.BLUE
print(b, type(b))
# assert (b == 'blue2') # false
assert (b == 'blue') # true

from pydantic import BaseModel
class A(BaseModel):
    a0: a

# data = A(a0 = "blue") # though type error, still working
data = A(a0 = "blue2")
# data = A(a0 = a['BLUE']) # nothing received.
print('data',data, data.a0)