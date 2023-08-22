# this file shall be identical anywhere else.
import pytz
import datetime
import os
import shutil
# import tkinter
from easyprocess import EasyProcess

# on windows nt, alert us (using tkinter or native api?) if commit has failed.
# on other platforms, please improvise.

base_repo = os.path.basename(os.curdir)
os_name = os.name
toast_title = f"commit error at '{base_repo}'"

def check_if_executable_in_path(executable: str):
    shutil.which(executable)

if os_name == "nt":
    from win10toast import ToastNotifier

    toaster = ToastNotifier()

    def show_toast(msg):
        toaster.show_toast(title=toast_title, msg=msg)

elif os_name == "darwin":

    def show_toast(msg):
        os.system('terminal-notifier ')

elif os_name == "linux":

    def show_toast(msg):
        ...

else:
    raise Exception(f"\nunable to show toast message due to unknown os: {os_name}")


def emit_message_and_raise_exception(exc_info: str):
    show_toast(exc_info)
    raise Exception(exc_info)


repodirs = []

for path, dirpath, filepath in os.walk("."):
    if ".git" in dirpath:
        repodirs.append(path)

if os.name == "nt":
    COMMIT_SCRIPT = "cmd /C commit.cmd"
else:
    COMMIT_SCRIPT = "bash commit.sh"

try:
    assert "." in repodirs
except:
    emit_message_and_raise_exception(
        "current directory is not a git repo root dir!\nLocation: {os.curdir}"
    )

base_repo_name_and_location = f"repo {base_repo}\nLocation: {os.curdir}"

CHECK_GPTCOMMIT_KEYS = "gptcommit config keys"

check_if_exist_keylist = ["openai.apibase", "openai.api_key"]


def check_proc_exit_status(proc, action):
    if proc.return_code != 0:
        emit_message_and_raise_exception(
            f"Abnormal exit code {proc.return_code} during {action}.\nStdout:\n{proc.stdout}\nStderr:\n{proc.stderr}"
        )


if os.name == "nt":
    setup_file = "setup_gptcommit.cmd"
    SETUP_GPTCOMMIT = f"cmd /C {setup_file}"
else:
    setup_file = "setup_gptcommit.sh"
    SETUP_GPTCOMMIT = f"bash {setup_file}"

repo_absdirs = [os.path.abspath(p) for p in repodirs]
repo_basedir = os.path.abspath(".")

for repo_absdir in repo_absdirs:
    os.chdir(repo_absdir)
    proc = EasyProcess(CHECK_GPTCOMMIT_KEYS).call()

    if proc.return_code != 0:
        emit_message_and_raise_exception(
            "gptcommit is not in your PATH.\nplease install by running `cargo install --locked gptcommit`."
        )

    repo_name_and_location = (
        f"repo {os.path.basename(os.curdir)}\nLocation: {os.curdir}"
    )

    if any([k for k in check_if_exist_keylist if k not in proc.stdout]):
        print("setting up gptcommmit locally...")
        if not os.path.exist(setup_file):
            emit_message_and_raise_exception(
                f"setup file '{setup_file}' does not exist in {repo_name_and_location}"
            )
        proc = EasyProcess(SETUP_GPTCOMMIT)
        check_proc_exit_status(proc, "setting up gptcommit")

os.chdir(repo_basedir)

# setup timezone as Shanghai

timezone_str = "Asia/Shanghai"
timezone = pytz.timezone(timezone_str)

print("using timezone:", timezone)


def get_time_now():
    return datetime.datetime.now(tz=timezone)


commit_min_interval = datetime.timedelta(minutes=30)
last_commit_time_filepath = ".last_commit_time"

import traceback


def get_last_commit_time():
    read_from_file = False
    last_commit_time = datetime.datetime.fromtimestamp(0)
    if os.path.exists(last_commit_time_filepath):
        with open(last_commit_time_filepath, "r") as f:
            content = f.read()
        try:
            last_commit_time = datetime.datetime.fromisoformat(content)
            print("last commit time:", last_commit_time)
            read_from_file = True
        except:
            traceback.print_exc()

    if not read_from_file:
        print("using default last commit time:", last_commit_time)

    return last_commit_time


def check_if_commitable():
    last_commit_time = get_last_commit_time()
    time_now = get_time_now()
    commitable = False
    await_interval = last_commit_time + commit_min_interval - time_now
    if await_interval < 0:
        commitable = True
    else:
        print(
            f"need to wait for {await_interval.total_seconds() // 60} minutes till next commit."
        )
    return commitable


import filelock


def commit():
    if check_if_commitable():
        with filelock.FileLock(".commit_lock", timeout=1) as lock:
            proc = EasyProcess(COMMIT_SCRIPT).call()
            check_proc_exit_status(
                proc, f"commit changes at {base_repo_name_and_location}"
            )
