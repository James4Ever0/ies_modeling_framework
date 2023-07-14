# def mproperty(ptype:type, doc:str):
# def fget(self):
#     return
# def fset(self, val):
#     self. = val

# def fdel(self):
#     del self.

# return property(fget, fset,fdel,doc)

# class mymetaclass(type):
#     def __new__(cls, ):
#         ...

#     def __init__(cls, name, bases, dict):
#         ...

# class MyClass(metaclass=mymetaclass):
#     def __init__(self, ):
#         ...

import abc


class MyABC(metaclass=abc.ABCMeta):
    # class MyABC(abc.ABC):
    @abc.abstractmethod
    def myfunc(self) -> int:  # this alone does not ensure it has the function.
        ...


MyABC.register(dict)
print(issubclass(MyABC, dict))
print(issubclass(dict, MyABC))  # True


class mclass(MyABC):
    def __init__(self):
        ...

    # must implement myfunc.
    # checked by type checker.
    def myfunc(self):
        return 1.0


a = mclass()
# may be useless to typechecker?
# b:MyABC = {}

from typing import Any

# b: Any = lambda x: x+1

from typing_extensions import TypeGuard, reveal_type
from typing import TypeVar, NewType, overload

# typed code better generate with jinja2
p_int = NewType("p_int", int)
p_float = NewType("p_float", float)
T = TypeVar("T", p_int, p_float)
T0 = TypeVar("T0", int, float)


@overload
def is_positive(x: int) -> TypeGuard[p_int]:
    ...


@overload
def is_positive(x: float) -> TypeGuard[p_float]:
    ...


def is_positive(x):  # type: ignore
    # def is_positive(x: T0) -> TypeGuard[T]:
    return isinstance(x, (float, int)) and x > 0


a0 = -1
# is_positive(a0) and a0-1
if is_positive(a0):
    print(a0)  # positive now.

is_positive(False)

# mypy --disallow-untyped-defs --disallow-any-expr --disallow-any-generics --disallow-any-explicit --disallow-any-unimported --disallow-any-decorated --disallow-subclassing-any --disallow-subclassing-any --disallow-untyped-globals --disallow-untyped-calls

# lambda types shall be inferred in typed function parameters

from typing import Protocol


class mproto:
    a: int


mproto_processed = NewType("mproto_processed", mproto)
from typing import Union, Generic
from typing_extensions import TypeVarTuple, Unpack

T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
Ts = TypeVarTuple("Ts")


def mymul(a: T1, b: T2) -> Union[T1, T2]:
    return a * b  # type: ignore
from typing_extensions import TypeAlias, Self, assert_never


class mybase(Generic[T3], mproto):
    processed = False
    mybase_proc = NewType("mybase_proc", int)

    def __init__(self, val: T3):
        self.val = val

    @classmethod
    def create(cls, val: T3):
        return cls(getattr(val, "val", val))

    def __mul__(self, other: T4):  # type:ignore
        # if not isinstance(other, mproto): assert_never(other)
        val = mymul(getattr(self, "val", self), getattr(other, "val", other))
        return val
    # def __mul__(self: Self, other: T2) -> Union[Self, T2]:
    #     assert_type(other, mybase)
    #     return self * other


class mybase_proc(mybase):
    ...


from typing import cast, Type, List

MInt: Type = NewType("MInt", int)
NewInt: TypeAlias = cast(MInt, mybase)
b: mybase[int] = mybase(1)
c = b.__mul__(1.2)
from typing_extensions import assert_type

assert_type(b, mproto_processed)

d = mybase.create(NewInt(1))
# d: mybase[int] = mybase()
E: mybase[str] = mybase("1")
d = d * E
f: mybase[List[int]] = mybase([1])
g = f * 1
# g = mymul(E , f)
# g = E.__mul__(f)
h = g * 2
print(h)
# assert_type(h, mybase[str])

import time


class MyMeta(type):
    def __new__(cls, name, bases, dct):
        print("-----------------------------------")
        print("Allocating memory for class", name)
        print(cls)
        print(bases)
        dct["new_var"] = "new"
        print(dct)
        s = super(MyMeta, cls)
        print(s)
        print()
        return s.__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct):

        s = super(MyMeta, cls)
        print(s)
        print()
        s.__init__(name, bases, dct)  # not working. maybe it is on "bases" or "name"

        print("-----------------------------------")
        print("Initializing class", name)
        print(cls)
        print(bases)
        cls.init_var = f"init{time.time()}"  # no?
        print(dct)

    def __call__(cls, *args, **kwds):
        print("__call__ of ", str(cls))
        print("__call__ *args=", str(args))
        print("__call__ **kargs=", str(kwds))
        print()
        # return cls( *args, **kwds)
        return type.__call__(cls, *args, **kwds)

# class MyKlass(object):
#     __metaclass__ = MyMeta


class MyKlass(metaclass=MyMeta):
    # def __new__(cls, a):
    #     print("myklass new")
    #     print(dir(cls))
    #     super(MyKlass, cls).__new__(cls)
    #     print()
    init_var: str

    def __init__(self, a):
        self.a = a
        print("class non-meta init")
        print(dir(self))
        print()

    def foo(self, param):
        pass

    barattr = 2


mk = MyKlass(a=1)
print("*" * 50)
mk2 = MyKlass(a=9)
dir(mk2)
print(mk.init_var)
print(mk2.init_var)
# print(MyMeta.init_var)

from string import Template
t = Template("$arr value $arr2").substitute(arr=["a", "b"], arr2=["c", "d"])
print(t)