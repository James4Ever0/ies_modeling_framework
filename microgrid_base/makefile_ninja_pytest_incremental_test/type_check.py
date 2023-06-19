from typing import Protocol, Any, Generic, TypeVar

T = TypeVar('T')

class AddAndLength(Generic[T]):
    def __add__(self, *args: Any) -> Any:
        ...

    def __len__(self) -> int:
        ...


def mfunc(param: AddAndLength) -> int:
    print("You don't care what I do")
    length = len(param)
    print("LEN:", length)
    return length


mfunc(123)
mfunc(["i am list"])
