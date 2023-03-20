target_file = "fastapi_client_generated.py"

# let's generate the client from this json.

import os

# suggest you to clean this openapi json first:
# https://fastapi.tiangolo.com/advanced/generate-clients/
#
json_file_path = 'fastapi_openapi.json'

cmd = f'openapi-python-client generate --path {json_file_path}' # generate to: chimichang-app-client, with chimichang_app_client wrapped inside.

os.system(cmd)