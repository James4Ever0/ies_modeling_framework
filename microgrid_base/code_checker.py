from log_utils import logger_print

import ast
import os
import astor
import re
# import traceback

IMPORT_LOGGER_PRINT = "from log_utils import logger_print"
IMPORT_LOGGER_PRINT_REGEX = r"^from[ ]+?log_utils[ ]+?import[ ]+?logger_print(?:| .+)$"

fix_import_logger_in_content = lambda cnt: "\n\n".join([IMPORT_LOGGER_PRINT, cnt])

FIND_PRINT_REGEX = r"(?<!logger_)((rich.|)(?P<print_statement>print\(.+\)))"
REPLACE_PRINT_REGEX = "logger_\g<print_statement>"
fix_print_statement_in_content = lambda cnt: re.sub(FIND_PRINT_REGEX, "(?<!print)


stripped_source = lambda el: astor.to_source(el).strip()

# files = os.listdir(".")
files = ["test_replace_logger.py", "test_replace_logger_no_template.py", "test_replace_logger.py.j2"] # files for test!
for fpath in files:
    if fpath.endswith(".py"):
        with_template = (template_path:=f"{fpath}.j2") in files

        found_import_log_utils = False if fpath != "log_utils.py" else True

        # check pydantic field issues.
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
                funcName = stripped_source(el.func)
                if "Field" in funcName:
                    if len(el.args) > 0 or len(el.keywords) == 0:
                        source_code = stripped_source(el)
                        raise Exception(
                            f"Found erroneous `Field` call:\n    File: {fpath} line {el.lineno}:\n    {source_code}"
                        )
            elif isinstance(el, ast.ImportFrom):
                # check if really imported.
                if el.level == 0: # root level.
                    el_source = stripped_source(el)
                    if el_source == IMPORT_LOGGER_PRINT:
                        found_import_log_utils = True
        if not found_import_log_utils: # just import, do not change the print logic.
            # if no template was found, fix just one. if template found, fix both.

            print(f"fixing logging issue in file: {fpath}")
            with open(fpath, 'w+') as f:
                f.write(fix_import_logger_in_content(content))
        if with_template:
            with open(template_path, 'r') as f:
                template_content = f.read()
            has_import_on_root = re.findall(IMPORT_LOGGER_PRINT_REGEX, template_content, re.MULTILINE)
            if len(has_import_on_root) == 0:
                print(f"fixing logging issue in template: {template_path}")

                with open(template_path, 'w+') as f:
                    f.write(fix_import_logger_in_content(template_content))