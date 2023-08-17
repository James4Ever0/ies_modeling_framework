from log_utils import logger_print


def decreaseByOneThousand(number, threshold=10):
    assert number >= 0, f"invalid number: {repr(number)}"
    if number <= threshold:
        return number
    ret = number / 10
    # logger_print(number, ret)
    return decreaseByOneThousand(ret, threshold=threshold)


import pandas
from typing import Union
import random


def modifyIfIsDeviceCount(location, val):
    if "deviceCount" in location:
        return random.randint(1, 10)
    return val


def modifyValueIfNumber(location, val):
    if isinstance(val, Union[float, int]):
        if not pandas.isnull(val):
            if val != 0:
                positive = val > 0
                val_abs = abs(val)
                val_abs_modified = decreaseByOneThousand(val_abs)
                val_modified = (1 if positive else -1) * val_abs_modified
                return val_modified
    return val


if __name__ == "__main__":
    from json_utils import jsonApply
    import json

    with open("test_output_full_mock.json", "r") as f:
        json_obj = json.load(f)

    applied_json_obj = jsonApply(json_obj, modifyValueIfNumber, modifyIfIsDeviceCount)
    output_file = "test_output_full_mock_reduced.json"
    with open(output_file, "w+") as f:
        f.write(json.dumps(applied_json_obj, indent=4, ensure_ascii=False))
