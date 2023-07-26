import ast
import os
import astor
import re
# import traceback

# check pydantic field issues.

files = os.listdir(".")
for fpath in files:
    if fpath.endswith(".py"):
        found_import_log_utils = False if fpath != "log_utils.py" else True
        # read this file.
        with open(fpath, "r") as f:
            content = f.read()
        try:
            tree = ast.parse(content)
            # walk over this.
        except:
            # traceback.print_exc()
            print(f"Invalid syntax found in file: {fpath}")
            continue
            # might have some invalid syntax.
        for el in ast.walk(tree):
            if isinstance(el, ast.Call):
                # breakpoint()
                funcName = astor.to_source(el.func).strip()
                if "Field" in funcName:
                    if len(el.args) > 0 or len(el.keywords) == 0:
                        source_code = astor.to_source(el)
                        raise Exception(
                            f"Found erroneous `Field` call:\n    File: {fpath} line {el.lineno}:\n    {source_code.strip()}"
                        )
            elif isinstance(el, ...):
                # check if really imported.
                found_import_log_utils = True
        if not found_import_log_utils: # just import, do not change the print logic.
            # if no template was found, fix just one. if template found, fix both.
            with_template = (template_path:=f"{fpath}.j2") in files

            print("fixing logging issue on file:")
            with open(fpath, 'w+') as f:
                f.write("\n\n".join(["from log_utils import logger_print", content]))
            if with_template:
                print("fixing logging issue from template:")
                with open(template_path, 'r') as f:
                    template_content = f.read()
                    re.findall(r"[ ]+?from[ ]+?", , re.MULTILINE)