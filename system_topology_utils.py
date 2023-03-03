from integratedEnergySystemPrototypes import EnergyFlowNodeFactory
import networkx as nx
import matplotlib.pyplot as plt
def visualizeSystemTopology(NodeFactory:EnergyFlowNodeFactory):
    draw_options = {'node_color': 'yellow','node_size': 1000,}

    G = nx.DiGraph()
    
    