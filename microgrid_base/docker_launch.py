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

RELEASE_ENV = False
if rel_curdir != "microgrid_base":
    RELEASE_ENV = True
    os.system(
        f"sed -i 's/jubilant-adventure2\\/microgrid_base/{rel_pardir}\\/init/g' Dockerfile_patch"
        # f"sed -i 's/jubilant-adventure2\\/microgrid_base/{rel_pardir}\\/init/g' Dockerfile_*"
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


final_image_tag = "microgrid_docplex:latest"
image_tag = "microgrid_server:latest"
remote_image_tag = "agile4im/microgrid_server:latest"
intermediate_image_tag = "microgrid_init"
context_path = "../../"
dockerfile_init_path = "Dockerfile_init"
dockerfile_main_path = "Dockerfile_main"
dockerfile_patch_path = "Dockerfile_patch"


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
            if "-noremote" not in sys.argv:
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
all_containers = client.containers.list(all=True)
logger_print("stopping running containers...")
import progressbar

for container in progressbar.progressbar(all_containers):
    container.stop()
logger_print("pruning stopped containers...")
client.containers.prune()

# BUG: error while creating mount source path
# FIX: restart the docker engine (win) if fail to run container (usually caused by unplugging anything mounted by volume)
logger_print("running container...")
try:
    container = client.containers.run(
        final_image_tag,
        # image_tag,
        environment=dict(os.environ),  # may override normal environment variables?
        remove=True,
        # remove=False, # to get the image hash.
        # command="ls -lth microgrid",
        # command="bash fastapi_tmuxp.sh",
        command="bash -c 'cd microgrid/init && bash init.sh && cd ../server && bash fastapi_tmuxp.sh windows'",
        # command="bash -c 'cd microgrid/server && ls -lth .'",
        # command="echo 'hello world'",
        detach=True,
        tty=True,
        ports={f"{(server_port:=9870)}/tcp": server_port},
        volumes={
            host_mount_path: {"bind": (mount_path := "/root/microgrid"), "mode": "rw"}
        },
        # volumes={"<HOST_PATH>": {"bind": "<CONTAINER_PATH>", "mode": "rw"}},
        # working_dir=os.path.join(mount_path, "server"),
    )
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
