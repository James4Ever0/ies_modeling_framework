from common_fixtures import *
from export_format_validate import *

{% for devName in devNames %}
    {% set testModel = "测试{}模型".format(devName) %}
def test_{{devName}}_export({{testModel}}):
    timeParam = 10
    [% if devName == "柴油发电"%}
        {{testModel}}.热值 = 1
    {% endif %}
    {{testModel}}.constraints_register()
    for attrName in ['{{devName}}仿真结果', '{{devName}}出力曲线']:
        if obj:=globals().get(attrName, None):
            obj.export(, timeParam)
