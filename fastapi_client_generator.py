target_file = "fastapi_client_generated.py"

# let's generate the client from this json.

import os

# suggest you to clean this openapi json (the function name) first:
# https://fastapi.tiangolo.com/advanced/generate-clients/
#
json_file_path = 'fastapi_openapi.json'

# also try to automatically generate appropriate `__init__.py` file so we can have multiple api callers in the same namespace.

cmd = f'openapi-python-client generate --path {json_file_path}' # generate to: chimichang-app-client, with chimichang_app_client wrapped inside.

os.system(cmd)