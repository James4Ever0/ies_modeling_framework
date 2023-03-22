sources = ["cloudpss_optim_config2.json", "cloudpss_simulation_config2.json"]
# sources_curl_get = ['cloudpss_optim.mjson','cloudpss_simu.mjson']

# must place all components on the graph to get the data.
# like: https://ies.cloudpss.net:8201/editor/getComponentForHeat/?id=157
# or: getComponentForCPS

# but not all components are HeatComponents
# id is coming from the json containing svg.

import json
import pandas as pd

# question: convert pandas dataframe to markdown table.

for source in sources:
    with open(source, "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    components = data['component']
    existing_keys = []
    
    
    for key, val in components.items():
        key_prefix = key.replace("-","_").split("_")[0]
        if key_prefix not in ['defaultApp']+existing_keys:
            existing_keys.append(key_prefix)
            print(key_prefix)
            
            # val_prefix=val
            # if val_prefix not in ['defaultApp']+existing_vals:
            #     existing_vals.append(val_prefix)
            #     print(val_prefix)
            
            # shall create this table for every device.
            params = val['param']
            input_types = list(params.keys())
            for input_type in input_types:
                component_info = []
                input_data = params[input_type]
                for k,v in input_data['params'].items():
                    valDict ={"ID": k}
                    # valDict ={"InputType": input_type,"ID": k}
                    valDict.update({k0:v0 for k0,v0 in v.items()})
                    component_info.append(valDict)
                    
                df = pd.DataFrame(component_info)
                print(f"Data Input {input_type} in {key_prefix}:")
                # print(df.to_string(index=False))
                markdown_table = df.to_markdown(index=False)
                print(markdown_table)
            
            # component_info.append({"ID": key, "Name":val.get("name"),"Type": val.get("type"), "Thutype": val.get("thutype")})
    

        

# with open('cloudpss_file.json', 'w+') as f3:
#     json.dump(data, f3)



