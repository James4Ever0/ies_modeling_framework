import requests
import json

with open("test_graph_data.json",'r') as f:
    data = f.read()
    data_dict = json.loads(data)