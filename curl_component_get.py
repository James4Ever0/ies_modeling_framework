template_paths = dict(
    optim="curl_optim_component_get.sh.j2", simu="curl_simu_component_get.sh.j2"
)

import jinja2
from jinja2 import StrictUndefined

for template_path in template_paths:
    with open(template_path,'r', encoding='utf-8') as f:
        source = f.read()
        template = jinja2.Template(source = source, undefined=StrictUndefined)