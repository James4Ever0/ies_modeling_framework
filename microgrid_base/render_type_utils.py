from log_utils import logger_print
from jinja_utils import *
from type_def import *
from parse_params import TYPE_UTILS_MICROGRID_PORTS, TYPE_UTILS_EXTRA_PORTS
import json
from typing import Literal
from constants import UNKNOWN

互斥 = "互斥"
冷热互斥 = "冷热互斥"

UNKNOWN_REPR = repr(UNKNOWN)

可选连接 = "可选连接"
关联连接 = "关联连接"
至少连接 = "至少连接"

class AppendableDict(dict):
    def __init__(self, *args, **kwargs):
        super(AppendableDict, self).__init__(*args, **kwargs)

    def append(self, key, value):
        if key in self:
            self[key].append(value)
        else:
            self[key] = [value]


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
            "requirements": []
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
            "requirements": []
        },
    }
}

connectivity_check_header_prefixes = [可选连接, 关联连接, 至少连接]
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
        一直不工作=f"set(conds).difference({{ 'idle', {UNKNOWN_REPR} }}) == set()",
        **{
            k: f"{repr(v)} in conds or {UNKNOWN_REPR} in conds"
            for k, v in 工况翻译.items()
        },
    )
    make_param_list = lambda e: [e + str(i) for i in range(len(k))]
    makeRule = (
        lambda c0, c1: f"{c0} not in [{UNKNOWN_REPR}, 'idle']"
        if c1 is None
        else f"{c0} in [{UNKNOWN_REPR}, {repr(工况翻译[c1])}]"
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

    def generate_optional_connectivity_rule(port_names, optional_port_names):
        remained_et_params = [
            f"etype{i}"
            for i, pn in enumerate(port_names)
            if pn not in optional_port_names
        ]
        v = "True"
        if remained_et_params != []:
            connectivity_check_rule_content = ", ".join(
                [f"{pn_et} != {UNKNOWN_REPR}" for pn_et in remained_et_params]
            )
            v = f"all([{connectivity_check_rule_content}])"
        return v

    def parse_requirement(requirement, port_names):
        header, _content = rule_parser(requirement)
        content = parse_rule_side(_content)
        k = parse_rule_key(content)
        t = splited_header = (
            None if not isinstance(header, str) else header.split("[")[0]
        )
        exc = Exception("unknown header:", header, "content:", content)
        if header == 互斥:
            v = ", ".join([f"int({makeRuleWithoutUnknown(c0, c1)})" for c0, c1 in content])
            # v = ", ".join([f"int({makeRule(c0, c1)})" for c0, c1 in content])
            v = f"sum([{v}]) <= 1"
            v = replace_as_cond_or_etype(v, k, "cond")
        elif header == 冷热互斥:
            c0s = [c0 for c0, _ in content]
            c0s = ", ".join(c0s)
            enforce_heat_or_cold = (
                lambda heat_or_cold: f"all([{repr(heat_or_cold)} in it or it == {UNKNOWN_REPR} for it in [{c0s}]])"
            )
            v = " or ".join([enforce_heat_or_cold(e) for e in ["冷", "热"]])
            v = replace_as_cond_or_etype(v, k, "etype")
        elif (
            # isinstance(header, str)
            # and
            splited_header
            in connectivity_check_header_prefixes
        ):
            # port_candidates = [c0 for c0, _ in content]
            # port_candidates = k
            # skipped for now.
            # use 'and' to join all together
            et_param = ",".join([f"etype{i}" for i in range(len(k))])
            # et_param = ",".join([f"etype{i}" for i in range(len(port_names))])
            # if has optional ports, then do not add connectivity enforcement to all ports
            if splited_header == 可选连接:  # we need to have the port list later
                v = generate_optional_connectivity_rule(port_names, k)
                k = port_names
            elif splited_header == 关联连接:
                v = f"sum([int(it != {UNKNOWN_REPR}) for it in [{et_param}]]) in [0, {len(k)}]"
            elif splited_header == 至少连接:  # 获得至少连接的接口数量
                至少连接的接口数量 = int(header.split("[")[-1].strip("]"))
                v = f"sum([int(it != {UNKNOWN_REPR}) for it in [{et_param}]]) >= {至少连接的接口数量}"
            else:
                raise exc
        else:
            raise exc
        return k, v, t

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

                _conjugate_verifiers = AppendableDict()
                # _conjugate_verifiers = {}
                rule_list = devDef["rules"]
                requirement_list = devDef["requirements"]

                port_names = tuple(ports.keys())
                # tuple of port names
                # "lambda cond0, cond1: ..."

                for rule in rule_list:
                    k, v = parse_rule(rule)
                    _conjugate_verifiers.append(k, v)
                    # _conjugate_verifiers[k] = _conjugate_verifiers.get(k, []) + [v]

                has_optional_port_rule = False

                for requirement in requirement_list:
                    k, v, t = parse_requirement(requirement, port_names)
                    # k, v, t = parse_requirement(requirement)
                    if t == 可选连接:
                        has_optional_port_rule = True
                        # k = port_names
                    _conjugate_verifiers.append(k, v)
                    # _conjugate_verifiers[k] = _conjugate_verifiers.get(k, []) + [v]

                if not has_optional_port_rule:
                    v = generate_optional_connectivity_rule(port_names, [])
                    k = port_names
                    _conjugate_verifiers.append(k, v)

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
