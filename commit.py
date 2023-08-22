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

if os.name == "nt":
    COMMIT_SCRIPT = "cmd /C commit.cmd"
else:
    COMMIT_SCRIPT = "bash commit.sh"

def check_proc_exit_status(proc, action):
    if proc.return_code!=0:
        emit_message_and_raise_exception(f"Abnormal exit code {proc.return_code} during {action}.\nStdout:\n{proc.stdout}\nStderr:\n{proc.stderr}")

repo_name_and_location=f"repo {os.basename(os.curdir)}\nLocation: {os.curdir}"

if any([k for k in check_if_exist_keylist if k not in proc.stdout]):
    print("setting up gptcommmit locally...")
    if os.name == 'nt':
        setup_file = "setup_gptcommit.cmd"
        SETUP_GPTCOMMIT=f"cmd /C {setup_file}" 
    else:
        setup_file = "setup_gptcommit.sh"
        SETUP_GPTCOMMIT=f"bash {setup_file}"
    if not os.path.exist(setup_file):
        emit_message_and_raise_exception(f"setup file '{setup_file}' does not exist in {repo_name_and_location}")
    proc = EasyProcess(SETUP_GPTCOMMIT)
    check_proc_exit_status(proc, "setting up gptcommit")

# setup timezone as Shanghai

timezone_str = "Asia/Shanghai"
timezone = pytz.timezone(timezone_str)

print('using timezone:', timezone)

def get_time_now():
    return datetime.datetime.now(tz=timezone)

commit_min_interval = datetime.timedelta(minutes=30)
last_commit_time_filepath = ".last_commit_time"

import traceback

def get_last_commit_time():
    read_from_file = False
    last_commit_time = datetime.datetime.fromtimestamp(0)
    if os.path.exists(last_commit_time_filepath):
        with open(last_commit_time_filepath,'r') as f:
            content = f.read()
        try:
            last_commit_time = datetime.datetime.fromisoformat(content)
            print('last commit time:', last_commit_time)
            read_from_file = True
        except:
            traceback.print_exc()
        
    if not read_from_file:
        print('using default last commit time:', last_commit_time)

    return last_commit_time 

def check_if_commitable():
    last_commit_time = get_last_commit_time()
    time_now = get_time_now()
    commitable = False
    await_interval = last_commit_time + commit_min_interval - time_now
    if await_interval < 0: 
        commitable = True
    else:
        print(f"need to wait for {await_interval.total_seconds() // 60} minutes till next commit.")
    return commitable

import filelock

def commit():
    if check_if_commitable():
        with filelock.FileLock(".commit_lock", timeout = 1) as lock:
           proc = EasyProcess(COMMIT_SCRIPT).call() 
           check_proc_exit_status(proc, f"commit changes at {repo_name_and_location}")
