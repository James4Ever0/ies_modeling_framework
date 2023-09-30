from log_utils import logger_print
from log_utils import DOCKER_IMAGE_TAG
import progressbar
import sys
import os

import easyprocess, func_timeout
from typing import Tuple
import re
import datetime

LATEST = "latest"
DOCKER = "docker"
def docker_exec(cmd):
    logger_print("executing docker command: {}".format(cmd))
    os.system(f"{DOCKER} {cmd}")


def parse_docker_image_builttime_and_get_timestamp(builttime: str):
    no_letter_builttime, _ = re.subn(r"[a-zA-Z]", "", builttime)
    no_letter_builttime = no_letter_builttime.strip()
    time_format = r"%Y-%m-%d %H:%M:%S %z"
    builttime_timeobj = datetime.datetime.strptime(no_letter_builttime, time_format)
    builttime_timestamp = builttime_timeobj.timestamp()
    return builttime_timestamp


import json

# TODO: tag the final image with date & time
# docker tag microgrid_docplex:<latest_version> microgrid_docplex:latest

DOCKER_PROC_TIMEOUT = 15
ACCEPTED_DOCKER_ARCH = "x86_64"  # the only one.
# hold, we may check the architecture.


def number_to_version(number: int):
    digit1 = number // 100  # extract the first digit (hundreds place)
    digit2 = (number // 10) % 10  # extract the second digit (tens place)
    digit3 = number % 10  # extract the third digit (ones place)

    result = (digit1, digit2, digit3)
    return result


def version_to_number(version: Tuple[int, int, int]):
    number = 100 * version[0] + 10 * version[1] + version[2]
    return number


def increment_version(prev_version: Tuple[int, int, int]):
    ver_plain = version_to_number(prev_version)
    ver_plain += 1
    ver_new = number_to_version(ver_plain)
    return ver_new


def get_image_hash(image_name):
    dat = get_image_info(image_name)
    image_hash = dat["ID"]
    return image_hash


def get_image_info(image_name):
    cmd = f"docker images --format json {image_name}"
    proc = easyprocess.EasyProcess(cmd).call()
    stdout = proc.stdout
    dat = json.loads(stdout)
    return dat


def get_latest_builttime_of_image(image_basename):
    latest_image_name = image_basename + f":{LATEST}"
    dat = get_image_info(latest_image_name)
    builttime: str = dat["CreatedAt"]
    return builttime


ONE_HOUR = 3600
ONE_DAY = ONE_HOUR * 24
# ONE_WEEK = ONE_DAY * 7
# IMAGE_OUT_OF_DATE_THRESHOLD = ONE_WEEK
IMAGE_OUT_OF_DATE_THRESHOLD = ONE_DAY


def check_if_latest_builttime_of_image_is_out_of_date(image_basename):
    out_of_date = True
    current_timestamp = datetime.datetime.now().timestamp()
    latest_builttime = get_latest_builttime_of_image(image_basename)
    latest_builttime_timestamp = parse_docker_image_builttime_and_get_timestamp(
        latest_builttime
    )
    age = current_timestamp - latest_builttime_timestamp
    if age > IMAGE_OUT_OF_DATE_THRESHOLD:
        logger_print(
            f"image {image_basename} is out of date. latest builttime: {latest_builttime}"
        )
    else:
        out_of_date = False
    return out_of_date


def call_cmd_with_timeout_and_return_proc(cmd, timeout=DOCKER_PROC_TIMEOUT):
    proc = easyprocess.EasyProcess(cmd).call(timeout=timeout)
    return proc


def check_if_docker_arch_acceptable():
    cmd = "docker info -f json"
    proc = call_cmd_with_timeout_and_return_proc(cmd)
    obj = json.loads(proc.stdout)
    arch = obj["Architecture"]
    if arch != ACCEPTED_DOCKER_ARCH:
        raise Exception(
            "Unsupported architecture: %s (run under %s instead)"
            % (arch, ACCEPTED_DOCKER_ARCH)
        )


check_if_docker_arch_acceptable()

"""
create or import docker environment with scripts.

you may use Dockerfile.
"""
# TODO: replace with docker compose
# TODO: put this into release archive
# TODO: show both cli argument help

import docker
from config_utils import getConfig


def killAndPruneAllContainers():
    cmd = "docker container ls"
    proc = call_cmd_with_timeout_and_return_proc(cmd)
    # proc = easyprocess.EasyProcess("docker container ls -a").call()
    if proc.stdout:
        lines = proc.stdout.split("\n")[1:]
        container_ids = [line.split(" ")[0] for line in lines]
        for cid in progressbar.progressbar(container_ids):
            cmd = f"docker container kill {cid}"
            try:
                func_timeout.func_timeout(2, os.system, args=(cmd,))
            except func_timeout.FunctionTimedOut:
                logger_print(
                    f'timeout while killing container "{cid}".\nmaybe the container is not running.'
                )
            # os.system(f"docker container kill -s SIGKILL {cid}")
        os.system("docker container prune -f")


# from config import IESEnv
from config_dataclasses import IESEnv, DockerLauncherConfig

config = getConfig(DockerLauncherConfig)
# breakpoint()
# logger_print(config.reduce())
# breakpoint()

if config.TERMINATE_ONLY:
    killAndPruneAllContainers()
    logger_print("TERMINATE_ONLY is set. Exiting.")
    exit(0)


def recursive_split_path(path):
    leftover, ret = os.path.split(path)
    if ret != "":
        yield ret
    if leftover != "":
        yield from recursive_split_path(leftover)


client = docker.from_env()

abs_curdir = os.path.abspath(".")
path_components_generator = recursive_split_path(abs_curdir)
rel_curdir = next(path_components_generator)
rel_pardir = next(path_components_generator)

if sys.maxsize < 2**32:
    raise Exception("Your system is 32bit or lower, which Docker does not support.")


dockerfile_init_path = "Dockerfile_init"
dockerfile_main_path = "Dockerfile_main"
dockerfile_patch_path = "Dockerfile_patch"
dockerfile_update_path = "Dockerfile_update"
dockerfile_update_self_path = "Dockerfile_update_self"

RELEASE_ENV = False
if rel_curdir != "microgrid_base":
    RELEASE_ENV = True
    os.system(
        f"sed -i 's/jubilant-adventure2\\/microgrid_base/{rel_pardir}\\/init/g' {dockerfile_patch_path} {dockerfile_update_path}",
    )

# client = docker.DockerClient(
#     base_url="//./pipe/docker_engine" if os.name == "nt" else "unix://var/run/docker.sock"
# )
def build_image(image_tag, dockerfile_path, context_path):
    global RELEASE_ENV
    # if not RELEASE_ENV:
    #     os.environ['ADDITIONAL_SUFFIX'] ='/microgrid_server_release' # copy files from release, don't straight from curdir because it is huge.
    # env_additional_suffix = '' if RELEASE_ENV else 'env ADDITIONAL_SUFFIX=/microgrid_server_release' # copy files from release, don't straight from curdir because it is huge.
    ADDITIONAL_SUFFIX_ARGS = '../' if RELEASE_ENV else "microgrid_server_release"
    docker_buildargs = f'--build-arg ADDITIONAL_SUFFIX_ARGS=/{ADDITIONAL_SUFFIX_ARGS}' # copy files from release, don't straight from curdir because it is huge.
    command = f"{DOCKER} build -t {image_tag} -f {dockerfile_path} --progress plain {docker_buildargs} {context_path}"
    logger_print('build command:', command)
    # command = f"{env_additional_suffix} {DOCKER} build -t {image_tag} -f {dockerfile_path} --progress plain {context_path}"
    # logger_print(command)
    exit_code = os.system(command)
    if exit_code:
        raise Exception(f"Abnormal exit code {exit_code} for command:\n{' '*4+command}")
    return True


# import datetime
update_image_basename = "microgrid_update"
generate_image_with_tag = (
    lambda basename, verinfo: f"{basename}:v{'.'.join([str(i) for i in verinfo])}"
)
generate_update_image_with_tag =lambda verinfo: generate_image_with_tag(update_image_basename,verinfo)
init_verinfo = number_to_version(1)
update_image_first_ver_tag = generate_update_image_with_tag(init_verinfo)
update_image_tag = f"{update_image_basename}:latest"
# update_interval = datetime.timedelta(days=config.UPDATE_INTERVAL_IN_DAYS)
# update_image_file_path = os.path.join(os.path.expanduser("~"), ".microgrid_update")
final_image_tag = f"microgrid_docplex:{LATEST}"
image_tag = f"microgrid_server:{LATEST}"
remote_image_tag = f"agile4im/microgrid_server:{LATEST}"
intermediate_image_tag = "microgrid_init"
context_path = "../../"



image_storage_dir = "images"
image_path = os.path.join(image_storage_dir, f"{image_tag.replace(':','_')}.tar")

image_storage_gitignore = os.path.join(image_storage_dir, ".gitignore")

if os.path.exists(image_storage_dir):
    if not os.path.isdir(image_storage_dir):
        raise Exception("'%s' exists and is not a directory!" % image_storage_dir)
else:
    os.mkdir(image_storage_dir)

with open(image_storage_gitignore, "w+") as f:
    f.write("*\n")


def list_image_tags():
    images = client.images.list()
    image_tags = [tag for image in images for tag in image.tags]
    return image_tags


image_tags = list_image_tags()

if final_image_tag not in image_tags:
    if image_tag not in image_tags:
        logger_print("image not found: %s" % image_tag)
        if not os.path.exists(image_path):
            if config.NO_HALFDONE:
                # run remote pull command.
                docker_exec(f"pull {remote_image_tag}")
                docker_exec(f"tag {remote_image_tag} {image_tag}")
            else:
                # first build the image, then export.
                logger_print("building image...")
                # client.images.build(
                #     path=context_path, tag=image_tag, dockerfile=dockerfile_path, quiet=False
                # )
                build_image(intermediate_image_tag, dockerfile_init_path, context_path)
                build_image(image_tag, dockerfile_main_path, context_path)
                image = client.images.get(image_tag)
                # image.save()
                logger_print("saving image...")
                # not working via api.
                # with open(image_path, "wb") as f:
                #     for chunk in image.save():
                #         f.write(chunk)
                docker_exec(f"save -o {image_path} {image_tag}")
        else:
            logger_print("loading image...")
            docker_exec(f"load -i {image_path}")
            # with open(image_path, "rb") as f:
            #     data = f.read()
            #     client.images.load(data)

    # now patch the image.
    build_image(final_image_tag, dockerfile_patch_path, context_path)

# DEPRECATED: may not need to use scheduled update here.
# import pathlib
# import time


# def need_update_image():
#     if config.FORCE_UPDATE:
#         logger_print(f"user forced to update image.")
#         return True

#     ti_c = os.path.getctime(update_image_file_path)

#     time_now = time.time()
#     last_update_td = datetime.timedelta(seconds=time_now - ti_c)
#     if last_update_td > update_interval:
#         logger_print(
#             f"last update time: {last_update_td.days} days ago >= update interval: {update_interval.days} days"
#         )
#         logger_print("need to update image.")
#         return True
#     return False

# DEPRECATED: this may hang forever
# all_containers = client.containers.list(all=True)
# logger_print("stopping running containers...")

# for container in progressbar.progressbar(all_containers):
#     container.stop()
# logger_print("pruning stopped containers...")
# client.containers.prune()

# if need_update_image():
#     # remove old image first, then build new image
#     # how does docker build work anyway? does it cache based on file hash?
#     killAndPruneAllContainers()
#     docker_exec(f"image rm {dockerfile_update_path}")
#     if build_image(update_image_tag, dockerfile_update_path, context_path) is True:
#         os.remove(update_image_file_path)
#         pathlib.Path(update_image_file_path).touch()
#     else:
#         raise Exception("Image update failed.")

# load the exported image.
# run the command to launch server within image from here.
# host_path = "./microgrid_server_release"
log_path = os.path.join(os.path.expanduser("~"), "logs_container") if RELEASE_ENV else "./logs_container"
if os.path.isdir(log_path):
    logger_print(f"skipping creating logger directory: {log_path}")
elif not os.path.exists(log_path):
    os.mkdir(log_path)
else:
    raise Exception(f"{log_path} exists but is not a directory.")
# if RELEASE_ENV:
    # host_path = "../." + host_path
# host_mount_path = os.path.abspath(host_path)
# don't need this workaround when using docker-py.

def refine_nt_abspath_for_docker_mount(path:str):
    if os.name == "nt":
        disk_symbol, pathspec = path.split(":")
        pathspec = pathspec.replace("\\", "/")
        path = f"//{disk_symbol.lower()}{pathspec}"
    return path

host_log_path = os.path.abspath(log_path)
# host_log_path = refine_nt_abspath_for_docker_mount(host_log_path)

killAndPruneAllContainers()


def find_latest_verinfo_of_image_with_latest_image_tags(image_basename:str):
    image_tags = list_image_tags()
    return find_latest_verinfo_of_image(image_tags, image_basename)

def find_latest_image_tag_with_latest_verinfo_of_image_and_latest_image_tags(image_basename:str):
    verinfo = find_latest_verinfo_of_image_with_latest_image_tags(image_basename)
    if verinfo is None: return None
    return generate_image_with_tag(image_basename, verinfo)

def find_latest_verinfo_of_image(image_tags: list[str], image_basename: str):
    latest_verinfo = None
    for image_tag in image_tags:
        if image_tag.startswith(image_basename):
            verpart_ = image_tag.split(":v")
            if len(verpart_) == 2:
                verpart = verpart_[1]
                verinfo = tuple([int(i) for i in verpart.split(".")])
                assert len(verinfo) == 3, (
                    "invalid version format at: %s\nhint: must be three positive integers splited by dot, and first two on the right must be smaller than 10"
                    % image_tag
                )
                if latest_verinfo is None:
                    latest_verinfo = verinfo
                elif verinfo > latest_verinfo:
                    latest_verinfo = verinfo
                else:
                    continue
    if latest_verinfo is None:
        raise Exception(
            f"Could not find any versioned image ({image_basename}) with tag starting with {update_image_basename}"
        )
    logger_print(f"latest version for image {image_basename}: {latest_verinfo}")
    return latest_verinfo


def find_latest_verinfo_of_update_image(image_tags: list[str]):
    return find_latest_verinfo_of_image(image_tags, update_image_basename)


from contextlib import contextmanager


@contextmanager
def check_if_need_to_tag_context(image_tag):
    info = dict(need_to_tag=True, previous_hash=None)
    _image_tags = list_image_tags()
    if image_tag in _image_tags:
        info["need_to_tag"] = False
        info["previous_hash"] = get_image_hash(image_tag)

    def get_need_to_tag():
        if info["need_to_tag"] == False:
            # check hash now.
            current_hash = get_image_hash(image_tag)
            need_to_tag = info["previous_hash"] != current_hash
        return need_to_tag

    try:
        yield get_need_to_tag
    finally:
        del _image_tags
        del get_need_to_tag
        del info


def build_and_tag(
    latest_version_image_tag,
    latest_image_tag,
    dockerfile_path,
    context_path,
    # override_need_to_tag = False
):
    with check_if_need_to_tag_context(latest_image_tag) as get_need_to_tag:
        build_image(latest_image_tag, dockerfile_path, context_path)
        # build_image(latest_version_image_tag, dockerfile_path, context_path)
        need_to_tag = get_need_to_tag()
    # check if we really want to tag this (is this updated?)
    if need_to_tag:
        # if override_need_to_tag or need_to_tag:
        docker_exec(f"tag {latest_image_tag} {latest_version_image_tag}")
    # docker_exec(f"tag {latest_version_image_tag} {latest_image_tag}")


# update with tagging
if config.FINAL_IMAGE_TAG != LATEST:
    logger_print(f"skipping update because of custom tag: {config.FINAL_IMAGE_TAG}")
elif update_image_tag in image_tags:
    if update_image_first_ver_tag not in image_tags:
        logger_print(
            f"tagging first versioned final image ({update_image_tag}) build as: {update_image_first_ver_tag}"
        )
        docker_exec(f"tag {update_image_tag} {update_image_first_ver_tag}")
        # image_tags.append(update_image_first_ver_tag)
    logger_print("performing recursive update of final image")
    # old_verinfo = find_latest_verinfo_of_update_image(image_tags)
    old_verinfo = find_latest_verinfo_of_image_with_latest_image_tags(update_image_basename)

    if old_verinfo > init_verinfo:
        out_of_date = check_if_latest_builttime_of_image_is_out_of_date(
            update_image_basename
        )
    else:
        logger_print(
            f"forcing update because latest version info equals to initial version info: {init_verinfo}"
        )
        out_of_date = True
    if out_of_date:
        latest_verinfo = increment_version(old_verinfo)
    else:
        logger_print(f"using old tag: {old_verinfo} (to save space)")
        latest_verinfo = old_verinfo

    latest_verinfo = increment_version(old_verinfo)
    latest_update_image_tag = generate_update_image_with_tag(latest_verinfo)
    build_and_tag(
        latest_update_image_tag,
        update_image_tag,
        dockerfile_update_path,
        # dockerfile_update_self_path,
        context_path,
    )
else:
    logger_print("building final image (non-recursive)")
    build_and_tag(
        update_image_first_ver_tag,
        update_image_tag,
        dockerfile_update_path,
        context_path,
    )

latest_update_image = find_latest_image_tag_with_latest_verinfo_of_image_and_latest_image_tags(update_image_basename)
# build_image(update_image_tag, dockerfile_update_path, context_path)

# BUG: error while creating mount source path
# FIX: restart the docker engine (win) if fail to run container (usually caused by unplugging anything mounted by volume)
container_image_tag = (
    latest_update_image
    if config.FINAL_IMAGE_TAG == LATEST
    else f"{update_image_basename}:{config.FINAL_IMAGE_TAG}"
)
container_env = {DOCKER_IMAGE_TAG: container_image_tag, **config.reduce().dict()}
logger_print("running container...")
try:
    container = client.containers.run(
        # final_image_tag,
        container_image_tag,
        # image_tag,
        environment=container_env,
        # environment=dict(os.environ),  # may override normal environment variables?
        # remove=True,
        remove=False,  # to get the image hash.
        # command="ls -lth microgrid",
        # command="bash fastapi_tmuxp.sh",
        # command="bash -c 'cd microgrid/init && bash init.sh && cd ../server && bash fastapi_tmuxp.sh windows'",
        command="bash -c 'cd microgrid/server && bash fastapi_tmuxp.sh windows'",
        # command="bash -c 'cd microgrid/server && ls -lth .'",
        # command="echo 'hello world'",
        detach=True,
        restart_policy={
            "Name": "on-failure"
        },  # restart indefinitely, though might not always work.
        # detach=False,
        # we need to monitor this.
        tty=True,
        ports={f"{(server_port:=9870)}/tcp": server_port},
        volumes = { # if using volumes, you need to copy the contents of the volume to outside to view it.
            # docker run --rm \
            #   --mount source=myvolume,target=/mnt \
            #   -v /backup:/backup \
            #   alpine cp -r /mnt /backup
        host_log_path: {"bind": "/root/microgrid/server/logs", 'mode':'rw'}
        # "microgrid_logs": {"bind": "/root/microgrid/server/logs", 'mode':'rw'}
        }
        # volumes={
        #     host_mount_path: {"bind": (mount_path := "/root/microgrid"), "mode": "rw"}
        # },
        # volumes={"<HOST_PATH>": {"bind": "<CONTAINER_PATH>", "mode": "rw"}},
        # working_dir=os.path.join(mount_path, "server"),
    )

    short_id = container.short_id
    logger_print("attaching to: %s" % short_id)
    # ref: https://www.howtogeek.com/devops/how-to-detach-from-a-docker-container-without-stopping-it/
    if os.name == "nt":
        logger_print("unable to configure detach keys on windows.")
        os.system(f"docker attach {short_id}")
    else:
        os.system(f'docker attach {short_id} --detach-keys="{config.DETACH_KEYS}"')
    # while True:
#     # exit_code = os.system(f"docker attach {short_id} --detach-keys '{config.DETACH_KEYS}'")
#     # exit_code = os.system(f"docker attach {short_id} --detach-keys '{config.DETACH_KEYS}'")
#     exit_code = os.system(f"docker attach {short_id}")
#     if exit_code == 0:
#         break
except:
    import traceback

    traceback.print_exc()
    raise Exception("Error running new container.\nYou may restart the docker engine.")
# logger_print(container.logs())
# import rich

# logger_print(container.__dict__)
# breakpoint()
container_id = container.attrs["Config"]["Hostname"]
container_name = container.attrs["Name"].strip("/")
logger_print(f"Container {container_id} ({container_name}) created.")
logger_print(f"Service available at: http://localhost:{server_port}")
# for line in container.logs(stream=True):
#     logger_print(line.decode('utf-8').strip(), end=None)  # binary string.
