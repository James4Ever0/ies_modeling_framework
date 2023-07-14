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
                if isinstance(el, ast.Call):
                    funcName = el.func.id
                    args = el.args
                    if len(args) >0:
                        raise Exception(f"Found erroneous `Field` call at line {lineno}:\n{source_code}")
        except:
            traceback.print_exc()
            print(f"Invalid syntax found in file: {fpath}")
            # might have some invalid syntax.