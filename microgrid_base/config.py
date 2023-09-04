import os
import Levenshtein  # to detect suspicious mistypings
from pydantic import BaseModel, confloat
from exception_utils import ExceptionManager
from typing import Union

class EnvBaseModel(BaseModel):


    def __new__(cls):
        sch = cls.schema()
        upper_prop_keys = set()

        with ExceptionManager() as exc_manager:
            for key in sch["properties"].keys():
                upper_key = key.upper()
                if upper_key in upper_prop_keys:
                    exc_manager.append(
                        "Duplicate property %s in definition of %s"
                        % (upper_prop_keys, cls.__name__)
                    )
        return super().__new__(cls)


class IESEnv(EnvBaseModel):
    VAR_INIT_AS_ZERO: bool = True
    UNIT_WARNING_AS_ERROR: bool = True
    PERCENT_WARNING_THRESHOLD: confloat(gt=0) = 1

class IESShellEnv(IESEnv):
    IES_DOTENV: Union[str, None] = None

class IESDotEnv(IESEnv):
    IMPORT: str = ""
    @property
    def import_fpaths(self):
        imp_fpaths = self.IMPORT.strip().split()
        imp_fpaths = [(new_fp := fp.strip()) for fp in imp_fpaths if len(new_fp) > 0]
        return imp_fpaths

from dotenv import load_dotenv

class EnvConfig:
    """
    This class is used to parse and store the environment variables from file or environment variables.

    Property names are case-insensitive.
    """

    suspicous_threshold = 3
    min_envname_length_threshold = 6

    def __init__(self, cls):
        if issubclass(cls, EnvBaseModel):
            ...
        else:
            raise Exception(f"{cls} is not a valid EnvBaseModel")
    
    def load(self):
        """
        Load environment variables.

        Load sequence:
            Environment variables from os

        """

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

