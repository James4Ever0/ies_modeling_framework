from log_utils import logger_print

template_path = "macro_test.j2"

from jinja2 import Environment, FileSystemLoader

env = Environment(loader = FileSystemLoader('./'))
tpl = env.get_template(template_path)

script = tpl.render(test='test_string')
logger_print(script)