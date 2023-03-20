
from fastapi_server_with_doc import port # 9982?
client_location = 'D:/project/xianxing/chimichang-app-client'

CODE = f"""
port = {port}

import sys
client_location ="{client_location}"

sys.path.append(client_location)

# where's the path?

import chimichang_app_client  as CA
import chimichang_app_client.api.default as DEFAULT
import chimichang_app_client.api.users as USERS
import chimichang_app_client.models as M

# breakpoint()
"""
import os
filepath = os.path.join(client_location,os.path.basename(__file__))

with open(filepath,'w+',encoding='utf-8') as f:
    f.write(CODE)

import subprocess

subprocess.run(['python', filepath],cwd=client_location)