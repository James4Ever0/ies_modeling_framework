sources_curl_get = dict(optim="cloudpss_optim.mjson", simu="cloudpss_simu.mjson")
# almost the same as `cloudpss_config2.py`, with slight alternation.

choice = "simu"

mjson_path = sources_curl_get[choice]


import json
import pandas as pd

# question: convert pandas dataframe to markdown table.

with open(mjson_path, "r", encoding="utf-8") as f:
    data = json.loads(f.read())
components = data["component"]
existing_keys = []

headliner = lambda level: "#" * level

for key, val in components.items():
    key_prefix = key.replace("-", "_").split("_")[0]
    if key_prefix not in ["defaultApp"] + existing_keys:
        existing_keys.append(key_prefix)
        print(key_prefix)

        # shall create this table for every device.
        params = val["param"]
        input_types = list(params.keys())
        for input_type in input_types:
            component_info = []
            input_data = params[input_type]
            for k, v in input_data["params"].items():
                valDict = {"ID": k}
                # valDict ={"InputType": input_type,"ID": k}
                valDict.update({k0: v0 for k0, v0 in v.items()})
                component_info.append(valDict)

            df = pd.DataFrame(component_info)
            print(f"Data Input {input_type} in {key_prefix}:")
            # print(df.to_string(index=False))
            markdown_table = df.to_markdown(index=False)
            print(markdown_table)

        # component_info.append({"ID": key, "Name":val.get("name"),"Type": val.get("type"), "Thutype": val.get("thutype")})


# with open('cloudpss_file.json', 'w+') as f3:
#     json.dump(data, f3)
