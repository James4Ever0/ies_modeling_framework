import pytest
from typing import Sequence, TypeVar

Chooseable = TypeVar("Chooseable")

int.__covariant__
# pytest -s to print to stdout without collecting
# pytest --capture=tee-sys
def test_request_cache(request):
    val = request.caches.get("val")
    print(f"Value? {repr(val)}")