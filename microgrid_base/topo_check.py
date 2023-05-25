import networkx
from networkx.readwrite import json_graph

# when to check topology:
# 	1.  Building topology <- which the frontend does the job
# 	2.  Importing topology <- where algorithm kicks in

# so here we only check topo when importing. we don't check validity during the building.


# 母线最多99个对接的接口


def getMainAndSubType(data):
    print("DATA:", data)
    return data["type"], data["subtype"]


# better use some template.
# 设备、母线、连接线、合并线
锚点类型 = [
    "变流器输入",
    "变压器输出",
    "供电端输出",
    "电母线输入",
    "电储能端输入输出",
    "双向变流器储能端输入输出",
    "电母线输出",
    "双向变流器线路端输入输出",
    "负荷电输入",
    "柴油输入",
    "柴油输出",
]

母线类型 = ["可连接电储能端母线", "可连接供电端母线", "可连接负荷电母线", "可连接电母线", "可连接柴油母线"]

连接线类型 = [
    "不可连接电储能端母线输出",
    "不可连接负荷电母线",
    "不可连接电母线",
    "不可连接电母线输入输出",
    "不可连接供电端母线输入",
    "不可连接电储能端母线输入",
    "不可连接负荷电母线输入",
    "不可连接供电端母线输入输出",
    "不可连接负荷电母线输出",
    "不可连接电母线输出",
    "不可连接电储能端母线",
    "不可连接供电端母线输出",
    "不可连接负荷电母线输入输出",
    "不可连接电储能端母线输入输出",
    "不可连接电母线输入",
    "不可连接供电端母线",
    "不可连接柴油母线",
    "不可连接柴油母线输入输出",
    "不可连接柴油母线输出",
    "不可连接柴油母线输入",
]

合并线类型 = ["可合并供电端母线", "可合并电母线", "可合并电储能端母线", "可合并负荷电母线", "可合并柴油母线"]

设备类型 = ["柴油", "电负荷", "光伏发电", "风力发电", "柴油发电", "锂电池", "变压器", "变流器", "双向变流器", "传输线"]


设备接口集合 = {
    "柴油": {("燃料接口", "柴油输出")},
    "电负荷": {("电接口", "负荷电输入")},
    "光伏发电": {("电接口", "供电端输出")},
    "风力发电": {("电接口", "供电端输出")},
    "柴油发电": {("燃料接口", "柴油输入"), ("电接口", "供电端输出")},
    "锂电池": {("电接口", "电储能端输入输出")},
    "变压器": {("电输出", "变压器输出"), ("电输入", "电母线输入")},
    "变流器": {("电输出", "电母线输出"), ("电输入", "变流器输入")},
    "双向变流器": {("储能端", "双向变流器储能端输入输出"), ("线路端", "双向变流器线路端输入输出")},
    "传输线": {("电输出", "电母线输出"), ("电输入", "电母线输入")},
}
连接类型映射表 = {
    frozenset({"可连接电母线", "双向变流器线路端输入输出"}): "不可连接电母线输入输出",
    frozenset({"变流器输入", "供电端输出"}): "不可连接供电端母线",
    frozenset({"可连接供电端母线"}): "可合并供电端母线",
    frozenset({"变流器输入", "可连接供电端母线"}): "不可连接供电端母线输出",
    frozenset({"可连接供电端母线", "供电端输出"}): "不可连接供电端母线输入",
    frozenset({"变压器输出", "负荷电输入"}): "不可连接负荷电母线",
    frozenset({"可连接负荷电母线"}): "可合并负荷电母线",
    frozenset({"可连接负荷电母线", "负荷电输入"}): "不可连接负荷电母线输出",
    frozenset({"变压器输出", "可连接负荷电母线"}): "不可连接负荷电母线输入",
    frozenset({"柴油输出", "柴油输入"}): "不可连接柴油母线",
    frozenset({"可连接柴油母线"}): "可合并柴油母线",
    frozenset({"柴油输入", "可连接柴油母线"}): "不可连接柴油母线输出",
    frozenset({"柴油输出", "可连接柴油母线"}): "不可连接柴油母线输入",
    frozenset({"电母线输入", "电母线输出"}): "不可连接电母线",
    frozenset({"可连接电母线"}): "可合并电母线",
    frozenset({"可连接电母线", "电母线输入"}): "不可连接电母线输出",
    frozenset({"可连接电母线", "电母线输出"}): "不可连接电母线输入",
    frozenset({"电储能端输入输出", "双向变流器储能端输入输出"}): "不可连接电储能端母线",
    frozenset({"可连接电储能端母线"}): "可合并电储能端母线",
    frozenset({"电储能端输入输出", "可连接电储能端母线"}): "不可连接电储能端母线输出",
    frozenset({"双向变流器储能端输入输出", "可连接电储能端母线"}): "不可连接电储能端母线输入",
}


def getMainAndSubtype(data):
    mainType = data["type"]
    subType = data["subtype"]
    return mainType, subType


class 拓扑图:
    def __init__(self, **kwargs):
        self.node_count = 0
        self.G = networkx.Graph(**kwargs)
        self.合并母线ID集合列表 = []
        self.is_valid = False

    def get_all_devices(self) -> list:
        devs = []
        for node_index, node_data in self.G.nodes.items():
            node_type = node_data["type"]
            if node_type == "设备":
                devs.append(node_data)
        return devs

    def get_all_adders(self) -> dict:  # don't care about types here.
        # use adder ids. adder starts with -1
        adders = {
            min(s): {"input": [], "output": [], "IO": []} for s in self.合并母线ID集合列表
        }  # 用到：合并母线ID集合列表
        adder_id = -1
        母线ID映射表 = {e: min(s) for s in self.合并母线ID集合列表 for e in s}
        # format: {"input":input_ids, "output": output_ids, "IO": IO_ids}
        for node_index, node_data in self.G.nodes.items():
            node_type = node_data["type"]
            if node_type == "连接线":
                adder = {"input": [], "output": [], "IO": []}
                #  检查连接线两端
                left_id, right_id = self.G.neighbors(node_index)

                left_type = self.G.nodes[left_id]["type"]
                right_type = self.G.nodes[right_id]["type"]

                left_subtype = self.G.nodes[left_id]["subtype"]
                right_subtype = self.G.nodes[right_id]["subtype"]

                if left_type == "锚点" and right_type == "锚点":

                    if left_subtype.endswith("输入输出"):
                        adder["IO"].append(left_id)
                    elif left_subtype.endswith("输入"):
                        adder["output"].append(left_id)
                    elif left_subtype.endswith("输出"):
                        adder["input"].append(left_id)
                    else:
                        raise Exception("Unknown type:", left_subtype)

                    adders[adder_id] = adder
                    adder_id -= 1

                if left_type == "母线" and right_type == "锚点":
                    (left_id, left_type, left_subtype), (
                        right_id,
                        right_type,
                        right_subtype,
                    ) = (right_id, right_type, right_subtype), (
                        left_id,
                        left_type,
                        left_subtype,
                    )

                if left_type == "锚点" and right_type == "母线":
                    madder_id = 母线ID映射表[right_id]

                    if left_subtype.endswith("输入输出"):
                        adders[madder_id]["IO"].append(left_id)
                    elif left_subtype.endswith("输入"):
                        adders[madder_id]["output"].append(left_id)
                    elif left_subtype.endswith("输出"):
                        adders[madder_id]["input"].append(left_id)
                    else:
                        raise Exception("Unknown type:", left_subtype)

                else:
                    raise Exception(f"不合理的连接线两端：{left_type}-{right_type}")
        return adders

    def get_graph_data(self) -> dict:  # primary data. shall be found somewhere.
        graph_data = self.G.graph
        return graph_data

    def add_node(self, **kwargs):
        self.G.add_node(self.node_count, **kwargs)
        node_id = self.node_count
        self.node_count += 1
        return node_id

    # monotonically adding a node.
    def check_consistency(self):  # return nothing.
        #  use subgraph
        # 提取所有母线ID
        母线ID列表 = []
        for node_id, node_data in self.G.nodes.items():
            node_type, node_subtype = getMainAndSubType(node_data)
            print("NODE TYPE:", node_type)
            print("NODE SUBTYPE:", node_subtype)
            neighbors = self.G.neighbors(node_id)
            print("NEIGHBORS:", list(neighbors))
            for n in neighbors:
                print(self.G.nodes[n])
            print("=" * 40)
            if node_type == "母线":
                母线ID列表.append(node_id)
                assert node_subtype in 母线类型
                assert len(neighbors) <= 99

                for n in neighbors:
                    ne_data = self.G[n]
                    ne_type, ne_subtype = getMainAndSubtype(ne_data)

                    if ne_type == "合并线":
                        # just check type.
                        assert ne_subtype in 合并线类型
                        assert ne_subtype.replace("合并", "连接") == node_subtype
                    elif ne_type == "连接线":
                        assert ne_subtype in 连接线类型
                        assert (
                            ne_subtype.replace("不可", "可")
                            .replace("输入", "")
                            .replace("输出", "")
                            == node_subtype
                        )
                    else:
                        raise Exception(f"{node_subtype}连接非法类型节点：", ne_type)
            elif node_type == "设备":
                assert node_subtype in 设备类型
                port_set = set()

                for n in neighbors:
                    ne_data = self.G[n]
                    ne_type, ne_subtype = getMainAndSubtype(ne_data)

                    port_name = ne_data["port_name"]
                    assert ne_type == "锚点"
                    assert len(self.G.neighbors(n)) == 2
                    port_set.add((port_name, ne_subtype))
                try:
                    assert port_set == 设备接口集合[node_subtype]
                except:
                    print("PORT SET:", port_set)
                    print("TARGET:", 设备接口集合[node_subtype])
                    raise Exception()
            elif node_type == "连接线":
                assert node_subtype in 连接线类型
                assert len(neighbors) == 2
                dev_ids = set()
                subtypes = []

                for n in neighbors:
                    ne_data = self.G[n]
                    ne_type, ne_subtype = getMainAndSubtype(ne_data)

                    assert ne_type in ["锚点", "母线"]
                    subtypes.append(ne_subtype)
                    dev_ids.add(ne_data["device_id"])
                assert len(dev_ids) == 2  # no self-connection.
                assert 连接类型映射表[frozenset(subtypes)] == node_subtype
            elif node_type == "合并线":
                assert node_subtype in 合并线类型
                assert len(neighbors) == 2
                node_ids = set()

                for n in neighbors:
                    ne_data = self.G[n]
                    ne_type, ne_subtype = getMainAndSubtype(ne_data)

                    assert ne_type == "母线"
                    node_ids.add(n)
                assert len(node_ids) == 2
            else:
                raise Exception("unknown node type:", node_type)
            subgraph = self.G.subgraph(母线ID列表)  # check again.
            self.合并母线ID集合列表 = networkx.connected_components(subgraph)
            for id_set in self.合并母线ID集合列表:
                has_input = False
                has_output = False
                for node_id in id_set:
                    node_data = self.G.nodes[node_id]
                    conn = node_data["conn"]  # list.
                    for c in conn:
                        if not c.endswith("输入输出"):
                            if c.endswith("输入"):
                                has_input = True
                            elif c.endswith("输出"):
                                has_output = True
                            else:
                                raise Exception(
                                    f"{self.G.nodes[node_id]['type']}不可接受的连接类型: {c}"
                                )
                if has_input and has_output:
                    ...
                else:
                    print()
                    print("============ERROR LOG============")
                    print()
                    for n in id_set:
                        print("母线:", self.G.nodes[n])
                    print()
                    print("INPUT:", has_input)
                    print("OUTPUT:", has_output)
                    print()
                    raise Exception(f"母线组{id_set}未实现至少一进一出")
        self.is_valid = True

    def to_json(self) -> dict:
        data = json_graph.adjacency_data(self.G)
        return data

    @staticmethod
    def from_json(data):
        # load data to graph
        G = json_graph.adjacency_graph(data)
        kwargs = G.graph
        topo = 拓扑图(**kwargs)
        topo.G = G
        topo.check_consistency()
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
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(topo, type="母线", conn=[], **kwargs)
        # infinite ports.


class 设备(节点):
    def __init__(
        self, topo: 拓扑图, device_type: str, port_definition, **kwargs  # iterable.
    ):
        # check if device type is one of the common types.
        super().__init__(topo, type="设备", subtype=device_type, ports={}, **kwargs)
        self.ports = {}
        for port_name, port_type in port_definition:
            port_node_id = self.topo.add_node(
                type="锚点", port_name=port_name, subtype=port_type, device_id=self.id
            )
            self.ports.update({port_name: {"subtype": port_type, "id": port_node_id}})
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
            topo=topo, device_type="柴油", port_definition={("燃料接口", "柴油输出")}, **kwargs
        )

        self.燃料接口 = self.ports["燃料接口"]["id"]


class 电负荷(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="电负荷", port_definition={("电接口", "负荷电输入")}, **kwargs
        )

        self.电接口 = self.ports["电接口"]["id"]


class 光伏发电(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="光伏发电", port_definition={("电接口", "供电端输出")}, **kwargs
        )

        self.电接口 = self.ports["电接口"]["id"]


class 风力发电(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo, device_type="风力发电", port_definition={("电接口", "供电端输出")}, **kwargs
        )

        self.电接口 = self.ports["电接口"]["id"]


class 柴油发电(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="柴油发电",
            port_definition={("燃料接口", "柴油输入"), ("电接口", "供电端输出")},
            **kwargs,
        )

        self.燃料接口 = self.ports["燃料接口"]["id"]
        self.电接口 = self.ports["电接口"]["id"]


class 锂电池(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="锂电池",
            port_definition={("电接口", "电储能端输入输出")},
            **kwargs,
        )

        self.电接口 = self.ports["电接口"]["id"]


class 变压器(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="变压器",
            port_definition={("电输出", "变压器输出"), ("电输入", "电母线输入")},
            **kwargs,
        )

        self.电输出 = self.ports["电输出"]["id"]
        self.电输入 = self.ports["电输入"]["id"]


class 变流器(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="变流器",
            port_definition={("电输出", "电母线输出"), ("电输入", "变流器输入")},
            **kwargs,
        )

        self.电输出 = self.ports["电输出"]["id"]
        self.电输入 = self.ports["电输入"]["id"]


class 双向变流器(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="双向变流器",
            port_definition={("储能端", "双向变流器储能端输入输出"), ("线路端", "双向变流器线路端输入输出")},
            **kwargs,
        )

        self.储能端 = self.ports["储能端"]["id"]
        self.线路端 = self.ports["线路端"]["id"]


class 传输线(设备):
    def __init__(self, topo: 拓扑图, **kwargs):
        super().__init__(
            topo=topo,
            device_type="传输线",
            port_definition={("电输出", "电母线输出"), ("电输入", "电母线输入")},
            **kwargs,
        )

        self.电输出 = self.ports["电输出"]["id"]
        self.电输入 = self.ports["电输入"]["id"]
