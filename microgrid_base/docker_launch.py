"""
create or import docker environment with scripts.
you may use Dockerfile.
"""
import docker
import os

client = docker.from_env()
# client = docker.DockerClient(
#     base_url="//./pipe/docker_engine" if os.name == "nt" else "unix://var/run/docker.sock"
# )

image_tag = "microgrid_server:latest"
dockerfile_path = "."

image_storage_dir = "images"
image_path = os.path.join(image_storage_dir, f"{image_tag.replace(':','_')}.tar")
import os

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
if image_tag not in image_tags:
    if not os.path.exists(image_path):
        # first build the image, then export.
        model = client.images.build(path=dockerfile_path, tag = image_tag)
    # load the exported image.

# run the command to launch server within image from here.
