from typing import Protocol

class (Protocol)

def mfunc(param: ) -> T:
    print("You don't care what I do")
    length = len(param)
    print(length)

mfunc(123)
mfunc(['i am list'])