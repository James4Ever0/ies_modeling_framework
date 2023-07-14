import ast
import os
import traceback

# check pydantic field issues.

files = os.listdir(".")
for fpath in files:
    if fpath.endswith(".py"):
        # read this file.
        with open(fpath, 'r') as f:
            content = f.read()
        try:  
            tree = ast.parse(content)
            # walk over this.
            for el in ast.walk(tree):
                ...
        except:
            traceback.print_exc()
            print(f"Invalid syntax found in file: {fpath}")
            # might have some invalid syntax.