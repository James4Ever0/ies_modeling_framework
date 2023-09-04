import os
import Levenshtein # to detect suspicious mistypings
from pydantic import BaseModel

class EnvBaseModel(BaseModel):
    IMPORT:str = ""
    def get_import_fpaths(self):
        self.IMPORT

class EnvConfig:

    """
    This class is used to parse and store the environment variables from file or environment variables.
    """
    suspicous_threshold = 3
    min_envname_length_threshold = 6
    def __init__(self, cls):
        if issubclass(cls, EnvBaseModel):
            ...
        else:
            raise Exception(f"{cls} is not a valid EnvBaseModel")

    def __
    # VAR_INIT_AS_ZERO = False
    # UNIT_WARNING_AS_ERROR = False
    # PERCENT_WARNING_THRESHOLD = (
    #     0  # percent value less or equal than this value shall be warned
    # )
# VAR_INIT_AS_ZERO = True
# UNIT_WARNING_AS_ERROR = True
# PERCENT_WARNING_THRESHOLD = (
#     1  # percent value less or equal than this value shall be warned
# )

# MOCK = os.environ.get("MOCK", None)  # if this is mock test.
