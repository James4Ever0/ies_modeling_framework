from log_utils import logger_print
from type_def import *


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
    "市政自来水",
    "天然气",
    "电网",
    "氢气",
    "冷负荷",
    "热负荷",
    "蒸汽负荷",
    "氢气负荷",
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
    "导热油",
    "氢气",
    "柴油",
    "乙",
    "水",
    "冷乙二醇",
    "天然气",
    "自来水",
    "冰乙二醇",
    "冷水",
    "醇",
    "热乙二醇",
    "电",
    "热水",
    "蒸汽",
    "烟气",
    "二",
]


def ensureUniquenessInList(lst: list[str]):
    assert len(set(lst)) == len(lst)


class 动态拓扑校验节点:
    def __init__(
        self,
        deviceType: str,
        deviceNameFromFrontend: str,
        deviceIndex: int,
        portIndexToPortFrontendName: dict,
        requiredPortFrontendNameToPortPossibleStates: dict,
        requiredPortFrontendNameToEnergyTypes: dict,
        deviceCounter: int = 0,
    ):
        requiredPortFrontendNames = list(
            requiredPortFrontendNameToPortPossibleStates.keys()
        )
        ensureUniquenessInList(requiredPortFrontendNames)
        deviceCounter += 1

        self.deviceName = f"设备{deviceCounter}_{deviceType}"
        self.deviceNameFromFrontend = deviceNameFromFrontend
        self.deviceCounter = deviceCounter
        self.deviceIndex = deviceIndex

        portFrontendNames = list(portIndexToPortFrontendName.values())
        ensureUniquenessInList(portFrontendNames)
        assert set(portFrontendNames) == set(requiredPortFrontendNames)

        self.deviceTypeToDeviceName = {deviceType: self.deviceName}
        self.portFrontendNameToPortName = {
            portFrontendName: f"{self.deviceName}_{portFrontendName}"
            for portFrontendName in portFrontendNames
        }
        self.deviceNameToPortNames = {
            self.deviceName: list(self.portFrontendNameToPortName.values())
        }
        self.portIndexToPortName = {
            portIndex: self.portFrontendNameToPortName[portFrontendName]
            for portIndex, portFrontendName in portIndexToPortFrontendName.items()
        }
        self.portNameToPortPossibleStates = {
            self.portFrontendNameToPortName[
                requiredPortFrontendName
            ]: portPossibleStates
            for requiredPortFrontendName, portPossibleStates in requiredPortFrontendNameToPortPossibleStates.items()
        }

        self.energyTypeToPortNames = {}
        for (
            requiredPortFrontendName,
            energyTypes,
        ) in requiredPortFrontendNameToEnergyTypes.items():
            for energyType in energyTypes:
                if energyType not in self.energyTypeToPortNames.keys():
                    self.energyTypeToPortNames[energyType] = []
                self.energyTypeToPortNames[energyType].append(
                    self.portFrontendNameToPortName[requiredPortFrontendName]
                )


class 柴油_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "柴油"
        requiredPortFrontendNameToPortPossibleStates = {"燃料接口": ["idle", "output"]}
        requiredPortFrontendNameToEnergyTypes = {"燃料接口": ["柴油"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 电负荷_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "电负荷"
        requiredPortFrontendNameToPortPossibleStates = {"电接口": ["idle", "input"]}
        requiredPortFrontendNameToEnergyTypes = {"电接口": ["电"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 光伏发电_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "光伏发电"
        requiredPortFrontendNameToPortPossibleStates = {"电接口": ["idle", "output"]}
        requiredPortFrontendNameToEnergyTypes = {"电接口": ["电"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 风力发电_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "风力发电"
        requiredPortFrontendNameToPortPossibleStates = {"电接口": ["idle", "output"]}
        requiredPortFrontendNameToEnergyTypes = {"电接口": ["电"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 柴油发电_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "柴油发电"
        requiredPortFrontendNameToPortPossibleStates = {
            "燃料接口": ["idle", "input"],
            "电接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"燃料接口": ["柴油"], "电接口": ["电"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 锂电池_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "锂电池"
        requiredPortFrontendNameToPortPossibleStates = {
            "电接口": ["idle", "input", "output"]
        }
        requiredPortFrontendNameToEnergyTypes = {"电接口": ["电"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 变压器_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "变压器"
        requiredPortFrontendNameToPortPossibleStates = {
            "电输入": ["idle", "input", "output"],
            "电输出": ["idle", "input", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"电输入": ["电"], "电输出": ["电"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 双向变压器_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "双向变压器"
        requiredPortFrontendNameToPortPossibleStates = {
            "电输入": ["idle", "input", "output"],
            "电输出": ["idle", "input", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"电输入": ["电"], "电输出": ["电"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 变流器_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "变流器"
        requiredPortFrontendNameToPortPossibleStates = {
            "电输入": ["idle", "input"],
            "电输出": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"电输入": ["电"], "电输出": ["电"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 双向变流器_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "双向变流器"
        requiredPortFrontendNameToPortPossibleStates = {
            "储能端": ["idle", "input", "output"],
            "线路端": ["idle", "input", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"储能端": ["电"], "线路端": ["电"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 市政自来水_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "市政自来水"
        requiredPortFrontendNameToPortPossibleStates = {"水接口": ["idle", "output"]}
        requiredPortFrontendNameToEnergyTypes = {"水接口": ["自来水"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 天然气_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "天然气"
        requiredPortFrontendNameToPortPossibleStates = {"燃料接口": ["idle", "output"]}
        requiredPortFrontendNameToEnergyTypes = {"燃料接口": ["天然气"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 电网_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "电网"
        requiredPortFrontendNameToPortPossibleStates = {
            "电接口": ["idle", "input", "output"]
        }
        requiredPortFrontendNameToEnergyTypes = {"电接口": ["电"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 氢气_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "氢气"
        requiredPortFrontendNameToPortPossibleStates = {"氢气接口": ["idle", "output"]}
        requiredPortFrontendNameToEnergyTypes = {"氢气接口": ["氢气"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 冷负荷_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "冷负荷"
        requiredPortFrontendNameToPortPossibleStates = {"冷源接口": ["idle", "input"]}
        requiredPortFrontendNameToEnergyTypes = {"冷源接口": ["冷水"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 热负荷_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "热负荷"
        requiredPortFrontendNameToPortPossibleStates = {"热源接口": ["idle", "input"]}
        requiredPortFrontendNameToEnergyTypes = {"热源接口": ["热水"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 蒸汽负荷_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "蒸汽负荷"
        requiredPortFrontendNameToPortPossibleStates = {"蒸汽接口": ["idle", "input"]}
        requiredPortFrontendNameToEnergyTypes = {"蒸汽接口": ["蒸汽"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 氢气负荷_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "氢气负荷"
        requiredPortFrontendNameToPortPossibleStates = {"氢气接口": ["idle", "input"]}
        requiredPortFrontendNameToEnergyTypes = {"氢气接口": ["氢气"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 燃气发电机_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "燃气发电机"
        requiredPortFrontendNameToPortPossibleStates = {
            "燃料接口": ["idle", "input"],
            "电接口": ["idle", "output"],
            "高温烟气余热接口": ["idle", "output"],
            "缸套水余热接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "燃料接口": ["天然气"],
            "电接口": ["电"],
            "高温烟气余热接口": ["烟气"],
            "缸套水余热接口": ["热水"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 蒸汽轮机_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "蒸汽轮机"
        requiredPortFrontendNameToPortPossibleStates = {
            "蒸汽接口": ["idle", "input"],
            "电接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"蒸汽接口": ["蒸汽"], "电接口": ["电"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 氢燃料电池_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "氢燃料电池"
        requiredPortFrontendNameToPortPossibleStates = {
            "氢气接口": ["idle", "input"],
            "电接口": ["idle", "output"],
            "设备余热接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "氢气接口": ["氢气"],
            "电接口": ["电"],
            "设备余热接口": ["热水"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 平板太阳能_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "平板太阳能"
        requiredPortFrontendNameToPortPossibleStates = {"热接口": ["idle", "output"]}
        requiredPortFrontendNameToEnergyTypes = {"热接口": ["热水"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 槽式太阳能_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "槽式太阳能"
        requiredPortFrontendNameToPortPossibleStates = {"热接口": ["idle", "output"]}
        requiredPortFrontendNameToEnergyTypes = {"热接口": ["导热油"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 余热热水锅炉_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "余热热水锅炉"
        requiredPortFrontendNameToPortPossibleStates = {
            "烟气接口": ["idle", "input"],
            "制热接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"烟气接口": ["烟气"], "制热接口": ["热水"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 余热蒸汽锅炉_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "余热蒸汽锅炉"
        requiredPortFrontendNameToPortPossibleStates = {
            "烟气接口": ["idle", "input"],
            "蒸汽接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"烟气接口": ["烟气"], "蒸汽接口": ["蒸汽"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 浅层地热井_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "浅层地热井"
        requiredPortFrontendNameToPortPossibleStates = {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "output"],
            "热源接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 中深层地热井_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "中深层地热井"
        requiredPortFrontendNameToPortPossibleStates = {
            "电接口": ["idle", "input"],
            "热源接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"电接口": ["电"], "热源接口": ["热水"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 地表水源_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "地表水源"
        requiredPortFrontendNameToPortPossibleStates = {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "output"],
            "热源接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 水冷冷却塔_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "水冷冷却塔"
        requiredPortFrontendNameToPortPossibleStates = {
            "电接口": ["idle", "input"],
            "水接口": ["idle", "input"],
            "冷源接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "电接口": ["电"],
            "水接口": ["自来水"],
            "冷源接口": ["冷水"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 余热热源_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "余热热源"
        requiredPortFrontendNameToPortPossibleStates = {"热源接口": ["idle", "output"]}
        requiredPortFrontendNameToEnergyTypes = {"热源接口": ["热水"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 浅层双源四工况热泵_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "浅层双源四工况热泵"
        requiredPortFrontendNameToPortPossibleStates = {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "热源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "蓄冷接口": ["idle", "output"],
            "制热接口": ["idle", "output"],
            "蓄热接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
            "制冷接口": ["冷水"],
            "蓄冷接口": ["冷水"],
            "制热接口": ["热水"],
            "蓄热接口": ["热水"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 中深层双源四工况热泵_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "中深层双源四工况热泵"
        requiredPortFrontendNameToPortPossibleStates = {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "热源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "蓄冷接口": ["idle", "output"],
            "制热接口": ["idle", "output"],
            "蓄热接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
            "制冷接口": ["冷水"],
            "蓄冷接口": ["冷水"],
            "制热接口": ["热水"],
            "蓄热接口": ["热水"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 浅层双源三工况热泵_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "浅层双源三工况热泵"
        requiredPortFrontendNameToPortPossibleStates = {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "热源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "制冰接口": ["idle", "output"],
            "制热接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
            "制冷接口": ["冷乙二醇"],
            "制冰接口": ["冰乙二醇"],
            "制热接口": ["热乙二醇"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 中深层双源三工况热泵_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "中深层双源三工况热泵"
        requiredPortFrontendNameToPortPossibleStates = {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "热源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "制冰接口": ["idle", "output"],
            "制热接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
            "制冷接口": ["冷乙二醇"],
            "制冰接口": ["冰乙二醇"],
            "制热接口": ["热乙二醇"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 水冷螺杆机_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "水冷螺杆机"
        requiredPortFrontendNameToPortPossibleStates = {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "蓄冷接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "制冷接口": ["冷水"],
            "蓄冷接口": ["冷水"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 双工况水冷螺杆机组_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "双工况水冷螺杆机组"
        requiredPortFrontendNameToPortPossibleStates = {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "制冰接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "制冷接口": ["冷乙二醇"],
            "制冰接口": ["冰乙二醇"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 吸收式燃气热泵_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "吸收式燃气热泵"
        requiredPortFrontendNameToPortPossibleStates = {
            "燃料接口": ["idle", "input"],
            "制热接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"燃料接口": ["天然气"], "制热接口": ["热水"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 空气源热泵_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "空气源热泵"
        requiredPortFrontendNameToPortPossibleStates = {
            "电接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "蓄冷接口": ["idle", "output"],
            "制热接口": ["idle", "output"],
            "蓄热接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "电接口": ["电"],
            "制冷接口": ["冷水"],
            "蓄冷接口": ["冷水"],
            "制热接口": ["热水"],
            "蓄热接口": ["热水"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 蒸汽溴化锂_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "蒸汽溴化锂"
        requiredPortFrontendNameToPortPossibleStates = {
            "蒸汽接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "蒸汽接口": ["蒸汽"],
            "冷源接口": ["冷水"],
            "制冷接口": ["冷水"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 热水溴化锂_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "热水溴化锂"
        requiredPortFrontendNameToPortPossibleStates = {
            "热水接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "热水接口": ["热水"],
            "冷源接口": ["冷水"],
            "制冷接口": ["冷水"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 电热水锅炉_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "电热水锅炉"
        requiredPortFrontendNameToPortPossibleStates = {
            "电接口": ["idle", "input"],
            "制热接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"电接口": ["电"], "制热接口": ["热水"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 电蒸汽锅炉_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "电蒸汽锅炉"
        requiredPortFrontendNameToPortPossibleStates = {
            "电接口": ["idle", "input"],
            "蒸汽接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"电接口": ["电"], "蒸汽接口": ["蒸汽"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 天然气热水锅炉_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "天然气热水锅炉"
        requiredPortFrontendNameToPortPossibleStates = {
            "燃料接口": ["idle", "input"],
            "制热接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"燃料接口": ["天然气"], "制热接口": ["热水"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 天然气蒸汽锅炉_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "天然气蒸汽锅炉"
        requiredPortFrontendNameToPortPossibleStates = {
            "燃料接口": ["idle", "input"],
            "蒸汽接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"燃料接口": ["天然气"], "蒸汽接口": ["蒸汽"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 水蓄能_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "水蓄能"
        requiredPortFrontendNameToPortPossibleStates = {
            "蓄热接口": ["idle", "input", "output"],
            "蓄冷接口": ["idle", "input", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"蓄热接口": ["热水"], "蓄冷接口": ["冷水"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 蓄冰槽_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "蓄冰槽"
        requiredPortFrontendNameToPortPossibleStates = {
            "蓄冰接口": ["idle", "input", "output"]
        }
        requiredPortFrontendNameToEnergyTypes = {"蓄冰接口": ["冰乙二醇"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 储氢罐_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "储氢罐"
        requiredPortFrontendNameToPortPossibleStates = {
            "储氢接口": ["idle", "input", "output"]
        }
        requiredPortFrontendNameToEnergyTypes = {"储氢接口": ["氢气"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 输水管道_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "输水管道"
        requiredPortFrontendNameToPortPossibleStates = {
            "输入接口": ["idle", "input", "output"],
            "输出接口": ["idle", "input", "output"],
            "电接口": ["idle", "input"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "输入接口": ["冷水", "热水"],
            "输出接口": ["冷水", "热水"],
            "电接口": ["电"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 蒸汽管道_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "蒸汽管道"
        requiredPortFrontendNameToPortPossibleStates = {
            "输入接口": ["idle", "input", "output"],
            "输出接口": ["idle", "input", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"输入接口": ["蒸汽"], "输出接口": ["蒸汽"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 复合输水管道_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "复合输水管道"
        requiredPortFrontendNameToPortPossibleStates = {
            "冷输入接口": ["idle", "input", "output"],
            "热输入接口": ["idle", "input", "output"],
            "冷输出接口": ["idle", "input", "output"],
            "热输出接口": ["idle", "input", "output"],
            "电接口": ["idle", "input"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "冷输入接口": ["冷水"],
            "热输入接口": ["热水"],
            "冷输出接口": ["冷水"],
            "热输出接口": ["热水"],
            "电接口": ["电"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 水水换热器_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "水水换热器"
        requiredPortFrontendNameToPortPossibleStates = {
            "输入接口": ["idle", "input", "output"],
            "输出接口": ["idle", "input", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "输入接口": ["乙", "醇", "二", "水", "导热油"],
            "输出接口": ["乙", "醇", "二", "水", "导热油"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 复合水水换热器_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "复合水水换热器"
        requiredPortFrontendNameToPortPossibleStates = {
            "冷输入接口": ["idle", "input", "output"],
            "热输入接口": ["idle", "input", "output"],
            "冷输出接口": ["idle", "input", "output"],
            "热输出接口": ["idle", "input", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {
            "冷输入接口": ["冷乙二醇", "冰乙二醇", "冷水"],
            "热输入接口": ["热乙二醇", "热水", "导热油"],
            "冷输出接口": ["冷乙二醇", "冰乙二醇", "冷水"],
            "热输出接口": ["热乙二醇", "热水", "导热油"],
        }
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )


class 气水换热器_动态拓扑校验节点(动态拓扑校验节点):
    def __init__(
        self,
        deviceNameFromFrontend: str,
        portIndexToPortFrontendName: dict,
        deviceIndex: int,
        deviceCounter: int,
    ):
        deviceType = "气水换热器"
        requiredPortFrontendNameToPortPossibleStates = {
            "输入接口": ["idle", "input"],
            "输出接口": ["idle", "output"],
        }
        requiredPortFrontendNameToEnergyTypes = {"输入接口": ["蒸汽"], "输出接口": ["热水"]}
        super().__init__(
            deviceType,
            deviceNameFromFrontend,
            deviceIndex,
            portIndexToPortFrontendName,
            requiredPortFrontendNameToPortPossibleStates,
            requiredPortFrontendNameToEnergyTypes,
            deviceCounter,
        )
