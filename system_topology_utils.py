from integratedEnergySystemPrototypes import EnergyFlowNodeFactory
import networkx as nx
import matplotlib.pyplot as plt
def visualizeSystemTopology(NodeFactory:EnergyFlowNodeFactory):
    G = nx.DiGraph()
    node_index=0
    draw_options = {'node_color': 'yellow','node_size': 1000,}
    for node in NodeFactory.nodes:
        node_name = f"{node.energy_type}_{node_index}"
        G.add_node(node_name)
        node_index+=1
        # G.add_node(2,"BESS")
        for device_node in NodeFactory.
    