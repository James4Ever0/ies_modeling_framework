from typing import (
    Any,
    Generic,
    Protocol,
    TypeVar,
    cast,
    overload,
    runtime_checkable,
    NewType,
)
from typing_extensions import Never

from collections import namedtuple

# from typing import NamedTuple
from typing_extensions import TypeGuard, Concatenate, assert_type, assert_never, SupportsIndex, reveal_type
v = 1
if type(v) == float:
    assert False # will it raise error?

# myList:SupportsIndex = dict()
# concatenate is for decorators.
val: int = 0
assert_type(val, int)  # only for type checker.
assert_type(val, str)
if False:
    assert_never(val)
    # assert False

mNewStr = NewType("mNewStr", str)  # you can configure to ignore it.
# mNewStr = NewType("mStr", str) # ignore: [misc]
# class Point(NamedTuple):
#     a: int
#     b: int

# s = Point(a=1, b='')
# s.b

nt = namedtuple("nt", "a b c d")
instNt = nt(a=1, b=2, c=1, d=2)
instNt.a
from typing import List


def get_list() -> List[str]:
    lst = ["PyCon"]
    lst.append(2019)
    return [str(x) for x in lst]


T = TypeVar("T")
a = []  # type: list
# a = 1 # type: list
# how to make some traits of protocol to ensure that term will not implement?

# class NotList(Protocol):
#     def __getitem__(*args:Never,**kwargs:Never ) -> Never:...

# numA:NotList = 1


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
# a: AddAndLength
a = []
# a = 123

# skip pyomo library stub?
from pyomo.environ import ConcreteModel, Var  # type: ignore

model = ConcreteModel()

model.x = cast(ReadableBySubscription, Var([0, 1, 2]))
# model.x = cast(ReadableBySubscription, Var([0, 1, 2]))

model.x[1]
model.v = cast(ArithmaticType, Var())
val = model.v * 1


@overload
def myfun(val: int) -> float:
    ...


@overload
def myfun(val: float) -> int:
    ...


def myfun(val):
    if type(val) == float:
        return int(val)
    elif type(val) == int:
        return float(val)
    else:
        raise Exception("Unacceptable type:", type(val))


val = myfun(1)

# from runtype import Dispatch

# dp = Dispatch()


# @dp
# def mf(a: int) -> float:
#     print("RUNNING A")
#     return float(a)


# @dp
# def mf(a: float) -> int:
#     print("RUNNING B")
#     return int(a)


# unable to statically typecheck
