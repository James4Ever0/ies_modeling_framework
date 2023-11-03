from log_utils import logger_print

from config_utils import getConfig
from config_dataclasses import IESEnv

ies_env = getConfig(IESEnv)
__all__ = ["ies_env"]

# if __name__ == "__main__":
#     # let's test
#     # import rich

#     dat: IESEnv = IESEnvConfig.load()
#     logger_print(dat)
