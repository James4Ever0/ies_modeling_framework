import pytest
from typing import Sequence, TypeVar, Optional

Chooseable = TypeVar("Chooseable")
# pytest -s to print to stdout without collecting
# pytest --capture=tee-sys

# ninja -> invoke multiple pytest "persistant" sessions, not cleaning cache and not rerunning the test if passed test -> clean cache only by passing target "clean" to ninja

def demo(mtest: Optional[int] = ...):
    ...


def test_request_cache(request):
    val = request.caches.get("val")
    print(f"Value? {repr(val)}")
