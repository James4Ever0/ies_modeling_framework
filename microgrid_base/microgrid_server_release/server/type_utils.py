from log_utils import logger_print
from type_def import *
import os

"""static & dynamic topology type checking"""

deviceTypes = [
    "柴油",
    "电负荷",
    "光伏发电",
    "风力发电",
    "柴油发电",
    "锂电池",
    "变压器",
    "双向变压器",
    "变流器",
    "双向变流器",
    "传输线",
    "市政自来水",
    "天然气",
    "电网",
    "氢气",
    "冷负荷",
    "热负荷",
    "蒸汽负荷",
    "氢负荷",
    "燃气发电机",
    "蒸汽轮机",
    "氢燃料电池",
    "平板太阳能",
    "槽式太阳能",
    "余热热水锅炉",
    "余热蒸汽锅炉",
    "浅层地热井",
    "中深层地热井",
    "地表水源",
    "水冷冷却塔",
    "余热热源",
    "浅层双源四工况热泵",
    "中深层双源四工况热泵",
    "浅层双源三工况热泵",
    "中深层双源三工况热泵",
    "水冷螺杆机",
    "双工况水冷螺杆机组",
    "吸收式燃气热泵",
    "空气源热泵",
    "蒸汽溴化锂",
    "热水溴化锂",
    "电热水锅炉",
    "电蒸汽锅炉",
    "天然气热水锅炉",
    "天然气蒸汽锅炉",
    "电解槽",
    "水蓄能",
    "蓄冰槽",
    "储氢罐",
    "输水管道",
    "蒸汽管道",
    "复合输水管道",
    "水水换热器",
    "复合水水换热器",
    "气水换热器",
]
energyTypes = [
    "柴油",
    "热水",
    "氢气",
    "冷水",
    "冷乙二醇",
    "天然气",
    "导热油",
    "冰乙二醇",
    "蒸汽",
    "热乙二醇",
    "烟气",
    "电",
    "自来水",
]

deviceTypeToTypeInfo = {
    "柴油": {
        "requiredPortFrontendNameToPortPossibleStates": {"燃料接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"燃料接口": ["柴油"]},
    },
    "电负荷": {
        "requiredPortFrontendNameToPortPossibleStates": {"电接口": ["idle", "input"]},
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"]},
    },
    "光伏发电": {
        "requiredPortFrontendNameToPortPossibleStates": {"电接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"]},
    },
    "风力发电": {
        "requiredPortFrontendNameToPortPossibleStates": {"电接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"]},
    },
    "柴油发电": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "燃料接口": ["idle", "input"],
            "电接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"燃料接口": ["柴油"], "电接口": ["电"]},
    },
    "锂电池": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input", "output"]
        },
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"]},
    },
    "变压器": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电输入": ["idle", "input"],
            "电输出": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"电输入": ["电"], "电输出": ["电"]},
    },
    "双向变压器": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电输入": ["idle", "input", "output"],
            "电输出": ["idle", "input", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"电输入": ["电"], "电输出": ["电"]},
    },
    "变流器": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电输入": ["idle", "input"],
            "电输出": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"电输入": ["电"], "电输出": ["电"]},
    },
    "双向变流器": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "储能端": ["idle", "input", "output"],
            "线路端": ["idle", "input", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"储能端": ["电"], "线路端": ["电"]},
    },
    "传输线": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电输入": ["idle", "input", "output"],
            "电输出": ["idle", "input", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"电输入": ["电"], "电输出": ["电"]},
    },
    "市政自来水": {
        "requiredPortFrontendNameToPortPossibleStates": {"水接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"水接口": ["自来水"]},
    },
    "天然气": {
        "requiredPortFrontendNameToPortPossibleStates": {"燃料接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"燃料接口": ["天然气"]},
    },
    "电网": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input", "output"]
        },
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"]},
    },
    "氢气": {
        "requiredPortFrontendNameToPortPossibleStates": {"氢气接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"氢气接口": ["氢气"]},
    },
    "冷负荷": {
        "requiredPortFrontendNameToPortPossibleStates": {"冷源接口": ["idle", "input"]},
        "requiredPortFrontendNameToEnergyTypes": {"冷源接口": ["冷水"]},
    },
    "热负荷": {
        "requiredPortFrontendNameToPortPossibleStates": {"热源接口": ["idle", "input"]},
        "requiredPortFrontendNameToEnergyTypes": {"热源接口": ["热水"]},
    },
    "蒸汽负荷": {
        "requiredPortFrontendNameToPortPossibleStates": {"蒸汽接口": ["idle", "input"]},
        "requiredPortFrontendNameToEnergyTypes": {"蒸汽接口": ["蒸汽"]},
    },
    "氢负荷": {
        "requiredPortFrontendNameToPortPossibleStates": {"氢气接口": ["idle", "input"]},
        "requiredPortFrontendNameToEnergyTypes": {"氢气接口": ["氢气"]},
    },
    "燃气发电机": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "燃料接口": ["idle", "input"],
            "电接口": ["idle", "output"],
            "高温烟气余热接口": ["idle", "output"],
            "缸套水余热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "燃料接口": ["天然气"],
            "电接口": ["电"],
            "高温烟气余热接口": ["烟气"],
            "缸套水余热接口": ["热水"],
        },
    },
    "蒸汽轮机": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "蒸汽接口": ["idle", "input"],
            "电接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"蒸汽接口": ["蒸汽"], "电接口": ["电"]},
    },
    "氢燃料电池": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "氢气接口": ["idle", "input"],
            "电接口": ["idle", "output"],
            "设备余热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "氢气接口": ["氢气"],
            "电接口": ["电"],
            "设备余热接口": ["热水"],
        },
    },
    "平板太阳能": {
        "requiredPortFrontendNameToPortPossibleStates": {"热接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"热接口": ["热水"]},
    },
    "槽式太阳能": {
        "requiredPortFrontendNameToPortPossibleStates": {"热接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"热接口": ["导热油"]},
    },
    "余热热水锅炉": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "烟气接口": ["idle", "input"],
            "制热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"烟气接口": ["烟气"], "制热接口": ["热水"]},
    },
    "余热蒸汽锅炉": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "烟气接口": ["idle", "input"],
            "蒸汽接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"烟气接口": ["烟气"], "蒸汽接口": ["蒸汽"]},
    },
    "浅层地热井": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "output"],
            "热源接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
        },
    },
    "中深层地热井": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "热源接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"], "热源接口": ["热水"]},
    },
    "地表水源": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "output"],
            "热源接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
        },
    },
    "水冷冷却塔": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "水接口": ["idle", "input"],
            "冷源接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "水接口": ["自来水"],
            "冷源接口": ["冷水"],
        },
    },
    "余热热源": {
        "requiredPortFrontendNameToPortPossibleStates": {"热源接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"热源接口": ["热水"]},
    },
    "浅层双源四工况热泵": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "热源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "蓄冷接口": ["idle", "output"],
            "制热接口": ["idle", "output"],
            "蓄热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
            "制冷接口": ["冷水"],
            "蓄冷接口": ["冷水"],
            "制热接口": ["热水"],
            "蓄热接口": ["热水"],
        },
    },
    "中深层双源四工况热泵": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "热源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "蓄冷接口": ["idle", "output"],
            "制热接口": ["idle", "output"],
            "蓄热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
            "制冷接口": ["冷水"],
            "蓄冷接口": ["冷水"],
            "制热接口": ["热水"],
            "蓄热接口": ["热水"],
        },
    },
    "浅层双源三工况热泵": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "热源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "制冰接口": ["idle", "output"],
            "制热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
            "制冷接口": ["冷乙二醇"],
            "制冰接口": ["冰乙二醇"],
            "制热接口": ["热乙二醇"],
        },
    },
    "中深层双源三工况热泵": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "热源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "制冰接口": ["idle", "output"],
            "制热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
            "制冷接口": ["冷乙二醇"],
            "制冰接口": ["冰乙二醇"],
            "制热接口": ["热乙二醇"],
        },
    },
    "水冷螺杆机": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "蓄冷接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "制冷接口": ["冷水"],
            "蓄冷接口": ["冷水"],
        },
    },
    "双工况水冷螺杆机组": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "制冰接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "制冷接口": ["冷乙二醇"],
            "制冰接口": ["冰乙二醇"],
        },
    },
    "吸收式燃气热泵": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "燃料接口": ["idle", "input"],
            "制热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"燃料接口": ["天然气"], "制热接口": ["热水"]},
    },
    "空气源热泵": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "蓄冷接口": ["idle", "output"],
            "制热接口": ["idle", "output"],
            "蓄热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "制冷接口": ["冷水"],
            "蓄冷接口": ["冷水"],
            "制热接口": ["热水"],
            "蓄热接口": ["热水"],
        },
    },
    "蒸汽溴化锂": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "蒸汽接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "蒸汽接口": ["蒸汽"],
            "冷源接口": ["冷水"],
            "制冷接口": ["冷水"],
        },
    },
    "热水溴化锂": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "热水接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "热水接口": ["热水"],
            "冷源接口": ["冷水"],
            "制冷接口": ["冷水"],
        },
    },
    "电热水锅炉": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "制热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"], "制热接口": ["热水"]},
    },
    "电蒸汽锅炉": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "蒸汽接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"], "蒸汽接口": ["蒸汽"]},
    },
    "天然气热水锅炉": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "燃料接口": ["idle", "input"],
            "制热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"燃料接口": ["天然气"], "制热接口": ["热水"]},
    },
    "天然气蒸汽锅炉": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "燃料接口": ["idle", "input"],
            "蒸汽接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"燃料接口": ["天然气"], "蒸汽接口": ["蒸汽"]},
    },
    "电解槽": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "制氢接口": ["idle", "output"],
            "设备余热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "制氢接口": ["氢气"],
            "设备余热接口": ["热水"],
        },
    },
    "水蓄能": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "蓄热接口": ["idle", "input", "output"],
            "蓄冷接口": ["idle", "input", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"蓄热接口": ["热水"], "蓄冷接口": ["冷水"]},
    },
    "蓄冰槽": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "蓄冰接口": ["idle", "input", "output"]
        },
        "requiredPortFrontendNameToEnergyTypes": {"蓄冰接口": ["冰乙二醇"]},
    },
    "储氢罐": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "储氢接口": ["idle", "input", "output"]
        },
        "requiredPortFrontendNameToEnergyTypes": {"储氢接口": ["氢气"]},
    },
    "输水管道": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "输入接口": ["idle", "input", "output"],
            "输出接口": ["idle", "input", "output"],
            "电接口": ["idle", "input"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "输入接口": ["冷水", "热水"],
            "输出接口": ["冷水", "热水"],
            "电接口": ["电"],
        },
    },
    "蒸汽管道": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "输入接口": ["idle", "input", "output"],
            "输出接口": ["idle", "input", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"输入接口": ["蒸汽"], "输出接口": ["蒸汽"]},
    },
    "复合输水管道": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "冷输入接口": ["idle", "input", "output"],
            "热输入接口": ["idle", "input", "output"],
            "冷输出接口": ["idle", "input", "output"],
            "热输出接口": ["idle", "input", "output"],
            "电接口": ["idle", "input"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "冷输入接口": ["冷水"],
            "热输入接口": ["热水"],
            "冷输出接口": ["冷水"],
            "热输出接口": ["热水"],
            "电接口": ["电"],
        },
    },
    "水水换热器": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "输入接口": ["idle", "input", "output"],
            "输出接口": ["idle", "input", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "输入接口": ["热乙二醇", "冷乙二醇", "冰乙二醇", "冷水", "热水", "自来水", "导热油"],
            "输出接口": ["热乙二醇", "冷乙二醇", "冰乙二醇", "冷水", "热水", "自来水", "导热油"],
        },
    },
    "复合水水换热器": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "冷输入接口": ["idle", "input", "output"],
            "热输入接口": ["idle", "input", "output"],
            "冷输出接口": ["idle", "input", "output"],
            "热输出接口": ["idle", "input", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "冷输入接口": ["冷乙二醇", "冰乙二醇", "冷水"],
            "热输入接口": ["热乙二醇", "热水", "导热油"],
            "冷输出接口": ["冷乙二醇", "冰乙二醇", "冷水"],
            "热输出接口": ["热乙二醇", "热水", "导热油"],
        },
    },
    "气水换热器": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "输入接口": ["idle", "input"],
            "输出接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"输入接口": ["蒸汽"], "输出接口": ["热水"]},
    },
}

port_verifier_lookup_table = {
    "电负荷": {
        "电接口": lambda conds: ("input" in conds),
    },
    "光伏发电": {
        "电接口": lambda conds: ("idle" in conds),
    },
    "风力发电": {
        "电接口": lambda conds: ("idle" in conds),
    },
    "锂电池": {
        "电接口": lambda conds: ("input" in conds),
    },
    "冷负荷": {
        "冷源接口": lambda conds: ("input" in conds),
    },
    "热负荷": {
        "热源接口": lambda conds: ("input" in conds),
    },
    "蒸汽负荷": {
        "蒸汽接口": lambda conds: ("input" in conds),
    },
    "氢负荷": {
        "氢气接口": lambda conds: ("input" in conds),
    },
    "水蓄能": {
        "蓄热接口": lambda conds: ("input" in conds) or (set(conds) == {"idle"}),
        "蓄冷接口": lambda conds: ("input" in conds) or (set(conds) == {"idle"}),
    },
    "蓄冰槽": {
        "蓄冰接口": lambda conds: ("input" in conds) or (set(conds) == {"idle"}),
    },
    "储氢罐": {
        "储氢接口": lambda conds: ("input" in conds) or (set(conds) == {"idle"}),
    },
}

conjugate_port_verifier_constructor_lookup_table = {
    "柴油发电": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口", "燃料接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond1 == "input"]) if cond0 == "output" else True
            )
        }.items()
    },
    "变压器": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电输出", "电输入"): lambda cond0, cond1, etype0, etype1: (
                all([cond1 == "input"]) if cond0 == "output" else True
            )
        }.items()
    },
    "双向变压器": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电输出", "电输入"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            )
            and (all([cond1 == "input"]) if cond0 == "output" else True)
            and (sum([int(cond1 == "input"), int(cond0 == "input")]) <= 1)
        }.items()
    },
    "变流器": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电输出", "电输入"): lambda cond0, cond1, etype0, etype1: (
                all([cond1 == "input"]) if cond0 == "output" else True
            )
        }.items()
    },
    "双向变流器": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("储能端", "线路端"): lambda cond0, cond1, etype0, etype1: (
                all([cond1 == "input"]) if cond0 == "output" else True
            )
            and (all([cond0 == "input"]) if cond1 == "output" else True)
            and (sum([int(cond0 == "input"), int(cond1 == "input")]) <= 1)
        }.items()
    },
    "传输线": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电输出", "电输入"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            )
            and (all([cond1 == "input"]) if cond0 == "output" else True)
            and (sum([int(cond1 == "input"), int(cond0 == "input")]) <= 1)
        }.items()
    },
    "燃气发电机": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "电接口",
                "缸套水余热接口",
                "高温烟气余热接口",
                "燃料接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: (
                all([cond3 == "input", cond2 == "output", cond1 == "output"])
                if cond0 == "output"
                else True
            )
            and (
                all([cond3 == "input", cond0 == "output", cond2 == "output"])
                if cond1 == "output"
                else True
            ),
            (
                "电接口",
                "燃料接口",
                "缸套水余热接口",
                "高温烟气余热接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: (
                all([cond1 == "input", cond0 == "output", cond2 == "output"])
                if cond3 == "output"
                else True
            ),
        }.items()
    },
    "蒸汽轮机": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口", "蒸汽接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond1 == "input"]) if cond0 == "output" else True
            )
        }.items()
    },
    "氢燃料电池": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "电接口",
                "氢气接口",
                "设备余热接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond1 == "input", cond2 == "output"])
                if cond0 == "output"
                else True
            )
            and (
                all([cond1 == "input", cond0 == "output"])
                if cond2 == "output"
                else True
            )
        }.items()
    },
    "余热热水锅炉": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("烟气接口", "制热接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            )
        }.items()
    },
    "余热蒸汽锅炉": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("蒸汽接口", "烟气接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond1 == "input"]) if cond0 == "output" else True
            )
        }.items()
    },
    "浅层地热井": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口", "热源接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            ),
            ("电接口", "冷源接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            ),
            ("冷源接口", "热源接口"): lambda cond0, cond1, etype0, etype1: (
                sum([int(cond0 == "output"), int(cond1 == "output")]) <= 1
            ),
        }.items()
    },
    "中深层地热井": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口", "热源接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            )
        }.items()
    },
    "地表水源": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口", "冷源接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            ),
            ("电接口", "热源接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            ),
            ("冷源接口", "热源接口"): lambda cond0, cond1, etype0, etype1: (
                sum([int(cond0 == "output"), int(cond1 == "output")]) <= 1
            ),
        }.items()
    },
    "水冷冷却塔": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "电接口",
                "冷源接口",
                "水接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond0 == "input", cond2 == "input"]) if cond1 == "output" else True
            )
        }.items()
    },
    "浅层双源四工况热泵": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "电接口",
                "冷源接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond0 == "input", cond1 == "input"]) if cond2 == "output" else True
            ),
            (
                "蓄冷接口",
                "冷源接口",
                "电接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond2 == "input", cond1 == "input"]) if cond0 == "output" else True
            ),
            (
                "电接口",
                "热源接口",
                "制热接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond0 == "input", cond1 == "input"]) if cond2 == "output" else True
            ),
            (
                "电接口",
                "蓄热接口",
                "热源接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond0 == "input", cond2 == "input"]) if cond1 == "output" else True
            ),
            (
                "蓄冷接口",
                "蓄热接口",
                "制冷接口",
                "制热接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: (
                sum(
                    [
                        int(cond2 == "output"),
                        int(cond3 == "output"),
                        int(cond0 == "output"),
                        int(cond1 == "output"),
                    ]
                )
                <= 1
            ),
        }.items()
    },
    "中深层双源四工况热泵": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "电接口",
                "冷源接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond0 == "input", cond1 == "input"]) if cond2 == "output" else True
            ),
            (
                "蓄冷接口",
                "冷源接口",
                "电接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond2 == "input", cond1 == "input"]) if cond0 == "output" else True
            ),
            (
                "电接口",
                "热源接口",
                "制热接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond0 == "input", cond1 == "input"]) if cond2 == "output" else True
            ),
            (
                "电接口",
                "蓄热接口",
                "热源接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond0 == "input", cond2 == "input"]) if cond1 == "output" else True
            ),
            (
                "蓄冷接口",
                "蓄热接口",
                "制冷接口",
                "制热接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: (
                sum(
                    [
                        int(cond2 == "output"),
                        int(cond3 == "output"),
                        int(cond0 == "output"),
                        int(cond1 == "output"),
                    ]
                )
                <= 1
            ),
        }.items()
    },
    "浅层双源三工况热泵": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "电接口",
                "冷源接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond0 == "input", cond1 == "input"]) if cond2 == "output" else True
            ),
            (
                "制冰接口",
                "冷源接口",
                "电接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond2 == "input", cond1 == "input"]) if cond0 == "output" else True
            ),
            (
                "电接口",
                "热源接口",
                "制热接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond0 == "input", cond1 == "input"]) if cond2 == "output" else True
            ),
            (
                "制冰接口",
                "制冷接口",
                "制热接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                sum(
                    [
                        int(cond1 == "output"),
                        int(cond2 == "output"),
                        int(cond0 == "output"),
                    ]
                )
                <= 1
            ),
        }.items()
    },
    "中深层双源三工况热泵": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "电接口",
                "冷源接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond0 == "input", cond1 == "input"]) if cond2 == "output" else True
            ),
            (
                "制冰接口",
                "冷源接口",
                "电接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond2 == "input", cond1 == "input"]) if cond0 == "output" else True
            ),
            (
                "电接口",
                "热源接口",
                "制热接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond0 == "input", cond1 == "input"]) if cond2 == "output" else True
            ),
            (
                "制冰接口",
                "制冷接口",
                "制热接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                sum(
                    [
                        int(cond1 == "output"),
                        int(cond2 == "output"),
                        int(cond0 == "output"),
                    ]
                )
                <= 1
            ),
        }.items()
    },
    "水冷螺杆机": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "电接口",
                "冷源接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond0 == "input", cond1 == "input"]) if cond2 == "output" else True
            ),
            (
                "蓄冷接口",
                "冷源接口",
                "电接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond2 == "input", cond1 == "input"]) if cond0 == "output" else True
            ),
            ("蓄冷接口", "制冷接口"): lambda cond0, cond1, etype0, etype1: (
                sum([int(cond1 == "output"), int(cond0 == "output")]) <= 1
            ),
        }.items()
    },
    "双工况水冷螺杆机组": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "电接口",
                "冷源接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond0 == "input", cond1 == "input"]) if cond2 == "output" else True
            ),
            (
                "制冰接口",
                "冷源接口",
                "电接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond2 == "input", cond1 == "input"]) if cond0 == "output" else True
            ),
            ("制冰接口", "制冷接口"): lambda cond0, cond1, etype0, etype1: (
                sum([int(cond1 == "output"), int(cond0 == "output")]) <= 1
            ),
        }.items()
    },
    "吸收式燃气热泵": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("燃料接口", "制热接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            )
        }.items()
    },
    "空气源热泵": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口", "制冷接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            ),
            ("蓄冷接口", "电接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond1 == "input"]) if cond0 == "output" else True
            ),
            ("电接口", "制热接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            ),
            ("电接口", "蓄热接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            ),
            (
                "蓄冷接口",
                "蓄热接口",
                "制冷接口",
                "制热接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: (
                sum(
                    [
                        int(cond2 == "output"),
                        int(cond3 == "output"),
                        int(cond0 == "output"),
                        int(cond1 == "output"),
                    ]
                )
                <= 1
            ),
        }.items()
    },
    "蒸汽溴化锂": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "蒸汽接口",
                "冷源接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond0 == "input", cond1 == "input"]) if cond2 == "output" else True
            )
        }.items()
    },
    "热水溴化锂": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "冷源接口",
                "热水接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond1 == "input", cond0 == "input"]) if cond2 == "output" else True
            )
        }.items()
    },
    "电热水锅炉": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口", "制热接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            )
        }.items()
    },
    "电蒸汽锅炉": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口", "蒸汽接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            )
        }.items()
    },
    "天然气热水锅炉": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("燃料接口", "制热接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            )
        }.items()
    },
    "天然气蒸汽锅炉": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("蒸汽接口", "燃料接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond1 == "input"]) if cond0 == "output" else True
            )
        }.items()
    },
    "电解槽": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口", "设备余热接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            ),
            ("制氢接口", "电接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond1 == "input"]) if cond0 == "output" else True
            ),
        }.items()
    },
    "水蓄能": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("蓄冷接口", "蓄热接口"): lambda cond0, cond1, etype0, etype1: (
                sum([int(cond1 != "idle"), int(cond0 != "idle")]) <= 1
            )
        }.items()
    },
    "输水管道": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "输入接口",
                "电接口",
                "输出接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond2 == "input", cond1 == "input"]) if cond0 == "output" else True
            )
            and (
                all([cond0 == "input", cond1 == "input"]) if cond2 == "output" else True
            ),
            ("输入接口", "输出接口"): lambda cond0, cond1, etype0, etype1: (
                sum([int(cond0 == "input"), int(cond1 == "input")]) <= 1
            )
            and (
                all(["冷" in it for it in [etype0, etype1]])
                or all(["热" in it for it in [etype0, etype1]])
            ),
        }.items()
    },
    "蒸汽管道": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("输入接口", "输出接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond1 == "input"]) if cond0 == "output" else True
            )
            and (all([cond0 == "input"]) if cond1 == "output" else True)
            and (sum([int(cond0 == "input"), int(cond1 == "input")]) <= 1)
        }.items()
    },
    "复合输水管道": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "电接口",
                "冷输出接口",
                "冷输入接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond1 == "input", cond0 == "input"]) if cond2 == "output" else True
            )
            and (
                all([cond2 == "input", cond0 == "input"]) if cond1 == "output" else True
            ),
            (
                "电接口",
                "热输入接口",
                "热输出接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: (
                all([cond2 == "input", cond0 == "input"]) if cond1 == "output" else True
            )
            and (
                all([cond1 == "input", cond0 == "input"]) if cond2 == "output" else True
            ),
            (
                "冷输出接口",
                "热输入接口",
                "热输出接口",
                "冷输入接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: (
                sum(
                    [
                        int(cond3 == "input"),
                        int(cond1 == "input"),
                        int(cond0 == "input"),
                        int(cond2 == "input"),
                    ]
                )
                <= 1
            ),
        }.items()
    },
    "水水换热器": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("输入接口", "输出接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond1 == "input"]) if cond0 == "output" else True
            )
            and (all([cond0 == "input"]) if cond1 == "output" else True)
            and (sum([int(cond0 == "input"), int(cond1 == "input")]) <= 1)
            and (
                all(["冷" in it for it in [etype0, etype1]])
                or all(["热" in it for it in [etype0, etype1]])
            )
        }.items()
    },
    "复合水水换热器": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("冷输出接口", "冷输入接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            )
            and (all([cond1 == "input"]) if cond0 == "output" else True),
            ("热输入接口", "热输出接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond1 == "input"]) if cond0 == "output" else True
            )
            and (all([cond0 == "input"]) if cond1 == "output" else True),
            (
                "冷输出接口",
                "热输入接口",
                "热输出接口",
                "冷输入接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: (
                sum(
                    [
                        int(cond3 == "input"),
                        int(cond1 == "input"),
                        int(cond0 == "input"),
                        int(cond2 == "input"),
                    ]
                )
                <= 1
            ),
        }.items()
    },
    "气水换热器": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("输入接口", "输出接口"): lambda cond0, cond1, etype0, etype1: (
                all([cond0 == "input"]) if cond1 == "output" else True
            )
        }.items()
    },
}


def convert_topo_to_prolog_render_params_and_verification_params(topo):
    possibleEnergyTypes = set()
    possibleDeviceTypes = set()

    portNameToPortPossibleStates = {}  #
    deviceTypeToDeviceNames = {}  #
    deviceNameToPortNames = {}  #
    energyTypeToPortNames = {}  #
    adderNameToAdderPortNames = {}  #

    port_name_lookup_table = {}

    adders = topo.get_all_adders()
    adder_index_to_adder_name = {}

    port_verifiers = {}
    conjugate_port_verifiers = (
        {}
    )  # TODO: parse additional conjugate port verifiers from topo object.

    for devInfo in topo.get_all_devices():
        node_id = devInfo["id"]
        node_subtype = devInfo["subtype"]
        possibleDeviceTypes.add(node_subtype)
        devName = f"{node_subtype}_{node_id}"
        deviceNameToPortNames[devName] = []
        if node_subtype not in deviceTypeToDeviceNames.keys():
            deviceTypeToDeviceNames[node_subtype] = []
        deviceTypeToDeviceNames[node_subtype].append(devName)
        ports = devInfo["ports"]

        typeInfo = deviceTypeToTypeInfo[node_subtype]
        requiredPortFrontendNameToPortPossibleStates = typeInfo[
            "requiredPortFrontendNameToPortPossibleStates"
        ]
        requiredPortFrontendNameToEnergyTypes = typeInfo[
            "requiredPortFrontendNameToEnergyTypes"
        ]

        port_kind_to_port_name = {}

        for port_kind, port_info in ports.items():
            portPossibleStates = requiredPortFrontendNameToPortPossibleStates[port_kind]
            portPossibleEnergyTypes = requiredPortFrontendNameToEnergyTypes[port_kind]
            possibleEnergyTypes.update(portPossibleEnergyTypes)

            port_name = f"{devName}_{port_kind}"
            port_kind_to_port_name[port_kind] = port_name

            verifier = port_verifier_lookup_table.get(node_subtype, {}).get(
                port_kind, None
            )
            if verifier:
                port_verifiers[port_name] = verifier

            deviceNameToPortNames[devName].append(port_name)
            port_id = port_info["id"]
            port_name_lookup_table[port_id] = port_name
            portNameToPortPossibleStates[port_name] = portPossibleStates

            for energyType in portPossibleEnergyTypes:
                if energyType not in energyTypeToPortNames.keys():
                    energyTypeToPortNames[energyType] = []
                energyTypeToPortNames[energyType].append(port_name)

        conjugate_verifiers_constructor = (
            conjugate_port_verifier_constructor_lookup_table.get(
                node_subtype, lambda d: {}
            )
        )
        conjugate_verifiers = conjugate_verifiers_constructor(port_kind_to_port_name)
        conjugate_port_verifiers.update(conjugate_verifiers)

    for adder_index, adder_def in adders.items():
        index = str(adder_index).replace("-", "_")
        adder_name = f"adder{index}"
        adder_index_to_adder_name[adder_index] = adder_name
        port_name_list = []
        for _, port_index_list in adder_def.items():
            for port_index in port_index_list:
                port_name = port_name_lookup_table[port_index]
                port_name_list.append(port_name)
        adderNameToAdderPortNames[adder_name] = port_name_list

    render_params = dict(
        portNameToPortPossibleStates=portNameToPortPossibleStates,
        deviceTypes=list(possibleDeviceTypes),
        deviceTypeToDeviceNames=deviceTypeToDeviceNames,
        deviceNameToPortNames=deviceNameToPortNames,
        energyTypes=list(possibleEnergyTypes),
        energyTypeToPortNames=energyTypeToPortNames,
        adderNameToAdderPortNames=adderNameToAdderPortNames,
    )

    port_index_lookup_table = {v: k for k, v in port_name_lookup_table.items()}

    adder_name_to_adder_index = {v: k for k, v in adder_index_to_adder_name.items()}
    adder_index_to_port_name = {}

    for adderName, adderPortNames in adderNameToAdderPortNames.items():
        port_index_to_port_name = {
            port_index_lookup_table[portName]: portName for portName in adderPortNames
        }
        adder_index = adder_name_to_adder_index[adderName]
        adder_index_to_port_name[adder_index] = port_index_to_port_name

    verification_params = (
        adder_index_to_port_name,
        port_verifiers,
        conjugate_port_verifiers,
    )

    return render_params, verification_params


basepath = os.path.dirname(__file__)

template_path = "prolog_gen.pro.j2"

template_abs_path = os.path.join(basepath, template_path)

from jinja_utils import load_template_text

with open(template_abs_path, "r") as f:
    template_content = f.read()
    template_obj = load_template_text(template_content)


def render_prolog_code(render_params):
    prolog_code = template_obj.render(**render_params)
    logger_print("prolog code:", prolog_code)
    return prolog_code


def dynamic_verify_topo_object(topo):
    (
        render_params,
        verification_params,
    ) = convert_topo_to_prolog_render_params_and_verification_params(topo)

    (
        adder_index_to_port_name,
        port_verifiers,
        conjugate_port_verifiers,
    ) = verification_params

    prolog_script_content = render_prolog_code(render_params)

    adderNameToAdderPortNames = render_params["adderNameToAdderPortNames"]

    (
        can_proceed,
        isomorphic_topo_status,
    ) = execute_prolog_script_and_check_if_can_proceed(
        prolog_script_content,
        adder_index_to_port_name,
        port_verifiers,
        conjugate_port_verifiers,
        adderNameToAdderPortNames,
    )

    return can_proceed, isomorphic_topo_status


##############################################

from error_utils import ErrorManager
from failsafe_utils import chdir_context

##############################################

from swiplserver import PrologMQI, PrologThread
from pydantic import BaseModel
from typing import List, Dict

# from HashableDict.HashableDict import HashDict
from frozendict import frozendict
import rich
import os
import tempfile


banner = lambda title: logger_print(title.center(60, "-"))


def query_result_from_prolog(
    prolog_script_content: str, adder_index_to_port_name, adderNameToAdderPortNames
):
    banner("querying")
    topology_status_dict = {}
    with tempfile.TemporaryDirectory() as temp_dir:
        with chdir_context(temp_dir):
            prolog_file_path = "prolog_script.pro"
            prolog_file_path_abs = os.path.join(prolog_file_path)
            with open(prolog_file_path_abs, "w+") as f:
                f.write(prolog_script_content)
            with PrologMQI() as mqi:
                with mqi.create_thread() as prolog_thread:
                    topology_status_dict = query_prolog_in_context(
                        topology_status_dict,
                        prolog_file_path,
                        prolog_thread,
                        adder_index_to_port_name,
                        adderNameToAdderPortNames,
                    )
    return topology_status_dict


import progressbar


def query_prolog_in_context(
    topology_status_dict,
    prolog_file_path,
    prolog_thread,
    adder_index_to_port_name,
    adderNameToAdderPortNames,
):
    adder_name_list = []
    adder_index_mapping = {}
    for i, k in enumerate(adder_index_to_port_name.keys()):
        adder_name_list.append("adder{}".format(str(k).replace("-", "_")))
        adder_index_mapping[i] = k
    adder_names = ", ".join(adder_name_list)
    logger_print("adder_names: ", adder_names)
    # breakpoint()
    prolog_thread.query(f'["{prolog_file_path}"].')
    result = prolog_thread.query(
        f"findall(STATUS, adder_port_status_list([{adder_names}], STATUS), STATUS_LIST)"
    )
    logger_print("parsing result")
    STATUS_LIST = result[0]["STATUS_LIST"]

    for simutaneous_status in progressbar.progressbar(STATUS_LIST):
        adder_status_dict = {}
        port_status_dict = {}
        for _index, adder_simutaneous_status in enumerate(simutaneous_status):
            adder_index = adder_index_mapping[_index]
            adder_name = "adder{}".format(str(adder_index).replace("-", "_"))
            adder_energy_type, adder_port_status = adder_simutaneous_status
            adder_status_dict[adder_index] = adder_energy_type
            port_index_to_port_name = adder_index_to_port_name[adder_index]
            for _port_index, port_status in enumerate(adder_port_status):
                port_name = adderNameToAdderPortNames[adder_name][_port_index]
                port_status_dict[port_name] = port_status
        key = frozendict(adder_status_dict)
        value = frozendict(port_status_dict)
        if key not in topology_status_dict.keys():
            topology_status_dict[key] = set()
        topology_status_dict[key].add(value)
    logger_print("result parsed")
    return topology_status_dict


def verify_topology_status_dict(
    topology_status_dict,
    port_verifiers,
    conjugate_port_verifiers,
    adder_index_to_port_name,
):
    banner("unverified topo status")
    logger_print(topology_status_dict)
    banner("verifying")

    verified_topology_status_dict = {}
    for topo_status_index, (adder_status, topo_status) in enumerate(
        topology_status_dict.items()
    ):
        topo_status_frame_flatten = {}
        port_verified = {}
        conjugate_port_verified = {}

        port_name_to_energy_type = {
            v_v: adder_status[k]
            for k, v in adder_index_to_port_name.items()
            for v_k, v_v in v.items()
        }

        for topo_status_frame in topo_status:
            for topo_status_frame_index, (port_name, port_status) in enumerate(
                topo_status_frame.items()
            ):
                # breakpoint()
                if port_name not in topo_status_frame_flatten.keys():
                    topo_status_frame_flatten[port_name] = set()
                _conjugate_verified = True
                with ErrorManager(suppress_error=True) as em:
                    for (
                        conjugate_ports,
                        conjugate_verifier,
                    ) in conjugate_port_verifiers.items():
                        conds = [
                            topo_status_frame[port_name]
                            for port_name in conjugate_ports
                        ]
                        energytypes = [
                            port_name_to_energy_type[port_name]
                            for port_name in conjugate_ports
                        ]
                        conjugate_verified = conjugate_verifier(*conds, *energytypes)
                        # conjugate_verified = conjugate_verifier(*conds)
                        if not conjugate_verified:
                            em.append(
                                f"conjugate verification failed for conjugate ports '{conjugate_ports}' at topo status frame #{topo_status_frame_index}"
                            )
                            if _conjugate_verified:
                                _conjugate_verified = False
                if _conjugate_verified:
                    topo_status_frame_flatten[port_name].add(port_status)
                else:
                    logger_print(
                        f"skipping topo status frame #{topo_status_frame_index} due to failed conjugate ports verification"
                    )
        for port_name, verifier in port_verifiers.items():
            conds = topo_status_frame_flatten[port_name]
            verified = verifier(conds)
            port_verified[port_name] = verified
            if not verified:
                logger_print(f"verifier failed for port '{port_name}'")

        all_ports_verified = all(port_verified.values())
        all_conjugate_ports_verified = all(conjugate_port_verified.values())
        topo_verified = all_ports_verified and all_conjugate_ports_verified

        if not all_ports_verified:
            logger_print("not all port vaildations have passed")

        if not all_conjugate_ports_verified:
            logger_print("not all conjugate port vaildations have passed")

        if not topo_verified:
            logger_print(
                f"topo verification failed for topo status #{topo_status_index}"
            )
        else:
            if len(topo_status) > 0:
                verified_topology_status_dict[adder_status] = topo_status
            else:
                logger_print("skipping due to empty topo status")
        banner(f"processed topo status #{topo_status_index}")

    banner("verified topo status")
    logger_print(verified_topology_status_dict)
    return verified_topology_status_dict


def isomorphicTopologyStatusCombinator(topology_status_dict: dict):
    topo_status_to_adder_status_dict: Dict[frozenset, set] = {}
    for adder_index_to_energy_type, topo_status in topology_status_dict.items():
        topo_status_frozen = frozenset(topo_status)
        if topo_status_frozen not in topo_status_to_adder_status_dict.keys():
            topo_status_to_adder_status_dict[topo_status_frozen] = set()
        topo_status_to_adder_status_dict[topo_status_frozen].add(
            adder_index_to_energy_type
        )
    return topo_status_to_adder_status_dict


def check_if_can_proceed(verified_topology_status_dict):
    isomorphic_topo_status = None
    possible_adder_energy_type_set_counts = len(verified_topology_status_dict)
    logger_print(
        "possible adder energy type set counts:", possible_adder_energy_type_set_counts
    )

    isomorphic_topo_status = isomorphicTopologyStatusCombinator(
        verified_topology_status_dict
    )

    banner("isomorphic topo status (converted)")
    for k, v in isomorphic_topo_status.items():
        logger_print("key:", *[f"\t{str(e_k)}" for e_k in k], "value:", f"\t{v}")
    isomorphic_topo_status_counts = len(isomorphic_topo_status.keys())
    logger_print("isomorphic topo status counts:", isomorphic_topo_status_counts)

    can_proceed = False
    if isomorphic_topo_status_counts == 0:
        logger_print("no adder energy type set")
    elif isomorphic_topo_status_counts > 1:
        logger_print("multiple adder energy type sets found")
    else:
        can_proceed = True
    if not can_proceed:
        logger_print("cannot proceed")
    else:
        logger_print("clear to proceed")
    return can_proceed, isomorphic_topo_status


def execute_prolog_script_and_check_if_can_proceed(
    prolog_script_content,
    adder_index_to_port_name,
    port_verifiers,
    conjugate_port_verifiers,
    adderNameToAdderPortNames,
):
    topology_status_dict = query_result_from_prolog(
        prolog_script_content, adder_index_to_port_name, adderNameToAdderPortNames
    )
    verified_topology_status_dict = verify_topology_status_dict(
        topology_status_dict,
        port_verifiers,
        conjugate_port_verifiers,
        adder_index_to_port_name,
    )
    can_proceed, isomorphic_topo_status = check_if_can_proceed(
        verified_topology_status_dict
    )
    return can_proceed, isomorphic_topo_status
