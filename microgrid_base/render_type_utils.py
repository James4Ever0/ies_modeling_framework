from log_utils import logger_print
from jinja_utils import *
from type_def import *
from parse_params import TYPE_UTILS_MICROGRID_PORTS, TYPE_UTILS_EXTRA_PORTS
import json
from typing import Literal
from constants import UNKNOWN


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
# import rich
# logger_print(TYPE_UTILS_EXTRA_PORTS_DATA)
# # exit()
# breakpoint()
TYPE_UTILS_SPECIAL_PORTS = "<type_utils_special_ports>"

ANY = "/".join(基本类型.__members__.keys())

TYPE_UTILS_SPECIAL_PORTS_DATA = {
    "特殊元件": {
        "单向线": {
            "ports": {
                "输入接口": {
                    "info": None,
                    "细分类型": None,
                    "基本类型": ANY,
                    "能流方向": "进",
                    "必有工况": None,
                },
                "输出接口": {
                    "info": None,
                    "细分类型": None,
                    "基本类型": ANY,
                    "能流方向": "出",
                    "必有工况": None,
                },
            },
            "rules": ["输入接口 进 -> 输出接口 出", "输出接口 出 -> 输入接口 进"],
        },
        "互斥元件": {
            "ports": {
                "互斥接口A": {
                    "info": None,
                    "细分类型": None,
                    "基本类型": ANY,
                    "能流方向": "进出",
                    "必有工况": None,
                },
                "互斥接口B": {
                    "info": None,
                    "细分类型": None,
                    "基本类型": ANY,
                    "能流方向": "进出",
                    "必有工况": None,
                },
                "外部接口": {
                    "info": None,
                    "细分类型": None,
                    "基本类型": ANY,
                    "能流方向": "进出",
                    "必有工况": None,
                },
            },
            "rules": [
                "互斥接口A 进 -> 互斥接口B 空闲; 外部接口 出",
                "互斥接口A 出 -> 互斥接口B 空闲; 外部接口 进",
                "互斥接口B 进 -> 互斥接口A 空闲; 外部接口 出",
                "互斥接口B 出 -> 互斥接口A 空闲; 外部接口 进",
                "外部接口 空闲 -> 互斥接口A 空闲; 互斥接口B 空闲",
            ],
        },
    }
}

connectivity_check_header_prefixes = ["可选连接", "关联连接", "至少连接"]
# if UNKNOWN then the port must not be connected

__all__ = [
    "TYPE_UTILS_MICROGRID_PORTS_DATA",
    "TYPE_UTILS_EXTRA_PORTS_DATA",
    "TYPE_UTILS_MICROGRID_PORTS",
    "TYPE_UTILS_EXTRA_PORTS",
    "TYPE_UTILS_SPECIAL_PORTS",
    "TYPE_UTILS_SPECIAL_PORTS_DATA",
]

if __name__ == "__main__":
    # def parse_leftover(leftover):
    #     segments = leftover.split(";")
    #     ret = []
    #     for s in segments:
    #         s = s.strip()
    #         if s:
    #             ret.append(s)
    #     return ret

    工况翻译 = dict(进="input", 出="output", 空闲="idle")
    必有工况转定义 = dict(
        一直不工作=f"set(conds).difference({{ 'idle', {repr(UNKNOWN)} }}) == set()",
        **{
            k: f"{repr(v)} in conds or {repr(UNKNOWN)} in conds"
            for k, v in 工况翻译.items()
        },
    )
    make_param_list = lambda e: [e + str(i) for i in range(len(k))]
    makeRule = (
        lambda c0, c1: f"{c0} not in [{repr(UNKNOWN)}, 'idle']"
        if c1 is None
        else f"{c0} in [{repr(UNKNOWN)}, {repr(工况翻译[c1])}]"
    )
    makeRuleWithoutUnknown = (
        lambda c0, c1: f"{c0} not in ['idle']"
        if c1 is None
        else f"{c0} in [{repr(工况翻译[c1])}]"
    )

    def parse_rule_side(left_or_right: str):
        left_or_right = left_or_right.strip()
        comps = left_or_right.split(";")
        ret = []
        for c in comps:
            c = c.strip()
            if len(c) > 0:
                cs = c.split()
                assert len(cs) >= 1, f"invalid rule segment: {c}"
                assert len(cs) <= 2, f"invalid rule segment: {c}"
                if len(cs) == 1:
                    cs += [None]
                ret.append(tuple(cs))
        return ret

    def parse_rule_key(content):
        k = [c0 for c0, _ in content]
        k = tuple(set(k))
        return k

    def replace_with_table(content, table):
        ret = content
        for k, v in table.items():
            ret = ret.replace(k, v)
        return ret

    def replace_as_cond_or_etype(
        rule_definition: str, rule_key: tuple[str], target: Literal["cond", "etype"]
    ):
        translation_table = {k: f"{target}{i}" for i, k in enumerate(rule_key)}
        ret = replace_with_table(rule_definition, translation_table)
        return ret

    def parse_rule(rule):
        _, content = rule_parser(rule)
        _left, _right = content.split("->")
        left = parse_rule_side(_left)
        right = parse_rule_side(_right)
        k = parse_rule_key(left + right)
        assert len(left) == 1, f"abnormal rule because of multiple left side: {rule}"
        # v_left = makeRule(*left[0])
        v_left = makeRuleWithoutUnknown(*left[0])
        v_right = ", ".join([makeRule(*r) for r in right])
        v = f"all([{v_right}]) if {v_left} else True"
        v = replace_as_cond_or_etype(v, k, "cond")
        return k, v

    def parse_requirement(requirement):
        header, _content = rule_parser(requirement)
        content = parse_rule_side(_content)
        k = parse_rule_key(content)
        if header == "互斥":
            v = ", ".join([f"int({makeRule(c0, c1)})" for c0, c1 in content])
            v = f"sum([{v}]) <= 1"
            v = replace_as_cond_or_etype(v, k, "cond")
        elif header == "冷热互斥":
            c0s = [c0 for c0, _ in content]
            c0s = ", ".join(c0s)
            enforce_heat_or_cold = (
                lambda heat_or_cold: f"all([{repr(heat_or_cold)} in it or it == {repr(UNKNOWN)} for it in [{c0s}]])"
            )
            v = " or ".join([enforce_heat_or_cold(e) for e in ["冷", "热"]])
            v = replace_as_cond_or_etype(v, k, "etype")
        elif (
            isinstance(header, str)
            and header.split("[")[0] in connectivity_check_header_prefixes
        ):
            # skipped for now.
            # use 'and' to join all together
            # if has optional ports, then do not add connectivity enforcement to all ports
            ...
        else:
            raise Exception("unknown header:", header, "content:", content)
        return k, v

    def rule_parser(rule):
        rule = rule.replace("：", ":").replace("；", ";")
        segments = rule.split(":")
        if len(segments) == 1:
            header = None
            leftover = segments[0]
        elif len(segments) == 2:
            header = segments[0].strip()
            assert header, "empty header at rule: %s" % rule
            leftover = segments[1]
        else:
            raise Exception(
                "Invalid segment count: %d\nSegments: %s"
                % (len(segments), str(segments))
            )
        content = leftover.strip()
        assert content, "empty content at rule: %s" % rule
        # content = parse_leftover(leftover)
        return header, content

    output_path, template_path = code_and_template_path("type_utils")

    render_params = {}

    deviceTypeTriplets = []
    deviceTypes = []
    energyTypes = set()

    port_verifier_lookup_table = {}
    conjugate_port_verifier_constructor_lookup_table = {}

    def assert_is_nonempty_dict(d):
        assert isinstance(d, dict)
        assert d != {}

    能流方向翻译表 = dict(进="input", 出="output")

    def 能流方向翻译(能流方向):
        directions = []
        if 能流方向:
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
        if candidates is None:
            raise Exception("No candidates")
            # breakpoint()
        for t in candidates.split("/"):
            # if isinstance(t, list):
            #     if set(t) == set(['醇', '乙', '二']): breakpoint()
            # logger_print('t:', t, type(t))
            t_resolved = 解析基本类型(t)
            eTypes.extend(t_resolved)
        logger_print(eTypes)
        return eTypes

    for fpath, dat in {
        TYPE_UTILS_MICROGRID_PORTS: TYPE_UTILS_MICROGRID_PORTS_DATA,
        TYPE_UTILS_EXTRA_PORTS: TYPE_UTILS_EXTRA_PORTS_DATA,  # TODO: add synthetic data here.
        TYPE_UTILS_SPECIAL_PORTS: TYPE_UTILS_SPECIAL_PORTS_DATA,
    }.items():
        logger_print("Parsing:", fpath)
        # dat = load_json(fpath + ".json")
        # breakpoint()
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
                requiredPortFrontendNameToPortPossibleStates = {}
                requiredPortFrontendNameToEnergyTypes = {}
                device_port_verifier_lookup_table = {}

                for portName, portDef in ports.items():
                    requiredPortFrontendNameToPortPossibleStates[portName] = [
                        "idle"
                    ] + 能流方向翻译(portDef["能流方向"])
                    requiredPortFrontendNameToEnergyTypes[
                        portName
                    ] = portDefToEnergyTypes(portDef)

                    cond_segment_list = []

                    必有工况 = portDef["必有工况"]
                    if 必有工况:
                        for item in 必有工况.split("/"):
                            cond_segment = 必有工况转定义[item]
                            cond_segment_list.append(cond_segment)

                    verifier_definition = " or ".join(
                        [f"({cond_segment})" for cond_segment in cond_segment_list]
                    )

                    if verifier_definition:
                        device_port_verifier_lookup_table[
                            portName
                        ] = f"lambda conds: {verifier_definition}"

                if device_port_verifier_lookup_table:
                    port_verifier_lookup_table[
                        devSubType
                    ] = device_port_verifier_lookup_table

                for _, etypes in requiredPortFrontendNameToEnergyTypes.items():
                    for energyType in etypes:
                        energyTypes.add(energyType)

                _conjugate_verifiers = {}
                rule_list = devDef["rules"]
                requirement_list = devDef["requirements"]
                # tuple of port names
                # "lambda cond0, cond1: ..."

                for rule in rule_list:
                    k, v = parse_rule(rule)
                    _conjugate_verifiers[k] = _conjugate_verifiers.get(k, []) + [v]

                for requirement in requirement_list:
                    k, v = parse_requirement(requirement)
                    _conjugate_verifiers[k] = _conjugate_verifiers.get(k, []) + [v]

                conjugate_verifiers = {}

                for k, v in _conjugate_verifiers.items():
                    lambda_params = ", ".join(
                        make_param_list("cond") + make_param_list("etype")
                    )
                    v = " and ".join([f"({_v})" for _v in v])
                    v = f"lambda {lambda_params}: {v}"
                    conjugate_verifiers[k] = v

                if conjugate_verifiers:
                    for k in conjugate_verifiers.keys():
                        for e_k in k:
                            assert (
                                e_k in ports.keys()
                            ), f"found nonexistant key {e_k} at device {devSubType}"
                    conjugate_verifiers_repr = ", ".join(
                        [f"{repr(k)}: {v}" for k, v in conjugate_verifiers.items()]
                    )
                    conjugate_verifiers_repr = f"{{{conjugate_verifiers_repr}}}"
                    conjugate_verifiers_constructor = f"lambda port_kind_to_port_name: {{tuple([port_kind_to_port_name[it] for it in k]): v for k, v in {conjugate_verifiers_repr}.items()}}"
                    conjugate_port_verifier_constructor_lookup_table[
                        devSubType
                    ] = conjugate_verifiers_constructor

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
    # breakpoint()
    render_params["port_verifier_lookup_table"] = port_verifier_lookup_table
    render_params[
        "conjugate_port_verifier_constructor_lookup_table"
    ] = conjugate_port_verifier_constructor_lookup_table

    load_render_and_format(
        template_path,
        output_path,
        render_params=render_params,
        banner="GENERATING TYPE UTILS",
    )
