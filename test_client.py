import requests
import json
from test_server_client_configs import *


with open(TEST_GRAPH_CONFIG_PATH,'r') as f:
    data = f.read()
    data_dict = json.loads(data)


r = requests.post(upload_url,data={"data":data_dict}) # just upload the graph, nothing more.
status_code = r.status_code
r_json = r.json()
import rich
rich.print(r_json)
print("___RESPONSE___")