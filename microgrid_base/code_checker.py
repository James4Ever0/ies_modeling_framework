from log_utils import logger_print

import ast
import os
import astor
import re
from typing import Callable

# import traceback

IMPORT_LOGGER_PRINT = "from log_utils import logger_print"
IMPORT_LOGGER_PRINT_REGEX = r"^from[ ]+?log_utils[ ]+?import[ ]+?logger_print(?:| .+)$"


def open_file_and_modify_content(
    fpath: str, func: Callable[[str], str], modify_msg: str
):
    with open(fpath, "r") as f:
        cnt = f.read()
    fixed_cnt = func(cnt)
    if fixed_cnt != cnt:
        print(f"{modify_msg}: {fpath}")
    with open(fpath, "w+") as f:
        f.write(fixed_cnt)
    return fixed_cnt


def fix_import_logger_in_content(fpath):
    # fixed_cnt = "\n\n".join([IMPORT_LOGGER_PRINT, cnt])
    fixed_cnt = open_file_and_modify_content(
        fpath, lambda cnt: "\n\n".join([IMPORT_LOGGER_PRINT, cnt]), ""
    )
    return fixed_cnt


FIND_PRINT_REGEX = r"(?<!logger_)((rich.|)(?P<print_statement>print\(.+\)))"
REPLACE_PRINT_REGEX = "logger_\g<print_statement>"


def fix_print_statement_in_content(fpath: str):
    # with open(fpath, 'r') as f:
    #     cnt = f.read()
    # fixed_cnt = re.sub(FIND_PRINT_REGEX, REPLACE_PRINT_REGEX, cnt, re.MULTILINE)
    fixed_cnt = open_file_and_modify_content(
        fpath,
        lambda cnt: re.sub(FIND_PRINT_REGEX, REPLACE_PRINT_REGEX, cnt, re.MULTILINE),
        "",
    )
    # with open(fpath, 'w+') as f:
    #     f.write(fixed_cnt)
    return fixed_cnt


stripped_source = lambda el: astor.to_source(el).strip()

# files = os.listdir(".")
files = [
    "test_replace_logger.py",
    "test_replace_logger_no_template.py",
    "test_replace_logger.py.j2",
]  # files for test!
for fpath in files:
    if fpath.endswith(".py"):
        with_template = (template_path := f"{fpath}.j2") in files

        # with open(template_path, 'r') as f:
        #     template_content = f.read()

        found_import_log_utils = False if fpath != "log_utils.py" else True

        # read and fix this file.
        content = fix_print_statement_in_content(fpath)
        # with open(fpath, "r") as f:
        #     content = f.read()

        # # fixing print statement issue.
        # with open(fpath, 'w+') as f:
        #     f.write(fix_print_statement_in_content(content))

        # check pydantic field issues.
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
                if el.level == 0:  # root level.
                    el_source = stripped_source(el)
                    if el_source == IMPORT_LOGGER_PRINT:
                        found_import_log_utils = True
        if not found_import_log_utils:  # just import, do not change the print logic.
            # if no template was found, fix just one. if template found, fix both.

            # print(f"fixing logging issue in file: {fpath}")
            fix_import_logger_in_content(fpath)
            # with open(fpath, 'w+') as f:
            #     f.write(fix_import_logger_in_content(content))
        if with_template:
            template_content = fix_print_statement_in_content(template_path)

            has_import_on_root = re.findall(
                IMPORT_LOGGER_PRINT_REGEX, template_content, re.MULTILINE
            )
            if len(has_import_on_root) == 0:
                # print(f"fixing logging issue in template: {template_path}")
                fix_import_logger_in_content(template_path)
                # with open(template_path, 'w+') as f:
                #     f.write(fix_import_logger_in_content(template_content))
