from typing import Protocol, Any, Generic, TypeVar, runtime_checkable

T = TypeVar("T")


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

model.v  = Var('v')
model.v * 1