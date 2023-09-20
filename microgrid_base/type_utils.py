from log_utils import logger_print

"""static & dynamic topology type checking"""

from enum import auto
from strenum import StrEnum

class 基本类型(StrEnum):
    柴油 = auto()
    天然气 = auto()
    电 = auto()
    水 = auto()
    蒸汽 = auto()

class 水类型(StrEnum):
    热水 = auto()
    冷水 = auto()
    冰水 = auto()

_mappings = {
    基本类型.水: 水类型
}

类型细分表 = {}

def flatten_mappings(k, ks:list):
    if isinstance(k, str):
        ks.append(k)
    elif issubclass(k, StrEnum):
        ks.extend(list(k.__members__.values()))
    else:
        raise Exception("Unsupported type:", type(k))

from error_utils import ErrorManager

with ErrorManager(default_error = f"Found duplicated keys while processing.") as em:
    for k, v in _mappings.items():
        ks = []
        vs = []
        flatten_mappings(k,ks)
        flatten_mappings(v,vs)
        for k in ks:
            for v in vs:
                if k in 类型细分表.keys():
                    em.append(f"Duplicated: {k} -> {v} (Already have: {类型细分表[k]})")
                else:
                    类型细分表[k] = v
