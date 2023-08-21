from log_utils import logger_print

import ast
import os
import astor
import re
from typing import Callable
from error_utils import ErrorManager
# import traceback

EXCEPTION_LIST = ['exceptional_print.py', 'conflict_utils.py']


with ErrorManager() as em:
    for exceptional_filepath in EXCEPTION_LIST:
        if not os.path.exists(exceptional_filepath):
            em.append("exceptional filepath '%s' does not exist." % exceptional_filepath)
# errorManager.raise_if_any()

IMPORT_LOGGER_PRINT = "from log_utils import logger_print"
IMPORT_LOGGER_PRINT_REGEX = r"^from[ ]+?log_utils[ ]+?import[ ]+?logger_print(?:| .+)$"
fixed = False

SETUP_PYOMO_ENVIRON = "from pyomo_patch import *"

def open_file_and_modify_content(
    fpath: str, func: Callable[[str], str], modify_msg: str
):
    global fixed
    with open(fpath, "r") as f:
        cnt = f.read()
    fixed_cnt = func(cnt)
    if fixed_cnt != cnt:
        logger_print(f"fixing {modify_msg} issue in file: {fpath}")
        fixed = True
        with open(fpath, "w+") as f:  # only modify file when necessary.
            f.write(fixed_cnt)
    return fixed_cnt


def fix_import_logger_in_content(fpath):
    # fixed_cnt = "\n\n".join([IMPORT_LOGGER_PRINT, cnt])
    fixed_cnt = open_file_and_modify_content(
        fpath, lambda cnt: "\n\n".join([IMPORT_LOGGER_PRINT, cnt]), "logger import"
    )
    return fixed_cnt

def fix_pyomo_environ_in_content(fpath, linenos = []):
    def fix_pyomo_environ(cnt:str):
        for line

    fixed_cnt = open_file_and_modify_content(fpath, fix_pyomo_environ, "pyomo environ")
    return fixed_cnt


# TODO: use a single regex instead of two.
FIND_PRINT_REGEX = r"(?<!logger_)((rich.|)(?P<print_statement>print\())"
FIND_PRINT_REGEX_FROMSTART = r"^((rich.|)(?P<print_statement>print\())"
# FIND_PRINT_REGEX = r"(?<!logger_)((rich.|)(?P<print_statement>print\(.*\)))" # "rich." is part of the match, so it will be replaced. composing the replacement string only needs part of the match (not the "rich." part), so we don't include that in the named group.
REPLACE_PRINT_REGEX = "logger_\g<print_statement>"


def fix_print_statement_in_content(fpath: str):
    # with open(fpath, 'r') as f:
    #     cnt = f.read()
    # fixed_cnt = re.sub(FIND_PRINT_REGEX, REPLACE_PRINT_REGEX, cnt, re.MULTILINE)
    def fix_print_statement(cnt: str):
        for regex in [FIND_PRINT_REGEX, FIND_PRINT_REGEX_FROMSTART]:
            cnt = re.sub(regex, REPLACE_PRINT_REGEX, cnt, re.MULTILINE)
        return cnt

    fixed_cnt = open_file_and_modify_content(
        fpath,
        fix_print_statement,
        "print statement",
    )
    # with open(fpath, 'w+') as f:
    #     f.write(fixed_cnt)
    return fixed_cnt


stripped_source = lambda el: astor.to_source(el).strip()

files = os.listdir(".")
# files = [
#     "test_replace_logger.py",
#     "test_replace_logger_no_template.py",
#     "test_replace_logger.py.j2",
# ]  # files for test!
for fpath in files:
    if fpath.endswith(".py"):
        if fpath in EXCEPTION_LIST:
            logger_print("skipping file %s" % fpath)
            continue
        with_template = (template_path := f"{fpath}.j2") in files

        # with open(template_path, 'r') as f:
        #     template_content = f.read()

        found_import_log_utils = False if fpath != "log_utils.py" else True

        found_setup_pyomo_environ = False

        pyomo_environ_to_be_fixed_linenos = []

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
            logger_print(f"Invalid syntax found in file: {fpath}")
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
                if el.module == "pyomo.environ":
                    lineno = el.lineno
                    pyomo_environ_to_be_fixed_linenos.append(lineno)
                if el.level == 0:  # root level.
                    el_source = stripped_source(el)
                    if el_source == IMPORT_LOGGER_PRINT:
                        found_import_log_utils = True
                    elif el_source == SETUP_PYOMO_ENVIRON:
                        found_setup_pyomo_environ = True
        if fpath != "pyomo_patch.py":
            fix_pyomo_environ_in_content(fpath, pyomo_environ_to_be_fixed_linenos, found_setup_pyomo_environ)
        
        if not found_import_log_utils:  # just import, do not change the print logic.
            # if no template was found, fix just one. if template found, fix both.

            # logger_print(f"fixing logging issue in file: {fpath}")
            fix_import_logger_in_content(fpath)
            # with open(fpath, 'w+') as f:
            #     f.write(fix_import_logger_in_content(content))

        if with_template:
            template_content = fix_print_statement_in_content(template_path)

            has_import_on_root = re.findall(
                IMPORT_LOGGER_PRINT_REGEX, template_content, re.MULTILINE
            )
            if len(has_import_on_root) == 0:
                # logger_print(f"fixing logging issue in template: {template_path}")
                fix_import_logger_in_content(template_path)
                # with open(template_path, 'w+') as f:
                #     f.write(fix_import_logger_in_content(template_content))

if fixed:
    import sys

    # logger_print("Please rerun the `make` command for changes!")
    
    cmdargs = " ".join(sys.argv)
    spliter = '--'
    if spliter in sys.argv:
        logger_print("Rerunning `make` command for changes.")
        make_cmd = cmdargs.split(spliter)[-1].strip()
        logger_print("Command: %s" % make_cmd)
        os.system(make_cmd)
    # sys.exit(1)
