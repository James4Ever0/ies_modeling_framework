from integratedEnergySystemPrototypes import EnergyFlowNodeFactory
import networkx as nx
import matplotlib.pyplot as plt


def visualizeSystemTopology(
    NodeFactory: EnergyFlowNodeFactory,
    draw_options={
        "node_color": "yellow",
        "node_size": 1000,
    },
):
    G = nx.DiGraph()
    node_index = 0

    for device_id in NodeFactory.device_ids:
        device_node_name = f"{device_id}_device"
        G.add_node(device_node_name)

    for node in NodeFactory.nodes:
        node_name = f"{node.energy_type}_{node_index}"
        G.add_node(node_name)
        node_index += 1
        # G.add_node(2,"BESS")
        for input_id in node.input_ids:
            device_id = input_id.split("_")[0]
            device_node_name = f"{device_node}_device"
            G.add_edge(device_node_name,node_name)

        for output_id in node.output_ids:
            input_id.split("_")[0]
            device_node_name = f"{device_node}_device"
            G.add_edge(node_name,device_node_name)
