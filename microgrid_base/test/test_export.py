from common_fixtures import *
from export_format_validate import *


def test_柴油信息_export(测试柴油信息模型):
    timeParam = 10
    测试柴油信息模型.constraints_register()
    for attrName in ["柴油信息仿真结果", "柴油信息出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试柴油信息模型, timeParam)


def test_电负荷信息_export(测试电负荷信息模型):
    timeParam = 10
    测试电负荷信息模型.constraints_register()
    for attrName in ["电负荷信息仿真结果", "电负荷信息出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试电负荷信息模型, timeParam)


def test_光伏发电信息_export(测试光伏发电信息模型):
    timeParam = 10
    测试光伏发电信息模型.constraints_register()
    for attrName in ["光伏发电信息仿真结果", "光伏发电信息出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试光伏发电信息模型, timeParam)


def test_风力发电信息_export(测试风力发电信息模型):
    timeParam = 10
    测试风力发电信息模型.constraints_register()
    for attrName in ["风力发电信息仿真结果", "风力发电信息出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试风力发电信息模型, timeParam)


def test_柴油发电信息_export(测试柴油发电信息模型):
    timeParam = 10
    测试柴油发电信息模型.constraints_register()
    for attrName in ["柴油发电信息仿真结果", "柴油发电信息出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试柴油发电信息模型, timeParam)


def test_锂电池信息_export(测试锂电池信息模型):
    timeParam = 10
    测试锂电池信息模型.constraints_register()
    for attrName in ["锂电池信息仿真结果", "锂电池信息出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试锂电池信息模型, timeParam)


def test_变压器信息_export(测试变压器信息模型):
    timeParam = 10
    测试变压器信息模型.constraints_register()
    for attrName in ["变压器信息仿真结果", "变压器信息出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试变压器信息模型, timeParam)


def test_变流器信息_export(测试变流器信息模型):
    timeParam = 10
    测试变流器信息模型.constraints_register()
    for attrName in ["变流器信息仿真结果", "变流器信息出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试变流器信息模型, timeParam)


def test_双向变流器信息_export(测试双向变流器信息模型):
    timeParam = 10
    测试双向变流器信息模型.constraints_register()
    for attrName in ["双向变流器信息仿真结果", "双向变流器信息出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试双向变流器信息模型, timeParam)


def test_传输线信息_export(测试传输线信息模型):
    timeParam = 10
    测试传输线信息模型.constraints_register()
    for attrName in ["传输线信息仿真结果", "传输线信息出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试传输线信息模型, timeParam)
