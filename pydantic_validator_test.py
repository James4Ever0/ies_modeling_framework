from pydantic import BaseModel, validator
from typing import Optional
import json


class TestDataClass(BaseModel):
    key_1: str
    key_2: Optional[str]
    key_3: str

    @validator("key_1")
    def validate_key_1(cls, value) -> dict:  # validator can also process things?
        cmp = json.loads(value)  # will raise error if it is not parseable.
        return cmp  # now it is dict.


# try parsing?
obj = dict(key_1=json.dumps({"k": "abc"}), key_3="def")  # now we are talking.
TestDataClass.parse_raw(json.dumps(obj))
# how to construct one though?
# data = TestDataClass(key_1=2, key_3="10")  # invalid input! no error?
data_1 = TestDataClass(key_1=json.dumps({"k": "abc"}), key_2="11", key_3="11")
breakpoint()
