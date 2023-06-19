import pytest
from typing import Sequence, TypeVar, Optional, Protocol

Chooseable = TypeVar("Chooseable") # can limit the choice of vars.
# pytest -s to print to stdout without collecting
# pytest --capture=tee-sys

class mProto(Protocol):
    mattr:...
    def mfunc(self, *args, **kwargs): ...

a :mProto
a = 1 # type error
c = "abc"
c:str
c:int
for b in [1,2,3]:
    b: mProto
# ninja -> invoke multiple pytest "persistant" sessions, not cleaning cache and not rerunning the test if passed test -> clean cache only by passing target "clean" to ninja


def demo(mtest: Optional[int] = ...):
    ...


@pytest.fixture
def mfixture():
    print("fixture running")
    return 42


# seems fixture is to be called every time invoked.


def test_request_cache(request):
    val = request.config.cache.get("val", None)
    print(f"Value? {repr(val)}")


def test_fixture(mfixture):
    print("FIXTURE VAL?", mfixture)
    assert mfixture == 43


def test_fixture2(mfixture):
    print("VAL2?", mfixture)
    assert mfixture == 43
