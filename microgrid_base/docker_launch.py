"""
create or import docker environment with scripts.
you may use Dockerfile.
"""
import docker

image_name = "microgrid_server"
dockerfile_path = "."

image_storage_dir = "images"
import os
image_storage_gitignore = os.path.join(image_storage_dir, ".gitignore")

if os.path.exists(image_storage_dir):
    if not os.path.isdir(image_storage_dir):
        raise Exception("'%s' exists and is not a directory!"% image_storage_dir)
else:
    os.mkdir(image_storage_dir)

with open(image_storage_gitignore, 'w+') as f:
    f.write("*\n")

if no_imported_image:
    if no_exported_image:
        # first build the image, then export.
        ...
    # load the exported image.

# run the command to launch server within image from here.