# how to import fixtures from other places? "autouse"?
import pytest

@pytest.fixture
def my_fixture():
    """
    A fixture function that returns a string value.

    Returns:
        str: The string value "FIXTURE VAL".
    """
    return "FIXTURE VAL"
