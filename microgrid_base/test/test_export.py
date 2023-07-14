from common_fixtures import *
from export_format_validate import *

{% for devName in devNames %}
    {% set testModel = "测试{}模型".format(devName) %}
def test_{{devName}}_export({{testModel}}):
    [% if devName == "柴油发电"%}
        {{testModel}}.热值 = 1
    {% endif %}
    {{testModel}}.constraints_register()
    仿真结果
    出力曲线