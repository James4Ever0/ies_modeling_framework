sources = ["cloudpss_optim_config2.json", "cloudpss_simulation_config2.json"]

# must place all components on the graph to get the data.
# like: https://ies.cloudpss.net:8201/editor/getComponentForHeat/?id=157
# but not all components are HeatComponents
# id is coming from the graph.

import json

for source in sources:
    with open(source, "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    # print(data)
    components = data['component']
    existing_keys = []
    for key, val in components.items():
        key_prefix = key.split("_")
        if key_prefix not in ['defaultApp']+existing_keys:
            existing_keys.append(key_prefix)
            print(key_prefix)
# with open('cloudpss_file.json', 'w+') as f3:
#     json.dump(data, f3)



