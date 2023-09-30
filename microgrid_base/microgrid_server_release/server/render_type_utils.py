from log_utils import logger_print
from jinja_utils import *
from type_def import *
from parse_params import TYPE_UTILS_MICROGRID_PORTS, TYPE_UTILS_EXTRA_PORTS
import json


def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


def load_type_utils_json_with_added_suffix(fpath):
    fpath += ".json"
    logger_print("Loading:", fpath)
    dat = load_json(fpath)
    return dat


TYPE_UTILS_MICROGRID_PORTS_DATA = load_type_utils_json_with_added_suffix(
    TYPE_UTILS_MICROGRID_PORTS
)
TYPE_UTILS_EXTRA_PORTS_DATA = load_type_utils_json_with_added_suffix(
    TYPE_UTILS_EXTRA_PORTS
)

__all__ = ["TYPE_UTILS_MICROGRID_PORTS_DATA", "TYPE_UTILS_EXTRA_PORTS_DATA", "TYPE_UTILS_MICROGRID_PORTS", "TYPE_UTILS_EXTRA_PORTS"]

if __name__ == "__main__":

    # def parse_leftover(leftover):
    #     segments = leftover.split(";")
    #     ret = []
    #     for s in segments:
    #         s = s.strip()
    #         if s:
    #             ret.append(s)
    #     return ret
    
    def rule_parser(rule):
        rule = rule.replace("：",":").replace("；",";")
        segments = rule.split(":")
        if len(segments) == 1:
            header = None
            leftover = segments[0]
        elif len(segments) == 2:
            header = segments[0].strip()
            assert header, "empty header at rule: %s" % rule
            leftover = segments[1]
        else:
            raise Exception("Invalid segment count: %d\nSegments: %s" % (len(segments), str(segments)))
        content = leftover.strip()
        assert content, "empty content at rule: %s" % rule
        # content = parse_leftover(leftover)
        return header, content
        
    output_path, template_path = code_and_template_path("type_utils")

    render_params = {}

    deviceTypeTriplets = []
    deviceTypes = []
    energyTypes = set()

    def assert_is_nonempty_dict(d):
        assert isinstance(d, dict)
        assert d != {}

    能流方向翻译表 = dict(进="input", 出="output")

    def 能流方向翻译(能流方向: str):
        directions = []
        for 方向 in 能流方向.strip():
            if 方向 in 能流方向翻译表.keys():
                directions.append(能流方向翻译表[方向])
            else:
                raise Exception("不存在的方向:" + 方向)
        return directions

    def portDefToEnergyTypes(portDef: dict):
        eTypes = []
        _细分类型 = portDef["细分类型"]
        _基本类型 = portDef["基本类型"]
        candidates = _基本类型 if _细分类型 is None else _细分类型
        for t in candidates.split("/"):
            t_resolved = 解析基本类型(t)
            eTypes.extend(t_resolved)
        return eTypes

    for dat, fpath in {
        TYPE_UTILS_MICROGRID_PORTS: TYPE_UTILS_MICROGRID_PORTS_DATA,
        TYPE_UTILS_EXTRA_PORTS: TYPE_UTILS_EXTRA_PORTS_DATA,
    }.items():
        logger_print("Parsing:", fpath)
        # dat = load_json(fpath + ".json")
        for devType, devDict in dat.items():
            logger_print("parsing devType:", devType)
            assert_is_nonempty_dict(devDict)
            for devSubType, devDef in devDict.items():
                assert devSubType != "null"
                assert len(devSubType) > 0
                logger_print("parsing devSubType:", devSubType)
                deviceTypes.append(devSubType)
                ports = devDef["ports"]
                assert_is_nonempty_dict(ports)
                rules = devDef["rules"]
                requirements = devDef["requirements"]
                requiredPortFrontendNameToPortPossibleStates = {
                    portName: ["idle"] + 能流方向翻译(portDef["能流方向"])
                    for portName, portDef in ports.items()
                }
                requiredPortFrontendNameToEnergyTypes = {
                    portName: portDefToEnergyTypes(portDef)
                    for portName, portDef in ports.items()
                }
                for _, etypes in requiredPortFrontendNameToEnergyTypes.items():
                    for energyType in etypes:
                        energyTypes.add(energyType)

                deviceTypeTriplets.append(
                    (
                        devSubType,
                        requiredPortFrontendNameToPortPossibleStates,
                        requiredPortFrontendNameToEnergyTypes,
                    )
                )

    render_params["deviceTypeTriplets"] = deviceTypeTriplets

    render_params["deviceTypes"] = deviceTypes
    render_params["energyTypes"] = list(energyTypes)

    load_render_and_format(
        template_path,
        output_path,
        render_params=render_params,
        banner="GENERATING TYPE UTILS",
    )
