import os

generate_path = "Makefile.tmp"
import ast
import astor


def read_file(fname):
    with open(fname, "r") as f:
        content = f.read()
        return content


for fname in os.listdir("."):
    if fname.endswith(".py"):
        content = read_file(fname)
        tree = ast.parse(content)
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
            print("MAKE DEF IN FILE:", fname)
            print(MAKEFILE)  # type: ignore
