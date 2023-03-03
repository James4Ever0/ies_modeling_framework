from integratedEnergySystemPrototypes import EnergyFlowNodeFactory
import networkx as nx
import matplotlib.pyplot as plt
def visualizeSystemTopology(NodeFactory:EnergyFlowNodeFactory):
    draw_options = {'node_color': 'yellow','node_size': 1000,}
    G = nx.DiGraph()
    G.add_node("PV")
    G.add_node("BESS")
    G.add_node("LOAD")
    G.add_node("[NODE1]")
    G.add_node("GRID")

    G.add_edge("PV","[NODE1]")
    G.add_edge('BESS','[NODE1]')
    G.add_edge('[NODE1]','BESS')
    G.add_edge('GRID','[NODE1]')
    G.add_edge('[NODE1]','GRID')
    G.add_edge('[NODE1]','LOAD')

    nx.draw(G,with_labels=True, font_weight='bold',**draw_options
     )
    plt.show()
    