import ast
import os
import astor
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
        
        except:
            # traceback.print_exc()
            continue
            print(f"Invalid syntax found in file: {fpath}")
            # might have some invalid syntax.
        for el in ast.walk(tree):
            if isinstance(el, ast.Call):
                # breakpoint()
                funcName = astor.to_source(el.func).strip()
                args = el.args
                if len(args) >0:
                    source_code = astor.to_source(el)
                    raise Exception(f"Found erroneous `Field` call:\n    File: {fpath} line {el.lineno}:\n    {source_code.strip()}")