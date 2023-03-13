from pydantic import BaseModel, validator
from typing import Optional
import json

class TestDataClass(BaseModel):
    key_1:str
    key_2:Optional[str]
    key_3:str
    @validator("key_1")
    def validate_key_1():