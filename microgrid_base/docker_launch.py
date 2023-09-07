from log_utils import logger_print
import sys

"""
create or import docker environment with scripts.

you may use Dockerfile.
"""
# TODO: replace with docker compose
# TODO: put this into release archive

import docker
import os
from config_utils import getConfig
from pydantic import BaseModel, Field


class DockerLauncherConfig(BaseModel):
    NO_HALFDONE: bool = Field(
        default=False,
        title="Disable pulling half-done images from Dockerhub and build from ubuntu base image.",
    )
    # FORCE_UPDATE: bool = Field(
    #     default=False,
    #     title="Force updating ultimate docker image even if up-to-date (not older than 7 days).",
    # )
    # UPDATE_INTERVAL_IN_DAYS: int = Field(
    #     default=7, title="Update/rebuild image interval in days"
    # )


config = getConfig(DockerLauncherConfig)


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
    command = f"docker build -t {image_tag} -f {dockerfile_path} --progress plain {context_path}"
    # logger_print(command)
    exit_code = os.system(command)
    if exit_code:
        raise Exception(f"Abnormal exit code {exit_code} for command:\n{' '*4+command}")
    return True


# import datetime

update_image_tag = "microgrid_update:latest"
# update_interval = datetime.timedelta(days=config.UPDATE_INTERVAL_IN_DAYS)
# update_image_file_path = os.path.join(os.path.expanduser("~"), ".microgrid_update")

final_image_tag = "microgrid_docplex:latest"
image_tag = "microgrid_server:latest"
remote_image_tag = "agile4im/microgrid_server:latest"
intermediate_image_tag = "microgrid_init"
context_path = "../../"

def docker_exec(cmd):
    logger_print("executing docker command: {}".format(cmd))
    os.system(f"docker {cmd}")


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

images = client.images.list()
image_tags = [tag for image in images for tag in image.tags]
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
import progressbar

# for container in progressbar.progressbar(all_containers):
#     container.stop()
# logger_print("pruning stopped containers...")
# client.containers.prune()
import easyprocess, func_timeout


def killAndPruneAllContainers():
    proc = easyprocess.EasyProcess("docker container ls").call()
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
host_path = "./microgrid_server_release"

if RELEASE_ENV:
    host_path = "../." + host_path
host_mount_path = os.path.abspath(host_path)
# don't need this workaround when using docker-py.
if os.name == "nt":
    disk_symbol, pathspec = host_mount_path.split(":")
    pathspec = pathspec.replace("\\", "/")
    host_mount_path = f"//{disk_symbol.lower()}{pathspec}"


killAndPruneAllContainers()

build_image(update_image_tag, dockerfile_update_path, context_path)

# BUG: error while creating mount source path
# FIX: restart the docker engine (win) if fail to run container (usually caused by unplugging anything mounted by volume)
logger_print("running container...")
try:
    container = client.containers.run(
        # final_image_tag,
        update_image_tag,
        # image_tag,
        environment=dict(os.environ),  # may override normal environment variables?
        # remove=True,
        remove=False, # to get the image hash.
        # command="ls -lth microgrid",
        # command="bash fastapi_tmuxp.sh",
        command="bash -c 'cd ../server && bash fastapi_tmuxp.sh windows'",
        # command="bash -c 'cd microgrid/server && bash fastapi_tmuxp.sh windows'",
        # command="bash -c 'cd microgrid/server && ls -lth .'",
        # command="echo 'hello world'",
        detach=True,
        # we need to monitor this.
        tty=True,
        ports={f"{(server_port:=9870)}/tcp": server_port},
        volumes={
            host_mount_path: {"bind": (mount_path := "/root/microgrid"), "mode": "rw"}
        },
        # volumes={"<HOST_PATH>": {"bind": "<CONTAINER_PATH>", "mode": "rw"}},
        # working_dir=os.path.join(mount_path, "server"),
    )

    short_id = container.short_id
    logger_print("attaching to: %s" % short_id)
    os.system(f"docker attach {short_id}")
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
