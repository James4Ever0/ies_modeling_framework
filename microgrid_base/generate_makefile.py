from log_utils import logger_print

import os
import sys


assert (generate_path := sys.argv[-1]).endswith(".tmp")
# generate_path = "Makefile.tmp"

import ast
import astor
from typing import TypedDict, List


class MakefileDict(TypedDict):
    inputs: List[str]
    outputs: List[str]
    args: List[str]
    fname: str


def read_file(fname):
    with open(fname, "r") as f:
        content = f.read()
        return content


python_files = []
for fname in (fnames := os.listdir(".")):
    if fname.endswith(".py"):
        content = read_file(fname)
        tree = ast.parse(content)
        # you shall walk over this. see if it imports any python file in the same directory.
        mymodules = []
        for it in ast.walk(tree):
            if isinstance(it, ast.Import):
                modules = [alias.name for alias in it.names]
                mymodules.extend(modules)
            elif isinstance(it, ast.ImportFrom):
                module = it.module
                mymodules.append(module)
        mymodules = set(mymodules)
        mymodules = [f"{m}.py" for m in mymodules]
        required_pyfiles = [f for f in mymodules if f != fname and f in fnames]
        myindex = -1
        for index, elem in enumerate(tree.body):  # shall be an assignment.
            if isinstance(elem, ast.Assign):
                targets = elem.targets
                if len(targets) == 1:
                    if isinstance(targets[0], ast.Name) and targets[0].id == "MAKEFILE":
                        # this will be our last line.
                        myindex = index
                        break
        if myindex != -1:
            MAKEFILE: MakefileDict
            tree.body = tree.body[: myindex + 1]
            source_code = astor.to_source(tree)
            exec(source_code)
            logger_print(("MAKEFILE ENTRY: %s" % fname).center(60, "="))
            logger_print(MAKEFILE)  # type: ignore
            for argname in ["inputs", "outputs", "args"]:
                assert (
                    argname in MAKEFILE.keys()
                ), f"{argname} not in {MAKEFILE.keys()}"  # type:ignore
            MAKEFILE.update(fname=fname)  # type: ignore
            MAKEFILE["outputs"].extend(required_pyfiles)
            MAKEFILE["outputs"] = list(set(MAKEFILE["outputs"]))
            python_files.append(MAKEFILE.copy())  # type: ignore
            logger_print()

from jinja_utils import load_render_and_format

# logger_print(python_files)
# breakpoint()
load_render_and_format(
    generate_path.split(".")[0] + ".j2",
    generate_path,
    render_params=dict(python_files=python_files),
    banner="MAKEFILE TMP RENDER",
    needFormat=False,
)
