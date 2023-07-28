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
context_path = "../../"
dockerfile_path = "./jubilant-adventure2/microgrid_base/Dockerfile"

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
    print("image not found: %s" % image_tag)
    if not os.path.exists(image_path):
        # first build the image, then export.
        print("building image...")
        client.images.build(
            path=context_path, tag=image_tag, dockerfile=dockerfile_path, quiet=False
        )
        image = client.images.get(image_tag)
        # image.save()
        print("saving image...")
        with open(image_storage_dir, "wb") as f:
            for chunk in image.save():
                f.write(chunk)
    else:
        print("loading image...")
        with open(image_storage_dir, "rb") as f:
            data = f.read()
            client.images.load(data)

    # load the exported image.
print("running container...")
# run the command to launch server within image from here.
container = client.containers.run(
    image_tag, remove=True, command="echo 'hello world'", detach=True
)
# print(container.logs())

for line in container.logs(stream=True):
    print(line.strip())
