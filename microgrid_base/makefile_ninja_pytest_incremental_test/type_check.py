from typing import Any, Generic, Protocol, TypeVar, cast, runtime_checkable

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

    def __eq__(self, v, /) -> Any:
        ...

    def __ne__(self, v, /) -> Any:
        ...

    def __le__(self, v, /) -> Any:
        ...

    def __ge__(self, v, /) -> Any:
        ...


class ReadableBySubscription(Protocol):
    def __getitem__(self, index: int, /) -> Any:
        ...


class Subscripable(ReadableBySubscription, Protocol):
    def __setitem__(self, index: int, /) -> Any:
        ...


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

model.x:ReadableBySubscription= Var([0, 1, 2])
# model.x = cast(ReadableBySubscription, Var([0, 1, 2]))

model.x[1]
model.v = cast(ArithmaticType, Var())
val = model.v * 1
