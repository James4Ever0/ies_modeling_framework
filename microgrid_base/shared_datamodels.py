from log_utils import logger_print

from pydantic import Field, BaseModel, validator
from typing import Literal
import os

class ConflictRefinerParams(BaseModel):
    model_path: str = Field(title="'.lp' model file path")
    output: str = Field(title="conflict analysis output file path")
    config: Literal["cplex", "docplex"] = Field(
        default="cplex",
        title="conflict resolution method, can be one of ['cplex', 'docplex']",
    )
    timeout: float = Field(default=5, title="timeout in seconds, default is 5 seconds")

    @validator("output")
    def validate_output(cls, val):
        dirname = os.path.dirname(val)
        assert os.path.isdir(dirname), f"output directory does not exist!\noutput path: {val}"
        assert not os.path.isdir(val), f"output path shall not be an existing directory!\noutput path: {val}"
        return val