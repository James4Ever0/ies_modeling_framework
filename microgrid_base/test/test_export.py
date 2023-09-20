from common_fixtures import *
from export_format_validate import *


def test_柴油_export(测试柴油模型):
    timeParam = 10
    测试柴油模型.constraints_register()
    for attrName in ["柴油仿真结果", "柴油出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试柴油模型, timeParam)


def test_电负荷_export(测试电负荷模型):
    timeParam = 10
    测试电负荷模型.constraints_register()
    for attrName in ["电负荷仿真结果", "电负荷出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试电负荷模型, timeParam)


def test_光伏发电_export(测试光伏发电模型):
    timeParam = 10
    测试光伏发电模型.constraints_register()
    for attrName in ["光伏发电仿真结果", "光伏发电出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试光伏发电模型, timeParam)


def test_风力发电_export(测试风力发电模型):
    timeParam = 10
    测试风力发电模型.constraints_register()
    for attrName in ["风力发电仿真结果", "风力发电出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试风力发电模型, timeParam)


def test_柴油发电_export(测试柴油发电模型):
    timeParam = 10
    测试柴油发电模型.燃料热值 = 1
    测试柴油发电模型.constraints_register()
    for attrName in ["柴油发电仿真结果", "柴油发电出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试柴油发电模型, timeParam)


def test_锂电池_export(测试锂电池模型):
    timeParam = 10
    测试锂电池模型.constraints_register()
    for attrName in ["锂电池仿真结果", "锂电池出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试锂电池模型, timeParam)


def test_变压器_export(测试变压器模型):
    timeParam = 10
    测试变压器模型.constraints_register()
    for attrName in ["变压器仿真结果", "变压器出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试变压器模型, timeParam)


def test_变流器_export(测试变流器模型):
    timeParam = 10
    测试变流器模型.constraints_register()
    for attrName in ["变流器仿真结果", "变流器出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试变流器模型, timeParam)


def test_双向变流器_export(测试双向变流器模型):
    timeParam = 10
    测试双向变流器模型.constraints_register()
    for attrName in ["双向变流器仿真结果", "双向变流器出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试双向变流器模型, timeParam)


def test_传输线_export(测试传输线模型):
    timeParam = 10
    测试传输线模型.constraints_register()
    for attrName in ["传输线仿真结果", "传输线出力曲线"]:
        if obj := globals().get(attrName, None):
            obj.export(测试传输线模型, timeParam)
