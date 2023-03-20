
from fastapi_server_with_doc import port # 9982?
client_location = 'D:/project/xianxing/chimichang-app-client'

CODE = f"""
port = {port}

import sys
client_location ="{client_location}"

sys.path.append(client_location)

# where's the path?

import chimichang_app_client as CA
# import chimichang_app_client.api.default.post_item_api_name_items_post as POST
from chimichang_app_client.api.default import * # in a hurry?
import chimichang_app_client.api.users as USERS
import chimichang_app_client.models as M

client = CA.Client(base_url=f"http://localhost:{{port}}", verify_ssl=False, raise_on_unexpected_status=True, timeout=5)

someRandomDict=M.ItemMydict.from_dict(dict(a = 1))# strange it is
myItem = M.Item(name='myName', price=20,is_offer=True, my_dict = someRandomDict)

data = post_item_api_name_items_post.sync(client=client,json_body=myItem)

# breakpoint()
print("RESPONSE:", data)

"""

import os
filepath = os.path.join(client_location,os.path.basename(__file__))

with open(filepath,'w+',encoding='utf-8') as f:
    f.write(CODE)

import subprocess

subprocess.run(['python', filepath],cwd=client_location)