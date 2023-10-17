from log_utils import logger_print
from log_utils import logger_traceback
from type_utils import dynamic_verify_topo_object

import networkx
from networkx.readwrite import json_graph
from config import ies_env
from pydantic import BaseModel

from typing import List, Dict, Literal

# when to check topology:
# 	1.  Building topology <- which the frontend does the job
# 	2.  Importing topology <- where algorithm kicks in

# so here we only check topo when importing. we don't check validity during topo construction.


# 母线最多99个对接的接口


def getMainAndSubType(data):
    logger_print("DATA:", data)
    return data["type"], data["subtype"]


def getMainType(data):
    logger_print("DATA:", data)
    return data["type"]


# better use some template.
# 设备、母线、连接线、合并线

设备类型 = [
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


设备接口名称集合 = {
    "柴油": {"燃料接口"},
    "电负荷": {"电接口"},
    "光伏发电": {"电接口"},
    "风力发电": {"电接口"},
    "柴油发电": {"电接口", "燃料接口"},
    "锂电池": {"电接口"},
    "变压器": {"电输入", "电输出"},
    "双向变压器": {"电输入", "电输出"},
    "变流器": {"电输入", "电输出"},
    "双向变流器": {"储能端", "线路端"},
    "传输线": {"电输入", "电输出"},
    "市政自来水": {"水接口"},
    "天然气": {"燃料接口"},
    "电网": {"电接口"},
    "氢气": {"氢气接口"},
    "冷负荷": {"冷源接口"},
    "热负荷": {"热源接口"},
    "蒸汽负荷": {"蒸汽接口"},
    "氢负荷": {"氢气接口"},
    "燃气发电机": {"高温烟气余热接口", "电接口", "燃料接口", "缸套水余热接口"},
    "蒸汽轮机": {"蒸汽接口", "电接口"},
    "氢燃料电池": {"设备余热接口", "电接口", "氢气接口"},
    "平板太阳能": {"热接口"},
    "槽式太阳能": {"热接口"},
    "余热热水锅炉": {"烟气接口", "制热接口"},
    "余热蒸汽锅炉": {"蒸汽接口", "烟气接口"},
    "浅层地热井": {"电接口", "冷源接口", "热源接口"},
    "中深层地热井": {"电接口", "热源接口"},
    "地表水源": {"电接口", "冷源接口", "热源接口"},
    "水冷冷却塔": {"电接口", "冷源接口", "水接口"},
    "余热热源": {"热源接口"},
    "浅层双源四工况热泵": {"冷源接口", "制冷接口", "制热接口", "蓄冷接口", "热源接口", "电接口", "蓄热接口"},
    "中深层双源四工况热泵": {"冷源接口", "制冷接口", "制热接口", "蓄冷接口", "热源接口", "电接口", "蓄热接口"},
    "浅层双源三工况热泵": {"冷源接口", "制冰接口", "制冷接口", "制热接口", "热源接口", "电接口"},
    "中深层双源三工况热泵": {"冷源接口", "制冰接口", "制冷接口", "制热接口", "热源接口", "电接口"},
    "水冷螺杆机": {"制冷接口", "电接口", "冷源接口", "蓄冷接口"},
    "双工况水冷螺杆机组": {"制冷接口", "电接口", "冷源接口", "制冰接口"},
    "吸收式燃气热泵": {"制热接口", "燃料接口"},
    "空气源热泵": {"制冷接口", "制热接口", "蓄冷接口", "电接口", "蓄热接口"},
    "蒸汽溴化锂": {"蒸汽接口", "冷源接口", "制冷接口"},
    "热水溴化锂": {"制冷接口", "热水接口", "冷源接口"},
    "电热水锅炉": {"电接口", "制热接口"},
    "电蒸汽锅炉": {"蒸汽接口", "电接口"},
    "天然气热水锅炉": {"制热接口", "燃料接口"},
    "天然气蒸汽锅炉": {"蒸汽接口", "燃料接口"},
    "电解槽": {"设备余热接口", "制氢接口", "电接口"},
    "水蓄能": {"蓄冷接口", "蓄热接口"},
    "蓄冰槽": {"蓄冰接口"},
    "储氢罐": {"储氢接口"},
    "输水管道": {"输入接口", "电接口", "输出接口"},
    "蒸汽管道": {"输入接口", "输出接口"},
    "复合输水管道": {"冷输出接口", "热输入接口", "冷输入接口", "电接口", "热输出接口"},
    "水水换热器": {"输入接口", "输出接口"},
    "复合水水换热器": {"冷输出接口", "热输入接口", "冷输入接口", "热输出接口"},
    "气水换热器": {"输入接口", "输出接口"},
}

directionLookupTable = {
    "柴油": {"燃料接口": "输出"},
    "电负荷": {"电接口": "输入"},
    "光伏发电": {"电接口": "输出"},
    "风力发电": {"电接口": "输出"},
    "柴油发电": {"燃料接口": "输入", "电接口": "输出"},
    "锂电池": {"电接口": "输入输出"},
    "变压器": {"电输入": "输入", "电输出": "输出"},
    "双向变压器": {"电输入": "输入输出", "电输出": "输入输出"},
    "变流器": {"电输入": "输入", "电输出": "输出"},
    "双向变流器": {"储能端": "输入输出", "线路端": "输入输出"},
    "传输线": {"电输入": "输入输出", "电输出": "输入输出"},
    "市政自来水": {"水接口": "输出"},
    "天然气": {"燃料接口": "输出"},
    "电网": {"电接口": "输入输出"},
    "氢气": {"氢气接口": "输出"},
    "冷负荷": {"冷源接口": "输入"},
    "热负荷": {"热源接口": "输入"},
    "蒸汽负荷": {"蒸汽接口": "输入"},
    "氢负荷": {"氢气接口": "输入"},
    "燃气发电机": {"燃料接口": "输入", "电接口": "输出", "高温烟气余热接口": "输出", "缸套水余热接口": "输出"},
    "蒸汽轮机": {"蒸汽接口": "输入", "电接口": "输出"},
    "氢燃料电池": {"氢气接口": "输入", "电接口": "输出", "设备余热接口": "输出"},
    "平板太阳能": {"热接口": "输出"},
    "槽式太阳能": {"热接口": "输出"},
    "余热热水锅炉": {"烟气接口": "输入", "制热接口": "输出"},
    "余热蒸汽锅炉": {"烟气接口": "输入", "蒸汽接口": "输出"},
    "浅层地热井": {"电接口": "输入", "冷源接口": "输出", "热源接口": "输出"},
    "中深层地热井": {"电接口": "输入", "热源接口": "输出"},
    "地表水源": {"电接口": "输入", "冷源接口": "输出", "热源接口": "输出"},
    "水冷冷却塔": {"电接口": "输入", "水接口": "输入", "冷源接口": "输出"},
    "余热热源": {"热源接口": "输出"},
    "浅层双源四工况热泵": {
        "电接口": "输入",
        "冷源接口": "输入",
        "热源接口": "输入",
        "制冷接口": "输出",
        "蓄冷接口": "输出",
        "制热接口": "输出",
        "蓄热接口": "输出",
    },
    "中深层双源四工况热泵": {
        "电接口": "输入",
        "冷源接口": "输入",
        "热源接口": "输入",
        "制冷接口": "输出",
        "蓄冷接口": "输出",
        "制热接口": "输出",
        "蓄热接口": "输出",
    },
    "浅层双源三工况热泵": {
        "电接口": "输入",
        "冷源接口": "输入",
        "热源接口": "输入",
        "制冷接口": "输出",
        "制冰接口": "输出",
        "制热接口": "输出",
    },
    "中深层双源三工况热泵": {
        "电接口": "输入",
        "冷源接口": "输入",
        "热源接口": "输入",
        "制冷接口": "输出",
        "制冰接口": "输出",
        "制热接口": "输出",
    },
    "水冷螺杆机": {"电接口": "输入", "冷源接口": "输入", "制冷接口": "输出", "蓄冷接口": "输出"},
    "双工况水冷螺杆机组": {"电接口": "输入", "冷源接口": "输入", "制冷接口": "输出", "制冰接口": "输出"},
    "吸收式燃气热泵": {"燃料接口": "输入", "制热接口": "输出"},
    "空气源热泵": {"电接口": "输入", "制冷接口": "输出", "蓄冷接口": "输出", "制热接口": "输出", "蓄热接口": "输出"},
    "蒸汽溴化锂": {"蒸汽接口": "输入", "冷源接口": "输入", "制冷接口": "输出"},
    "热水溴化锂": {"热水接口": "输入", "冷源接口": "输入", "制冷接口": "输出"},
    "电热水锅炉": {"电接口": "输入", "制热接口": "输出"},
    "电蒸汽锅炉": {"电接口": "输入", "蒸汽接口": "输出"},
    "天然气热水锅炉": {"燃料接口": "输入", "制热接口": "输出"},
    "天然气蒸汽锅炉": {"燃料接口": "输入", "蒸汽接口": "输出"},
    "电解槽": {"电接口": "输入", "制氢接口": "输出", "设备余热接口": "输出"},
    "水蓄能": {"蓄热接口": "输入输出", "蓄冷接口": "输入输出"},
    "蓄冰槽": {"蓄冰接口": "输入输出"},
    "储氢罐": {"储氢接口": "输入输出"},
    "输水管道": {"输入接口": "输入输出", "输出接口": "输入输出", "电接口": "输入"},
    "蒸汽管道": {"输入接口": "输入输出", "输出接口": "输入输出"},
    "复合输水管道": {
        "冷输入接口": "输入输出",
        "热输入接口": "输入输出",
        "冷输出接口": "输入输出",
        "热输出接口": "输入输出",
        "电接口": "输入",
    },
    "水水换热器": {"输入接口": "输入输出", "输出接口": "输入输出"},
    "复合水水换热器": {"冷输入接口": "输入输出", "热输入接口": "输入输出", "冷输出接口": "输入输出", "热输出接口": "输入输出"},
    "气水换热器": {"输入接口": "输入", "输出接口": "输出"},
}


class NodeStruct(BaseModel):
    id: int
    type: str
    subtype: str
    direction: Literal[None, "输入输出", "输入", "输出"] = None


def constructAdder() -> Dict[str, List[int]]:
    return {"input": [], "output": [], "IO": []}


def parse_node_struct_and_update_adder(node: NodeStruct, adder: Dict[str, List[int]]):
    # this is the main reason you cannot make subtype passed from frontend.
    # TODO: resolve direction from rules

    direction = node.direction
    if direction == "输入输出":
        adder["IO"].append(node.id)
    elif direction == "输入":
        adder["output"].append(node.id)
    elif direction == "输出":
        adder["input"].append(node.id)
    elif direction is None:
        raise Exception("direction is not specified in node struct:", node)
    else:
        raise Exception("Unknown direction for node:", node)


def get_node_struct_from_node_id_and_node_data(node_id, node_data):
    _type = node_data["type"]
    subtype = node_data["subtype"]
    direction = node_data.get("direction", None)
    node_struct = NodeStruct(
        id=node_id, type=_type, subtype=subtype, direction=direction
    )
    return node_struct


def lookup_port_direction(device_name, node_name):
    direction = directionLookupTable[device_name][node_name]
    return direction


class 拓扑图:
    def __init__(self, **kwargs):
        self.node_count = 0
        self.G = networkx.Graph(**kwargs)
        self.合并母线ID集合列表 = []
        self.is_valid = ies_env.FAILSAFE

    def get_direction_from_node_id(self, node_id):
        direction = None
        node_data = self.G.nodes[node_id]
        if node_data["type"] == "锚点":
            node_name = node_data["port_name"]
            for neighbor_id in self.G.neighbors(node_id):
                neighbor_data = self.G.nodes[neighbor_id]
                if neighbor_data["type"] == "设备":
                    device_name = neighbor_data["subtype"]
                    direction = lookup_port_direction(device_name, node_name)
        return direction

    def get_node_struct_from_node_id(self, node_id):
        node_data = self.G.nodes[node_id]

        direction = self.get_direction_from_node_id(node_id)

        if direction is not None:
            node_data["direction"] = direction

        node_struct = get_node_struct_from_node_id_and_node_data(node_id, node_data)
        return node_struct

    def get_left_and_right_node_struct_from_connector_node_index(self, node_index):
        left_id, right_id = self.G.neighbors(node_index)
        left_node_struct, right_node_struct = self.get_node_struct_from_node_id(
            left_id
        ), self.get_node_struct_from_node_id(right_id)
        return left_node_struct, right_node_struct

    def get_all_devices(self) -> list:
        devs = []
        for node_index, node_data in self.G.nodes.items():
            node_type = node_data["type"]
            node_data["id"] = node_index

            if node_type == "设备":
                devs.append(node_data)
        return devs

    def get_all_adders(self) -> dict:  # don't care about types here.
        # use adder ids. adder starts with -1
        adders = {min(s): constructAdder() for s in self.合并母线ID集合列表}  # 用到：合并母线ID集合列表
        adder_id = -1
        母线ID映射表 = {e: min(s) for s in self.合并母线ID集合列表 for e in s}
        # format: {"input":input_ids, "output": output_ids, "IO": IO_ids}
        for node_index, node_data in self.G.nodes.items():
            node = get_node_struct_from_node_id_and_node_data(node_index, node_data)
            if node.type == "连接线":
                #  检查连接线两端
                (
                    left,
                    right,
                ) = self.get_left_and_right_node_struct_from_connector_node_index(
                    node_index
                )

                if left.type == "母线" and right.type == "锚点":  # swap
                    right, left = left, right

                if left.type == "锚点" and right.type == "锚点":
                    adder = constructAdder()

                    parse_node_struct_and_update_adder(left, adder)
                    parse_node_struct_and_update_adder(right, adder)

                    adders[adder_id] = adder
                    adder_id -= 1

                elif left.type == "锚点" and right.type == "母线":
                    madder_id = 母线ID映射表[right.id]

                    adder = adders[madder_id]
                    parse_node_struct_and_update_adder(left, adder)

                else:
                    raise Exception(
                        f"不合理的连接线两端：{left.type}[{left.subtype}]-{right.type}[{right.subtype}]"
                    )

        return adders

    def get_graph_data(self) -> dict:  # primary data. shall be found somewhere.
        graph_data = self.G.graph
        return graph_data

    def add_node(self, **kwargs):
        self.G.add_node(self.node_count, **kwargs)
        node_id = self.node_count
        self.node_count += 1
        return node_id

    def get_neighbors_by_node_id(self, node_id):
        neighbors = list(self.G.neighbors(node_id))
        logger_print(f"NEIGHBORS FOR NODE #{node_id}:", neighbors)
        for n in neighbors:
            logger_print(self.G.nodes[n])
        return neighbors

    # monotonically adding a node.
    def _check_consistency(self):  # return nothing.
        #  use subgraph
        # 提取所有母线ID
        母线ID列表 = []
        合并线ID列表 = []

        for node_id, node_data in self.G.nodes.items():
            node = get_node_struct_from_node_id_and_node_data(node_id, node_data)

            logger_print("NODE TYPE:", node.type)
            logger_print("NODE SUBTYPE:", node.subtype)

            neighbors = self.get_neighbors_by_node_id(node.id)
            neighbors_count = len(neighbors)

            logger_print("=" * 40)

            if node.type == "母线":
                母线ID列表.append(node.id)
                assert (
                    neighbors_count <= 99
                ), f"节点 #{node.id} 母线连接数超过99: {neighbors_count}"

                for n in neighbors:
                    ne_data = self.G.nodes[n]
                    ne_type, ne_subtype = getMainAndSubType(ne_data)

                    if ne_type in ["合并线", "连接线"]:
                        pass
                    else:
                        raise Exception(f"节点 #{n} {node.subtype}连接非法类型节点：", ne_type)
            elif node.type == "设备":
                try:
                    assert (
                        node.subtype in 设备类型
                    ), f"节点 #{node.id} 不存在的设备类型: {node.subtype}"
                    port_name_set = set()

                    for n in neighbors:
                        ne_data = self.G.nodes[n]
                        ne_type, ne_subtype = getMainAndSubType(ne_data)

                        port_name = ne_data["port_name"]
                        assert ne_type == "锚点", f"节点 #{n} 错误的节点类型: {ne_type}"
                        assert (
                            len(list(self.G.neighbors(n))) == 2
                        ), f"节点 #{n} 相邻节点数错误: {len(list(self.G.neighbors(n)))} 相邻节点: {(list(self.G.neighbors(n)))}"
                        port_name_set.add(port_name)

                    assert (
                        port_name_set == 设备接口名称集合[node.subtype]
                    ), f"节点 #{node.id}  PORT SET: {port_name_set} TARGET: {设备接口名称集合[node.subtype]}"
                except Exception as e:
                    if ies_env.FAILSAFE or ies_env.IGNORE_ANCHOR_EXCEPTIONS:
                        logger_print("Ignoring exception in device type:", node.subtype)
                        logger_traceback(e)
                    else:
                        raise e
            elif node.type == "连接线":
                assert (
                    len(neighbors) == 2
                ), f"节点 #{node.id} 不合理连接线相邻节点数: {len(neighbors)} 相邻节点: {neighbors}"
                dev_ids = set()
                subtypes = []

                for n in neighbors:
                    ne_data = self.G.nodes[n]
                    ne_type, ne_subtype = getMainAndSubType(ne_data)

                    assert ne_type in ["锚点", "母线"]
                    if ne_type == "锚点":
                        dev_ids.add(ne_data["device_id"])
                    else:
                        dev_ids.add(n)
                assert (
                    len(dev_ids) == 2
                ), f"节点 #{node.id} invalid dev_ids: {dev_ids}"  # no self-connection.
            elif node.type == "合并线":
                合并线ID列表.append(node.id)
                assert (
                    len(neighbors) == 2
                ), f"节点 #{node.id} 不合理相邻节点数: {len(neighbors)} 相邻节点: {len(neighbors)}"
                node_ids = set()

                for n in neighbors:
                    ne_data = self.G.nodes[n]
                    ne_type, ne_subtype = getMainAndSubType(ne_data)

                    assert ne_type == "母线", f"节点 #{n} 不合理类型: {ne_type}"
                    node_ids.add(n)
                assert (
                    len(node_ids) == 2
                ), f"节点 #{node.id} 不合理合并线总节点数：{len(node_ids)} 节点列表: {node_ids}"
            elif node.type == "锚点":
                continue
            else:
                raise Exception("unknown node type:", node.type)
        subgraph = self.G.subgraph(母线ID列表 + 合并线ID列表)  # check again.
        logger_print("母线ID列表:", 母线ID列表)
        self.合并母线ID集合列表 = list(networkx.connected_components(subgraph))
        self.合并母线ID集合列表 = [
            set([i for i in e if i not in 合并线ID列表]) for e in self.合并母线ID集合列表
        ]
        logger_print("合并母线ID集合列表:", self.合并母线ID集合列表)

    def check_consistency(self):
        self._check_consistency()
        verified = False
        isomorphic_topo_status = None
        if ies_env.DYNAMIC_TYPE_VERIFICATION:
            verified, isomorphic_topo_status = dynamic_verify_topo_object(self)
        else:
            logger_print("skipping dynamic verification")
            verified = True
        if not verified:
            raise Exception("Dynamical verification failed.")
        self.is_valid = True
        return verified, isomorphic_topo_status

    def to_json(self) -> dict:
        data = json_graph.node_link_data(self.G)
        return data

    @staticmethod
    def from_json(data):
        # load data to graph
        G = json_graph.node_link_graph(data)
        kwargs = G.graph
        topo = 拓扑图(**kwargs)
        topo.G = G
        try:
            topo.check_consistency()
        except Exception as e:
            if not ies_env.FAILSAFE:
                raise e
            else:
                logger_traceback(e)
                logger_print("检测到拓扑图不合法，但仍然继续运行")
        return topo

    # with checking.
    # iterate through all nodes.


# 下面的都需要传拓扑图进来


class 节点:
    def __init__(self, topo: 拓扑图, **kwargs):
        self.topo = topo
        self.kwargs = kwargs
        self.id = self.topo.add_node(**kwargs)


class 母线(节点):
    def __init__(self, topo: 拓扑图, subtype: str, **kwargs):
        super().__init__(topo, type="母线", subtype=subtype, conn=[], **kwargs)
        # infinite ports.


class 设备(节点):
    def __init__(
        self, topo: 拓扑图, device_type: str, port_definition, **kwargs  # iterable.
    ):
        # check if device type is one of the common types.
        super().__init__(topo, type="设备", subtype=device_type, ports={}, **kwargs)
        self.ports = {}
        for port_name in port_definition:
            subtype = "unknown"
            port_node_id = self.topo.add_node(
                type="锚点", port_name=port_name, subtype=subtype, device_id=self.id
            )
            self.ports.update({port_name: {"subtype": subtype, "id": port_node_id}})
            self.topo.G.add_edge(self.id, port_node_id)
        self.topo.G.nodes[self.id]["ports"] = self.ports


class 连接节点(节点):
    def __init__(
        self,
        topo: 拓扑图,
        _type: str,
        subtype: str,
        conn_start_id: int,
        conn_end_id: int,
        **kwargs,
    ):
        super().__init__(topo, type=_type, subtype=subtype, **kwargs)
        self.topo.G.add_edge(conn_start_id, self.id)
        self.topo.G.add_edge(self.id, conn_end_id)
        if self.topo.G.nodes[conn_start_id]["type"] == "母线":
            self.topo.G.nodes[conn_start_id]["conn"].append(subtype)
        if self.topo.G.nodes[conn_end_id]["type"] == "母线":
            self.topo.G.nodes[conn_end_id]["conn"].append(subtype)


class 连接线(连接节点):
    def __init__(
        self, topo: 拓扑图, subtype: str, conn_start_id: int, conn_end_id: int, **kwargs
    ):
        super().__init__(
            topo,
            _type="连接线",
            subtype=subtype,
            conn_start_id=conn_start_id,
            conn_end_id=conn_end_id,
            **kwargs,
        )


class 合并线(连接节点):
    def __init__(
        self, topo: 拓扑图, subtype: str, conn_start_id: int, conn_end_id: int, **kwargs
    ):
        super().__init__(
            topo,
            _type="合并线",
            subtype=subtype,
            conn_start_id=conn_start_id,
            conn_end_id=conn_end_id,
            **kwargs,
        )


class 柴油(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="柴油", port_definition={"燃料接口"}, **kwargs
        )

        self.燃料接口 = self.ports["燃料接口"]["id"]


class 电负荷(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="电负荷", port_definition={"电接口"}, **kwargs
        )

        self.电接口 = self.ports["电接口"]["id"]


class 光伏发电(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="光伏发电", port_definition={"电接口"}, **kwargs
        )

        self.电接口 = self.ports["电接口"]["id"]


class 风力发电(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="风力发电", port_definition={"电接口"}, **kwargs
        )

        self.电接口 = self.ports["电接口"]["id"]


class 柴油发电(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="柴油发电", port_definition={"电接口", "燃料接口"}, **kwargs
        )

        self.电接口 = self.ports["电接口"]["id"]
        self.燃料接口 = self.ports["燃料接口"]["id"]


class 锂电池(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="锂电池", port_definition={"电接口"}, **kwargs
        )

        self.电接口 = self.ports["电接口"]["id"]


class 变压器(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="变压器", port_definition={"电输入", "电输出"}, **kwargs
        )

        self.电输入 = self.ports["电输入"]["id"]
        self.电输出 = self.ports["电输出"]["id"]


class 双向变压器(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="双向变压器", port_definition={"电输入", "电输出"}, **kwargs
        )

        self.电输入 = self.ports["电输入"]["id"]
        self.电输出 = self.ports["电输出"]["id"]


class 变流器(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="变流器", port_definition={"电输入", "电输出"}, **kwargs
        )

        self.电输入 = self.ports["电输入"]["id"]
        self.电输出 = self.ports["电输出"]["id"]


class 双向变流器(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="双向变流器", port_definition={"储能端", "线路端"}, **kwargs
        )

        self.储能端 = self.ports["储能端"]["id"]
        self.线路端 = self.ports["线路端"]["id"]


class 传输线(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="传输线", port_definition={"电输入", "电输出"}, **kwargs
        )

        self.电输入 = self.ports["电输入"]["id"]
        self.电输出 = self.ports["电输出"]["id"]


class 市政自来水(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="市政自来水", port_definition={"水接口"}, **kwargs
        )

        self.水接口 = self.ports["水接口"]["id"]


class 天然气(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="天然气", port_definition={"燃料接口"}, **kwargs
        )

        self.燃料接口 = self.ports["燃料接口"]["id"]


class 电网(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(topo=topo, device_type="电网", port_definition={"电接口"}, **kwargs)

        self.电接口 = self.ports["电接口"]["id"]


class 氢气(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="氢气", port_definition={"氢气接口"}, **kwargs
        )

        self.氢气接口 = self.ports["氢气接口"]["id"]


class 冷负荷(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="冷负荷", port_definition={"冷源接口"}, **kwargs
        )

        self.冷源接口 = self.ports["冷源接口"]["id"]


class 热负荷(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="热负荷", port_definition={"热源接口"}, **kwargs
        )

        self.热源接口 = self.ports["热源接口"]["id"]


class 蒸汽负荷(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="蒸汽负荷", port_definition={"蒸汽接口"}, **kwargs
        )

        self.蒸汽接口 = self.ports["蒸汽接口"]["id"]


class 氢负荷(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="氢负荷", port_definition={"氢气接口"}, **kwargs
        )

        self.氢气接口 = self.ports["氢气接口"]["id"]


class 燃气发电机(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="燃气发电机",
            port_definition={"高温烟气余热接口", "电接口", "燃料接口", "缸套水余热接口"},
            **kwargs,
        )

        self.高温烟气余热接口 = self.ports["高温烟气余热接口"]["id"]
        self.电接口 = self.ports["电接口"]["id"]
        self.燃料接口 = self.ports["燃料接口"]["id"]
        self.缸套水余热接口 = self.ports["缸套水余热接口"]["id"]


class 蒸汽轮机(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="蒸汽轮机", port_definition={"蒸汽接口", "电接口"}, **kwargs
        )

        self.蒸汽接口 = self.ports["蒸汽接口"]["id"]
        self.电接口 = self.ports["电接口"]["id"]


class 氢燃料电池(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="氢燃料电池",
            port_definition={"设备余热接口", "电接口", "氢气接口"},
            **kwargs,
        )

        self.设备余热接口 = self.ports["设备余热接口"]["id"]
        self.电接口 = self.ports["电接口"]["id"]
        self.氢气接口 = self.ports["氢气接口"]["id"]


class 平板太阳能(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="平板太阳能", port_definition={"热接口"}, **kwargs
        )

        self.热接口 = self.ports["热接口"]["id"]


class 槽式太阳能(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="槽式太阳能", port_definition={"热接口"}, **kwargs
        )

        self.热接口 = self.ports["热接口"]["id"]


class 余热热水锅炉(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="余热热水锅炉", port_definition={"烟气接口", "制热接口"}, **kwargs
        )

        self.烟气接口 = self.ports["烟气接口"]["id"]
        self.制热接口 = self.ports["制热接口"]["id"]


class 余热蒸汽锅炉(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="余热蒸汽锅炉", port_definition={"蒸汽接口", "烟气接口"}, **kwargs
        )

        self.蒸汽接口 = self.ports["蒸汽接口"]["id"]
        self.烟气接口 = self.ports["烟气接口"]["id"]


class 浅层地热井(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="浅层地热井",
            port_definition={"电接口", "冷源接口", "热源接口"},
            **kwargs,
        )

        self.电接口 = self.ports["电接口"]["id"]
        self.冷源接口 = self.ports["冷源接口"]["id"]
        self.热源接口 = self.ports["热源接口"]["id"]


class 中深层地热井(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="中深层地热井", port_definition={"电接口", "热源接口"}, **kwargs
        )

        self.电接口 = self.ports["电接口"]["id"]
        self.热源接口 = self.ports["热源接口"]["id"]


class 地表水源(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="地表水源",
            port_definition={"电接口", "冷源接口", "热源接口"},
            **kwargs,
        )

        self.电接口 = self.ports["电接口"]["id"]
        self.冷源接口 = self.ports["冷源接口"]["id"]
        self.热源接口 = self.ports["热源接口"]["id"]


class 水冷冷却塔(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="水冷冷却塔",
            port_definition={"电接口", "冷源接口", "水接口"},
            **kwargs,
        )

        self.电接口 = self.ports["电接口"]["id"]
        self.冷源接口 = self.ports["冷源接口"]["id"]
        self.水接口 = self.ports["水接口"]["id"]


class 余热热源(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="余热热源", port_definition={"热源接口"}, **kwargs
        )

        self.热源接口 = self.ports["热源接口"]["id"]


class 浅层双源四工况热泵(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="浅层双源四工况热泵",
            port_definition={"冷源接口", "制冷接口", "制热接口", "蓄冷接口", "热源接口", "电接口", "蓄热接口"},
            **kwargs,
        )

        self.冷源接口 = self.ports["冷源接口"]["id"]
        self.制冷接口 = self.ports["制冷接口"]["id"]
        self.制热接口 = self.ports["制热接口"]["id"]
        self.蓄冷接口 = self.ports["蓄冷接口"]["id"]
        self.热源接口 = self.ports["热源接口"]["id"]
        self.电接口 = self.ports["电接口"]["id"]
        self.蓄热接口 = self.ports["蓄热接口"]["id"]


class 中深层双源四工况热泵(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="中深层双源四工况热泵",
            port_definition={"冷源接口", "制冷接口", "制热接口", "蓄冷接口", "热源接口", "电接口", "蓄热接口"},
            **kwargs,
        )

        self.冷源接口 = self.ports["冷源接口"]["id"]
        self.制冷接口 = self.ports["制冷接口"]["id"]
        self.制热接口 = self.ports["制热接口"]["id"]
        self.蓄冷接口 = self.ports["蓄冷接口"]["id"]
        self.热源接口 = self.ports["热源接口"]["id"]
        self.电接口 = self.ports["电接口"]["id"]
        self.蓄热接口 = self.ports["蓄热接口"]["id"]


class 浅层双源三工况热泵(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="浅层双源三工况热泵",
            port_definition={"冷源接口", "制冰接口", "制冷接口", "制热接口", "热源接口", "电接口"},
            **kwargs,
        )

        self.冷源接口 = self.ports["冷源接口"]["id"]
        self.制冰接口 = self.ports["制冰接口"]["id"]
        self.制冷接口 = self.ports["制冷接口"]["id"]
        self.制热接口 = self.ports["制热接口"]["id"]
        self.热源接口 = self.ports["热源接口"]["id"]
        self.电接口 = self.ports["电接口"]["id"]


class 中深层双源三工况热泵(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="中深层双源三工况热泵",
            port_definition={"冷源接口", "制冰接口", "制冷接口", "制热接口", "热源接口", "电接口"},
            **kwargs,
        )

        self.冷源接口 = self.ports["冷源接口"]["id"]
        self.制冰接口 = self.ports["制冰接口"]["id"]
        self.制冷接口 = self.ports["制冷接口"]["id"]
        self.制热接口 = self.ports["制热接口"]["id"]
        self.热源接口 = self.ports["热源接口"]["id"]
        self.电接口 = self.ports["电接口"]["id"]


class 水冷螺杆机(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="水冷螺杆机",
            port_definition={"制冷接口", "电接口", "冷源接口", "蓄冷接口"},
            **kwargs,
        )

        self.制冷接口 = self.ports["制冷接口"]["id"]
        self.电接口 = self.ports["电接口"]["id"]
        self.冷源接口 = self.ports["冷源接口"]["id"]
        self.蓄冷接口 = self.ports["蓄冷接口"]["id"]


class 双工况水冷螺杆机组(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="双工况水冷螺杆机组",
            port_definition={"制冷接口", "电接口", "冷源接口", "制冰接口"},
            **kwargs,
        )

        self.制冷接口 = self.ports["制冷接口"]["id"]
        self.电接口 = self.ports["电接口"]["id"]
        self.冷源接口 = self.ports["冷源接口"]["id"]
        self.制冰接口 = self.ports["制冰接口"]["id"]


class 吸收式燃气热泵(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="吸收式燃气热泵", port_definition={"制热接口", "燃料接口"}, **kwargs
        )

        self.制热接口 = self.ports["制热接口"]["id"]
        self.燃料接口 = self.ports["燃料接口"]["id"]


class 空气源热泵(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="空气源热泵",
            port_definition={"制冷接口", "制热接口", "蓄冷接口", "电接口", "蓄热接口"},
            **kwargs,
        )

        self.制冷接口 = self.ports["制冷接口"]["id"]
        self.制热接口 = self.ports["制热接口"]["id"]
        self.蓄冷接口 = self.ports["蓄冷接口"]["id"]
        self.电接口 = self.ports["电接口"]["id"]
        self.蓄热接口 = self.ports["蓄热接口"]["id"]


class 蒸汽溴化锂(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="蒸汽溴化锂",
            port_definition={"蒸汽接口", "冷源接口", "制冷接口"},
            **kwargs,
        )

        self.蒸汽接口 = self.ports["蒸汽接口"]["id"]
        self.冷源接口 = self.ports["冷源接口"]["id"]
        self.制冷接口 = self.ports["制冷接口"]["id"]


class 热水溴化锂(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="热水溴化锂",
            port_definition={"制冷接口", "热水接口", "冷源接口"},
            **kwargs,
        )

        self.制冷接口 = self.ports["制冷接口"]["id"]
        self.热水接口 = self.ports["热水接口"]["id"]
        self.冷源接口 = self.ports["冷源接口"]["id"]


class 电热水锅炉(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="电热水锅炉", port_definition={"电接口", "制热接口"}, **kwargs
        )

        self.电接口 = self.ports["电接口"]["id"]
        self.制热接口 = self.ports["制热接口"]["id"]


class 电蒸汽锅炉(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="电蒸汽锅炉", port_definition={"蒸汽接口", "电接口"}, **kwargs
        )

        self.蒸汽接口 = self.ports["蒸汽接口"]["id"]
        self.电接口 = self.ports["电接口"]["id"]


class 天然气热水锅炉(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="天然气热水锅炉", port_definition={"制热接口", "燃料接口"}, **kwargs
        )

        self.制热接口 = self.ports["制热接口"]["id"]
        self.燃料接口 = self.ports["燃料接口"]["id"]


class 天然气蒸汽锅炉(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="天然气蒸汽锅炉", port_definition={"蒸汽接口", "燃料接口"}, **kwargs
        )

        self.蒸汽接口 = self.ports["蒸汽接口"]["id"]
        self.燃料接口 = self.ports["燃料接口"]["id"]


class 电解槽(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="电解槽",
            port_definition={"设备余热接口", "制氢接口", "电接口"},
            **kwargs,
        )

        self.设备余热接口 = self.ports["设备余热接口"]["id"]
        self.制氢接口 = self.ports["制氢接口"]["id"]
        self.电接口 = self.ports["电接口"]["id"]


class 水蓄能(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="水蓄能", port_definition={"蓄冷接口", "蓄热接口"}, **kwargs
        )

        self.蓄冷接口 = self.ports["蓄冷接口"]["id"]
        self.蓄热接口 = self.ports["蓄热接口"]["id"]


class 蓄冰槽(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="蓄冰槽", port_definition={"蓄冰接口"}, **kwargs
        )

        self.蓄冰接口 = self.ports["蓄冰接口"]["id"]


class 储氢罐(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="储氢罐", port_definition={"储氢接口"}, **kwargs
        )

        self.储氢接口 = self.ports["储氢接口"]["id"]


class 输水管道(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="输水管道",
            port_definition={"输入接口", "电接口", "输出接口"},
            **kwargs,
        )

        self.输入接口 = self.ports["输入接口"]["id"]
        self.电接口 = self.ports["电接口"]["id"]
        self.输出接口 = self.ports["输出接口"]["id"]


class 蒸汽管道(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="蒸汽管道", port_definition={"输入接口", "输出接口"}, **kwargs
        )

        self.输入接口 = self.ports["输入接口"]["id"]
        self.输出接口 = self.ports["输出接口"]["id"]


class 复合输水管道(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="复合输水管道",
            port_definition={"冷输出接口", "热输入接口", "冷输入接口", "电接口", "热输出接口"},
            **kwargs,
        )

        self.冷输出接口 = self.ports["冷输出接口"]["id"]
        self.热输入接口 = self.ports["热输入接口"]["id"]
        self.冷输入接口 = self.ports["冷输入接口"]["id"]
        self.电接口 = self.ports["电接口"]["id"]
        self.热输出接口 = self.ports["热输出接口"]["id"]


class 水水换热器(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="水水换热器", port_definition={"输入接口", "输出接口"}, **kwargs
        )

        self.输入接口 = self.ports["输入接口"]["id"]
        self.输出接口 = self.ports["输出接口"]["id"]


class 复合水水换热器(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="复合水水换热器",
            port_definition={"冷输出接口", "热输入接口", "冷输入接口", "热输出接口"},
            **kwargs,
        )

        self.冷输出接口 = self.ports["冷输出接口"]["id"]
        self.热输入接口 = self.ports["热输入接口"]["id"]
        self.冷输入接口 = self.ports["冷输入接口"]["id"]
        self.热输出接口 = self.ports["热输出接口"]["id"]


class 气水换热器(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="气水换热器", port_definition={"输入接口", "输出接口"}, **kwargs
        )

        self.输入接口 = self.ports["输入接口"]["id"]
        self.输出接口 = self.ports["输出接口"]["id"]
