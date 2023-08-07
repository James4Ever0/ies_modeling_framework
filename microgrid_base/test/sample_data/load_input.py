data = open("json_from_browser.txt").read()
import json
eval(f"val = {data}")
json_data = json.loads(val)