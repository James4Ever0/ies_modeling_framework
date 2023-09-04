from config_utils import *
from pydantic import confloat
from log_utils import logger_print

class IESEnv(EnvBaseModel):
    VAR_INIT_AS_ZERO: bool = False
    UNIT_WARNING_AS_ERROR: bool = False
    PERCENT_WARNING_THRESHOLD: confloat(gt=0) = 1
    MOCK_TEST: Union[None, str] = None


IESEnvConfig = getEnvConfigClass(IESEnv)

if __name__ == "__main__":
    # let's test
    # import rich

    dat: IESEnv = IESEnvConfig.load()
    logger_print(dat)
