from fastapi_server_with_doc import port
import requests

baseurl = f"http://127.0.0.1:{port}/"

url = baseurl + "items"
json_data = dict(
    name="hello", price=1, is_offer=False, myDict={"mydict": {"more": [1, 2, 3]}}
)
r = requests.post(url, json=json_data)
response = r.json()
print("RESP:", response)
print("STATUS_CODE", r.status_code)
