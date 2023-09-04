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


class ShellEnv:
    DOTENV: Union[str, None] = None


from dotenv import dotenv_values


class DotEnv:
    IMPORT: str = ""

    @property
    def import_fpaths(self):
        imp_fpaths = self.IMPORT.strip().split()
        imp_fpaths = [(new_fp := fp.strip()) for fp in imp_fpaths if len(new_fp) > 0]
        return imp_fpaths

    def resolve_import_graph(self):
        import_fpaths = self.import_fpaths
        resolv = []
        for fpath in import_fpaths:
            assert os.path.isfile(fpath), "File %s does not exist" % fpath
            subdot = self.load(fpath)
            resolv.append(fpath)
            subresolv = subdot.resolve_import_graph()
            resolv.extend(subresolv)
        resolv.reverse()
        ret = []
        for res in resolv:
            if res not in ret:
                ret.append(res)
        ret.reverse()
        return ret

    @classmethod
    def load(cls, fpath: str):
        vals = dotenv_values(fpath)
        return cls()


class IESEnv(EnvBaseModel):
    VAR_INIT_AS_ZERO: bool = True
    UNIT_WARNING_AS_ERROR: bool = True
    PERCENT_WARNING_THRESHOLD: confloat(gt=0) = 1
    MOCK_TEST: Union[None, str] = None


class IESShellEnv(ShellEnv, IESEnv):
    ...


class IESDotEnv(DotEnv, IESEnv):
    ...


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
            Dotenv file and subsequent imported files
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
