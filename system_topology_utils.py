from integratedEnergySystemPrototypes import EnergyFlowNodeFactory
import networkx as nx
import matplotlib.pyplot as plt


def visualizeSystemTopology(
    NodeFactory: EnergyFlowNodeFactory,
    draw_options={
        "node_color": "yellow",
        "node_size": 1000,
    },
    system_name="ies_system",
):
    G = nx.DiGraph()
    node_index = 0

    for device_id in NodeFactory.device_ids:
        device_name = NodeFactory.device_id_to_device_name[device_id]
        device_node_name = f"{device_name}_{device_id[:4]}_device"
        G.add_node(device_node_name)

    for node in NodeFactory.nodes:
        node_name = f"{node.energy_type}_io_{node_index}"
        G.add_node(node_name)
        node_index += 1
        # G.add_node(2,"BESS")
        for input_id in node.input_ids:
            device_id = input_id.split("_")[0]
            try:
                # device_id = input_id
                device_node_name = f"{NodeFactory.device_id_to_device_name[device_id]}_{device_id[:4]}_device"
                G.add_edge(
                    node_name,
                    device_node_name,
                )
            except:
                breakpoint()
                pass

        for output_id in node.output_ids:
            device_id = output_id.split("_")[0]
            try:
                # device_id = output_id
                device_node_name = f"{NodeFactory.device_id_to_device_name[device_id]}_{device_id[:4]}_device"
                G.add_edge(
                    device_node_name,
                    node_name,
                )
            except:
                breakpoint()
                pass
    # breakpoint() # check how to save the graph as json.
    from networkx.readwrite import json_graph
    serialized = json_graph.dumps(G)
    import rich
    rich.print(serialized)
    breakpoint()
    nx.draw(G, with_labels=True, font_weight="bold", **draw_options)
    # plt.show()
    figure_path = f"topology_{system_name}.png"
    print("Saving figure to:", figure_path)
    plt.savefig(figure_path)
