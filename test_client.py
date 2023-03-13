import requests
import json

port = 3398

with open("test_graph_data.json",'r') as f:
    data = f.read()
    data_dict = json.loads(data)

url_base= f"http://localhost:{port}"

get_url = lambda suffix: f"{url_base}/{suffix}"

# will refuse connection if current task count is above 3.

url = get_url("upload_graph")

async_url = get_url("upload_graph_async")
check_result_async = get_url("check_result_async")

r = requests.post(url,data_dict)
status_code = r.status_code
r_json = r.json()