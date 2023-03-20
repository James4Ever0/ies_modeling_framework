target_file = "fastapi_client_generated.py"

# let's generate the client from this json.

import os

cmd = f'openapi-python-client generate --path '

os.system(cmd)