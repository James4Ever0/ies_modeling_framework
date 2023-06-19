from typing import Protocol, Any, Generic, TypeVar, runtime_checkable, cast

T = TypeVar("T")

class ArithmaticType(Protocol):
    """
    Protocol of which able to do arithmatic operations.
    """
    
    def __add__(self, v, /) -> Any:
        ...
        
    def __sub__(self, v, /) -> Any:
        ...
        
    def __mul__(self, v, /) -> Any:
        ...
        
    def __div__(self, v, /) -> Any:
        ...
        
    def __eq__(self, v, /) -> Any: ...
    def __ne__(self, v, /) -> Any: ...
    def __le__(self, v, /) -> Any: ...
    def __ge__(self, v, /) -> Any: ...

class Subscripable(Protocol):
    def __getitem__(self, index:int, /) -> Any: ...

class 

@runtime_checkable
class AddAndLength(Protocol):
    def __add__(self, v, /) -> Any:
        ...

    def __len__(self) -> Any:
        ...


def mfunc(param: AddAndLength) -> int:
    print("You don't care what I do")
    length = len(param)
    print("LEN:", length)
    return length


# mfunc(123)
mfunc(["i am list"])
a: AddAndLength
a = []
# a = 123
from pyomo.environ import *

model = ConcreteModel()

model.x = cast(Subscripable,Var([0,1,2]))
model.x:  # type: ignore
model.x[1]
model.v = cast(ArithmaticType, Var())
val = model.v * 1