from integratedEnergySystemPrototypes import EnergyFlowNodeFactory
import networkx as nx
import matplotlib.pyplot as plt
def visualizeSystemTopology(NodeFactory:EnergyFlowNodeFactory):
    for node in NodeFactory.nodes:
        draw_options = {'node_color': 'yellow','node_size': 1000,}

        G = nx.DiGraph()
        G.add_node(1,"photoVoltaic")
        G.add_node(2,"BESS")
        

    