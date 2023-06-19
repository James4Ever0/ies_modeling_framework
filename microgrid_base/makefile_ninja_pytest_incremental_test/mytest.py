import pytest
from typing import Sequence, TypeVar, Optional

Chooseable = TypeVar("Chooseable")
# pytest -s to print to stdout without collecting
# pytest --capture=tee-sys

# ninja -> invoke multiple pytest "persistant" sessions, not cleaning cache and not rerunning the test if passed test -> clean cache only by passing target "clean" to ninja


def demo(mtest: Optional[int] = ...):
    ...


@pytest.fixture
def mfixture():
    print("fixture running")
    return 42


def test_request_cache(request):
    val = request.config.cache.get("val", None)
    print(f"Value? {repr(val)}")


def test_fixture(mfixture):
    print("FIXTURE VAL?", mfixture)
    assert mfixture == 43


def test_fixture2(mfixture):
    print("VAL2?", mfixture)
== 43


def test_fixture2(mfixture):
    print("FIXTURE VAL2")
    assert mfixture == 43
    
