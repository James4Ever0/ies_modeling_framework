from log_utils import logger_print

from config_utils import getConfig, Union, EnvBaseModel
from pydantic import confloat

class IESEnv(EnvBaseModel):
    VAR_INIT_AS_ZERO:Union[None, str] = None
    # VAR_INIT_AS_ZERO: bool = False
    UNIT_WARNING_AS_ERROR: bool = False
    PERCENT_WARNING_THRESHOLD: confloat(gt=0) = 1
    MOCK_TEST: Union[None, str] = None

 
ies_env = getConfig(IESEnv)
__all__ = ["ies_env"]
# if __name__ == "__main__":
#     # let's test
#     # import rich

#     dat: IESEnv = IESEnvConfig.load()
#     logger_print(dat)
