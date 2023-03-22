sources = ["cloudpss_optim_config2.json", "cloudpss_simulation_config2.json"]

# must place all components on the graph to get the data.

import json

for source in sources:
    with open(source, "r", encoding="utf-8") as f:
        data = json.loads(f.read())

    print(data)
