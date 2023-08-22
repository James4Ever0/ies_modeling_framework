# this file shall be identical anywhere else.
import pytz
import datetime
import os
import shutil

from easyprocess import EasyProcess
import traceback
import filelock

# on windows nt, alert us (using tkinter or native api?) if commit has failed.
# on other platforms, please improvise.

base_repo = os.path.basename(os.curdir)
os_name = os.name
toast_title = f"commit error at '{base_repo}'"


def raise_exception(msg):
    raise Exception(msg)


def check_proc_exit_status_base(proc: EasyProcess, action: str, printer):
    if proc.return_code != 0:
        printer(
            f"Abnormal exit code {proc.return_code} during {action}.\nStdout:\n{proc.stdout}\nStderr:\n{proc.stderr}"
        )


def run_and_check_proc_base(cmd, action, printer=raise_exception):
    proc = EasyProcess(cmd)
    check_proc_exit_status_base(proc, action, printer)


def check_if_executable_in_path(
    executable: str, extra_info="", raise_exception: bool = True
):
    lookup_result = shutil.which(executable)
    if lookup_result:
        print("executable {} found in path: {}".format(executable, lookup_result))
        return True
    elif raise_exception:
        base_exc = "executable {} not found in path.".format(executable)
        if extra_info:
            base_exc = "\n".join([base_exc, extra_info])
        raise Exception(base_exc)
    return False


if os_name == "nt":
    from win10toast import ToastNotifier

    toaster = ToastNotifier()

    def show_toast(msg):
        toaster.show_toast(title=toast_title, msg=msg)

elif os_name == "darwin":
    notifier_exec = "terminal-notifier"
    check_if_executable_in_path(notifier_exec)

    def show_toast(msg):
        cmd = [notifier_exec, "-title", toast_title, "-message", msg]
        run_and_check_proc_base(cmd, "sending macos toast")

elif os_name == "linux":
    notifier_exec = "notify-send"
    check_if_executable_in_path(notifier_exec)

    def show_toast(msg):
        cmd = [notifier_exec, toast_title, msg]
        run_and_check_proc_base(cmd, "sending linux toast")

else:
    raise Exception(f"\nunable to show toast message due to unknown os: {os_name}")


def emit_message_and_raise_exception(exc_info: str):
    show_toast(exc_info)
    raise Exception(exc_info)

# currently only enable gitcommit support for each (sub)repo. no recursive commit support (yet).
repodirs = []

for path, dirpath, filepath in os.walk("."):
    if ".git" in dirpath:
        repodirs.append(path)


def get_script_path_and_exec_cmd(script_prefix):
    if os.name == "nt":
        script_suffix = "cmd"
        exec_prefix = "cmd /C"
    else:
        script_suffix = "sh"
        exec_prefix = "bash"
    script_path = f"{script_prefix}.{script_suffix}"
    cmd = f"{exec_prefix} {script_path}"
    try:
        assert os.path.exists(script_path)
        return script_path, cmd
    except:
        emit_message_and_raise_exception(
            "script {} not found in path.".format(script_path)
        )


_, COMMIT_EXEC = get_script_path_and_exec_cmd("commit")

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
    check_proc_exit_status_base(proc, action, emit_message_and_raise_exception)


def run_and_check_proc(cmd, action):
    run_and_check_proc_base(cmd, action, emit_message_and_raise_exception)


setup_file, SETUP_GPTCOMMIT = get_script_path_and_exec_cmd("setup_gptcommit")

repo_absdirs = [os.path.abspath(p) for p in repodirs]
repo_basedir = os.path.abspath(".")

check_if_executable_in_path(
    "gptcommit", "please install by running `cargo install --locked gptcommit`."
)

for repo_absdir in repo_absdirs:
    os.chdir(repo_absdir)
    repo_reldir = os.path.basename(repo_absdir)
    proc = EasyProcess(CHECK_GPTCOMMIT_KEYS)
    check_proc_exit_status(proc, "checking gptcommit config keys")

    repo_name_and_location = (
        f"repo {os.path.basename(os.curdir)}\nLocation: {os.curdir}"
    )

    if any([k for k in check_if_exist_keylist if k not in proc.stdout]):
        print(
            f"setting up gptcommmit locally at repo {repo_reldir}.\nLocation: {repo_absdir}"
        )
        if not os.path.exist(setup_file):
            emit_message_and_raise_exception(
                f"setup file '{setup_file}' does not exist in {repo_name_and_location}"
            )
        run_and_check_proc(SETUP_GPTCOMMIT, "setting up gptcommit")

os.chdir(repo_basedir)

# setup timezone as Shanghai

timezone_str = "Asia/Shanghai"
timezone = pytz.timezone(timezone_str)

print("using timezone:", timezone)


def get_time_now():
    return datetime.datetime.now(tz=timezone)


commit_min_interval = datetime.timedelta(minutes=30)
last_commit_time_filepath = ".last_commit_time"


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


def commit():
    if check_if_commitable():
        with filelock.FileLock(".commit_lock", timeout=1) as lock:
            proc = EasyProcess(COMMIT_EXEC).call()
            check_proc_exit_status(
                proc, f"commit changes at {base_repo_name_and_location}"
            )


if __name__ == "__main__":
    commit()
