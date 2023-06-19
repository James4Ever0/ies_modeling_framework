from typing import TypeVar, List
from typing_extensions import Never, TypeAlias

T = TypeVar('T')
NotList: TypeAlias = T if T is not List else Never

def mfunc(param: NotList) -> T:
    print("You don't care what I do")
    return param

mfunc(123)