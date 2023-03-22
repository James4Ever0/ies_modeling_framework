template_paths = dict(
    optim="curl_optim_component_get.sh.j2", simu="curl_simu_component_get.sh.j2"
)

import jinja2
from jinja2 import StrictUndefined
import subprocess

access_paths = ['CPS','Heat']

for template_path in template_paths:
    with open(template_path,'r', encoding='utf-8') as f:
        source = f.read()
        template = jinja2.Template(source = source, undefined=StrictUndefined)
        template.render(access_path=access_path, id=_id)