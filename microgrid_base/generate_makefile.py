import os
import sys


assert (generate_path := sys.argv[-1]).endswith(".tmp")
# generate_path = "Makefile.tmp"

import ast
import astor


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
            tree.body = tree.body[: myindex + 1]
            source_code = astor.to_source(tree)
            exec(source_code)
            print(("MAKEFILE ENTRY: %s" % fname).center(60, "="))
            print(MAKEFILE)  # type: ignore
            for argname in ["inputs", "outputs", "args"]:
                assert (
                    argname in MAKEFILE.keys()
                ), f"{argname} not in {MAKEFILE.keys()}"  # type:ignore
            MAKEFILE.update(fname=fname)  # type: ignore
            python_files.append(MAKEFILE.copy())  # type: ignore
            print()

from jinja_utils import load_render_and_format

# print(python_files)
# breakpoint()
load_render_and_format(
    generate_path.split(".")[0] + ".j2",
    generate_path,
    render_params=dict(python_files=python_files),
    banner="MAKEFILE TMP RENDER",
    needFormat=False,
)
