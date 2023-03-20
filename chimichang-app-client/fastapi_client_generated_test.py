port = 9982

import sys

client_location = "D:/project/xianxing/chimichang-app-client"

sys.path.append(client_location)

# where's the path?

import chimichang_app_client as CA
from chimichang_app_client.api.default import *
import chimichang_app_client.api.users as USERS
import chimichang_app_client.models as M

client = CA.Client(base_url=f"http://localhost:{port}", verify_ssl=False, raise_on_unexpected_status=True, timeout=5)

someRandomDict = M.ItemMydict.from_dict(dict(a=1))  # strange it is
myItem = M.Item(name="myName", price=20, is_offer=True, my_dict=someRandomDict)

data = POST.sync(client=client, json_body=myItem)

# breakpoint()
print("RESPONSE:", data)
