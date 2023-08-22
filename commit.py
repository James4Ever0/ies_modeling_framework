# this file shall be identical anywhere else.
import pytz
import datetime
import os
import sys
import tkinter
from easyprocess import EasyProcess
# on windows nt, alert us (using tkinter or native api?) if commit has failed.
# on other platforms, please improvise.

def emit_message_and_raise_exception(exc_info:str):
    raise Exception(exc_info)

CHECK_GPTCOMMIT_KEYS="gptcommit config keys"

check_if_exist_keylist = ['openai.apibase', 'openai.api_key']

proc = EasyProcess(CHECK_GPTCOMMIT_KEYS).call()

if proc.return_code !=0:
    emit_message_and_raise_exception("gptcommit is not in your PATH. please install.")

if any([k for k in check_if_exist_keylist if k not in proc.stdout]):
    print("setting up gptcommmit locally...")
    if os.name == 'nt':
        setup_file = "setup_gptcommit.cmd"
        SETUP_GPTCOMMIT=f"cmd /C {setup_file}" 
    else:
        setup_file = "setup_gptcommit.sh"
        SETUP_GPTCOMMIT=f"bash {setup_file}"
    if not os.path.exist(setup_file):
        emit_message_and_raise_exception(f"setup file '{setup_file}' does not exist.")
    proc = EasyProcess(SETUP_GPTCOMMIT)
    if proc.return_code!=0:
        emit_message_and_raise_exception(f"Abnormal exit code {proc.return_code} during setting up gptcommit.\nStdout:\n{proc.stdout}\nStderr:\n{proc.stderr}")

# setup timezone as Shanghai

timezone_str = "Asia/Shanghai"
timezone = pytz.timezone(timezone_str)

def get_time_now():
    return datetime.datetime.now(tz=timezone)

commit_min_interval = datetime.timedelta(minutes=30)
last_commit_time_filepath = ".last_commit_time"

def check_if_commitable():
