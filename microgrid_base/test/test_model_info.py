# put device model info here.
# put info into yaml template, which is autogenerated. (suffix: ".tmp") must be renamed and configured to generate this code.

# TODO: figure out how to import fixtures between tests.

import rich
import hydra
from omegaconf import OmegaConf
# from omegaconf import DictConfig, OmegaConf

# shall not use that as type.
from typing import Protocol

# create this using recursion?
class myConfig(Protocol):
    myDb: str
    class subConfig:
        mySubConfig: int

@hydra.main(
    version_base=None,
    config_path=".",
    # config_path="conf",
    config_name="test_config",
)
def my_app(cfg: myConfig) -> None:
# def my_app(cfg: DictConfig) -> None:
    # cfg.subConfig.mySubConfig
    mconfig = OmegaConf.to_yaml(cfg)
    rich.print(mconfig)
    print()
    rich.print(cfg)
    print(type(cfg), dir(cfg))
    print(cfg.db.abc) # error by type checker.


if __name__ == "__main__":
    my_app()
