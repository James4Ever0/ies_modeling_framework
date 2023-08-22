# this file shall be identical anywhere else.
import pytz
import datetime
import os
import sys
import tkinter
from easyprocess import EasyProcess
# on windows nt, alert us (using tkinter or native api?) if commit has failed.
# on other platforms, please improvise.

CHECK_GPTCOMMIT_KEYS="gptcommit config keys"

check_if_exist_keylist = ['openai.apibase', 'openai.api_key']

proc = EasyProcess(CHECK_GPTCOMMIT_KEYS).call()

if proc.return_code !=0:
    raise Exception("gptcommit is not in your PATH. please install.")

if any([k for k in check_if_exist_keylist if k not in proc.stdout]):
    print("setting up gptcommmit locally...")
    if os.name == 'nt':
        setup_file = "setup_gptcommit.cmd"
        SETUP_GPTCOMMIT=f"cmd /C {setup_file}" 
    else:
        setup_file = "setup_gptcommit.sh"
        SETUP_GPTCOMMIT=f"bash {setup_file}"
    if not os.path.exist(setup_file):
        raise Exception(f"setup file '{setup_file}' does not exist.")
    proc = EasyProcess(SETUP_GPTCOMMIT)
    if proc.return_code!=0:
        raise Exception(f"Abnormal exit code {proc.return_code} during setting up gptcommit.\nStdout:\n{proc.stdout}\nStderr:\n{proc.stderr}")

# setup timezone as Shanghai

