from log_utils import logger_print

"""static & dynamic topology type checking"""

from enum import auto
from strenum import StrEnum

class 基本类型(StrEnum):
    柴油 = auto()
    天然气 = auto()
    氢气 = auto()
    电 = auto()
    水 = auto()
    蒸汽 = auto()
    烟气 = auto()
    导热油 = auto()
    乙二醇 = auto()


class 水类型(StrEnum):
    管道水 = auto()
    自来水 = auto()


class 乙二醇类型(StrEnum):
    冷乙二醇 = auto()
    热乙二醇 = auto()
    冰乙二醇 = auto()


class 管道水类型(StrEnum):
    热水 = auto()
    冷水 = auto()

_mappings = {
    基本类型.水: 水类型,
    水类型.管道水: 管道水类型,
    基本类型.乙二醇: 乙二醇类型,
}

类型泛化表 = {}

def flatten_mappings(c, cs: list):
    if isinstance(c, str):
        cs.append(c)
    elif issubclass(c, StrEnum):
        cs.extend(list(c.__members__.values()))
    else:
        raise Exception("Unsupported type:", type(c))


from error_utils import ErrorManager

with ErrorManager(default_error=f"Found duplicated keys while processing.") as em:
    for v,k in _mappings.items():
        ks = []
        vs = []
        flatten_mappings(k, ks)
        flatten_mappings(v, vs)
        for k in ks:
            for v in vs:
                if k in 类型泛化表.keys():
                    em.append(f"Duplicated: {k} -> {v} (Already have: {类型泛化表[k]})")
                else:
                    类型泛化表[str(k)] = str(v)

类型细分表 = {}
for k, v in 类型泛化表.items():
    if v not in 类型细分表.keys():
        类型细分表[v] = set()
    类型细分表[v].add(k)

def 解析基本类型(t):
    if not isinstance(t, list):
        t = [t]
    t_resolved = set()
    for _t in t:
        if _t in 类型细分表.keys():
            t_resolved.update(_t)
        else:
            t_resolved.add(_t)
    ret = list(t_resolved)
    if t_resolved == set(t):
        return ret
    else:
        return 解析基本类型(ret)