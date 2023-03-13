import requests
import json
from test_server_client_configs import *


with open("test_graph_data.json",'r') as f:
    data = f.read()
    data_dict = json.loads(data)


r = requests.post(upload_url,data_dict)
status_code = r.status_code
r_json = r.json()