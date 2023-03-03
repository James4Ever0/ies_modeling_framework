from integratedEnergySystemPrototypes import EnergyFlowNodeFactory
import networkx as nx
import matplotlib.pyplot as plt
def visualizeSystemTopology(NodeFactory:EnergyFlowNodeFactory):
    electricity_type = 'electricity'
    Node1 = NodeFactory.create_node(electricity_type)
    draw_options = {'node_color': 'yellow','node_size': 1000,}

    G = nx.DiGraph()

    