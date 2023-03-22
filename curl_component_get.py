template_paths = dict(
    optim="curl_optim_component_get.sh.j2", simu="curl_simu_component_get.sh.j2"
)

id_paths = dict(
    optim="cloudpss_component_optimize_ports.json",
    simu="cloudpss_component_ports.json"
)

import json

def get_ids(id_path:str):
    ids = []
    with open(id_path) as f:
        data = json.loads(f.read())
        cmp = data['cmp']
        for component in cmp:
            _id = component['id']
            ids.append(_id)
    return ids
ids = {key: get_ids(val) for key, val in id_paths.items()}

import jinja2
from jinja2 import StrictUndefined
import subprocess

output_script_path = "script.sh"

cmd = ['bash', output_script_path]
# access_paths = ['CPS','Heat']
access_paths = ['Heat']
# there is no component using 'CPS'
# simply add a new line after each call.
import os
for key, template_path in template_paths.items():
    output_path = f"cloudpss_{key}.mjson"
    os.system(f"rm -rf {output_path}")
    with open(template_path,'r', encoding='utf-8') as f:
        source = f.read()
        template = jinja2.Template(source = source, undefined=StrictUndefined)
        for _id in ids[key]:
            for access_path in access_paths:
                script_content = template.render(access_path=access_path, id=_id, output_path=output_path)
                with open(output_script_path, 'w+') as f0:
                    f0.write(script_content)
                output = subprocess.getoutput(cmd)
                print("ACCESS PATH:", access_path, "ID:", _id)
                print("OUTPUT?", output[:20])
                with open(output_path, 'a+', encoding='utf-8') as f1:
                    f1.write('\n')