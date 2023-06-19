from typing import Protocol, Any, Generic, TypeVar, runtime_checkable, cast

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

model.v  = Var()
model.x = cast(Generic)
model.x:  # type: ignore
model.x[1]
model.v= cast(float, Var([0,1,2]))
val = model.v * 1