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
    '''
    冰水
    '''

class 水类型(StrEnum):
    热水 = auto()
    冷水 = auto()
    自来水 = auto()
# class 热水(StrEnum):
#     蓄热 = auto()
#     制热 = auto()
# class 冷水(StrEnum):
#     蓄冷 = auto()
#     制冷 = auto()
_mappings = {
    基本类型.水: 水类型,
    # 水类型.冷水: 冷水,
    # 水类型.热水: 热水
}

类型细分表 = {}

def flatten_mappings(c, cs:list):
    if isinstance(c, str):
        cs.append(c)
    elif issubclass(c, StrEnum):
        cs.extend(list(c.__members__.values()))
    else:
        raise Exception("Unsupported type:", type(c))

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
