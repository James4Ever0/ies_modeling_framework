import os

generate_path = "Makefile.tmp"
import ast

def read_file(fname):
    with open(fname, 'r') as f:
        content = f.read()
        return content

for fname in os.listdir("."):
    if fname.endswith(".py"):
        content = read_file(fname)
        tree = ast.parse(content)
        myindex = -1
        for index, elem in enumerate(tree.body): # shall be an assignment.
            if isinstance(elem, ast.Assign):
                targets = elem.targets
                if len(targets) == 1:
                    if targets[0].id == "MAKEFILE":
                        # this will be our last line.
                        break