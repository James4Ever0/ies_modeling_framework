from log_utils import logger_print

from pydantic import Field, BaseModel
from typing import Literal


class ConflictRefinerParams(BaseModel):
    model_path: str = Field(title="'.lp' model file path")
    output: str = Field(title="conflict analysis output file path")
    config: Literal["cplex", "docplex"] = Field(
        default="cplex",
        title="conflict resolution method, can be one of ['cplex', 'docplex']",
    )
    timeout: float = Field(default=5, title="timeout in seconds, default is 5 seconds")
