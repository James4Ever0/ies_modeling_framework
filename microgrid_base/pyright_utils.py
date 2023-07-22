MIN_PYRIGHT_VERSION = "1.1.317"  # if lower than this version then raise exception.

import parse


def parse_version(version: str):
    p = parse.parse("{x:d}.{y:d}.{z:d}", version)
    return [p[k] for k in "xyz"]


def check_version(current_version: str, minimum_version: str):
    cp = parse_version(current_version)
    mp = parse_version(minimum_version)
    for cv, mv in zip(cp, mp):
        if cv < mv:
            return False
    return True


import pyright
from typing import Any, Union
import subprocess

# monkey patch start
def run(
    *args: str, **kwargs: Any
) -> Union["subprocess.CompletedProcess[bytes]", "subprocess.CompletedProcess[str]"]:
    ROOT_CACHE_DIR = pyright.utils.get_cache_dir() / "pyright-python"
    version = pyright.__pyright_version__
    if not check_version(version, MIN_PYRIGHT_VERSION):
        raise Exception(
            f"Pyright version {version} does not meet minimum version {MIN_PYRIGHT_VERSION}\nPlease upgrade using `pip install -U pyright`"
        )
    # current_version = pyright.node.get_pkg_version(pkg_dir / 'package.json')
    # cache_dir = ROOT_CACHE_DIR / current_version
    cache_dir = ROOT_CACHE_DIR / version
    cache_dir.mkdir(exist_ok=True, parents=True)
    pkg_dir = cache_dir / "node_modules" / "pyright"

    script = pkg_dir / "index.js"
    if not script.exists():
        raise RuntimeError(f"Expected CLI entrypoint: {script} to exist")
    result = pyright.node.run("node", str(script), *args, **kwargs)
    return result


pyright.cli.run = run
# monkey patch end

if __name__ == "__main__":
    args = ["ies_optim.py"]
    kwargs = dict(capture_output=True)
    result = pyright.cli.run(*args, capture_output=True)

    import rich

    rich.print(result)
