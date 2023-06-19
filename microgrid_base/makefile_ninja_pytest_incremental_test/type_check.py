from typing import TypeVar, List
from typing_extensions import Never

T = TypeVar('T')

def mfunc(param: Never if T is List else T) -> T:
    print("You don't care what I do")
    return param

mfunc(123)
mfunc(['i am list'])