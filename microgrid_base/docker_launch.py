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
def build_image(image_tag, dockerfile_path, context_path):
    command = f"docker build -t {image_tag} -f {dockerfile_path} --progress plain {context_path}"
    # print(command)
    exit_code = os.system(command)
    if exit_code:
        raise Exception(f"Abnormal exit code {exit_code} for command:\n{' '*4+command}")


image_tag = "microgrid_server:latest"
intermediate_image_tag = "microgrid_init"
context_path = "../../"
dockerfile_init_path = "Dockerfile_init"
dockerfile_main_path = "Dockerfile_main"

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
        # client.images.build(
        #     path=context_path, tag=image_tag, dockerfile=dockerfile_path, quiet=False
        # )
        build_image(intermediate_image_tag, dockerfile_init_path, context_path)
        build_image(image_tag, dockerfile_main_path, context_path)
        image = client.images.get(image_tag)
        # image.save()
        print("saving image...")
        # with open(image_path, "wb") as f:
        #     for chunk in image.save():
        #         f.write(chunk)
        os.system("docker save -o {} %s" % image_tag)
    else:
        print("loading image...")
        # with open(image_path, "rb") as f:
        #     data = f.read()
        #     client.images.load(data)

    # load the exported image.
print("running container...")
# run the command to launch server within image from here.
container = client.containers.run(
    image_tag, remove=True, command="echo 'hello world'", detach=True
)
# print(container.logs())

for line in container.logs(stream=True):
    print(line.strip())
