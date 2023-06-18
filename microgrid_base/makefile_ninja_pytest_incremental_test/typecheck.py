# from typing import NoReturn
from typing_extensions import Never


def never_call_me(arg: Never):
    pass

# do mypy check.
# mypy --python-version <version> does not work for version higher than interpreter's.
def int_or_str(arg: int | str) -> None:
    never_call_me(arg)  # type checker error
    match arg:
        case int():
            print("It's an int")
        case str():
            print("It's a str")
        case _:
            never_call_me(arg)  # OK, arg is of type Never