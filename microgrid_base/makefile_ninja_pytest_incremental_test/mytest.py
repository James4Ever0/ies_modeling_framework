import pytest

def test_request_cache(request):
    val = request.caches.get("val")
    print(f"Value? {repr(val)}")