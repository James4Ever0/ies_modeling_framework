import pytest

# pytest -s to print to stdout without collecting
# pytest --capture=tee-sys
def test_request_cache(request):
    val = request.caches.get("val")
    print(f"Value? {repr(val)}")