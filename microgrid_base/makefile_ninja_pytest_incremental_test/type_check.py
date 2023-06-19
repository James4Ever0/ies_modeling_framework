from typing import Protocol, Any

class AddAndLength(Protocol):
    def __add__(self, v: Any) -> Any: ...
    def __len__(self) -> int: ...

def mfunc(param: AddAndLength) -> int:
    print("You don't care what I do")
    length = len(param)
    print('LEN:', length)
    return length

mfunc(123)
mfunc(['i am list'])