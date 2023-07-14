from common_fixtures import *
from export_format_validate import *

{% for devName in devNames %}
    {% set testModel = "测试{}模型".format(devName) %}
def test_{{devName}}_export({{testModel}}):
    if {{testModel}}
    {{testModel}}.constraints_register()
    