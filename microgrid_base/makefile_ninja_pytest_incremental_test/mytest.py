import pytest
from typing import Sequence, TypeVar, Optional

Chooseable = TypeVar("Chooseable")
# pytest -s to print to stdout without collecting
# pytest --capture=tee-sys

def demo(mtest: Optional[int] = ...):
    ...

def test_request_cache(request):
    val = request.caches.get("val")
    print(f"Value? {repr(val)}")