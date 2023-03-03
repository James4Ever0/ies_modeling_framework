import networkx as nx

G = nx.DiGraph()

G.add_node("PV")
G.add_node("BESS")
G.add_node("LOAD")
G.add_node("[NODE1]")
G.add_node("GRID")

G.add_edge("PV","[NODE1]")
G.add_edge('BESS','[NODE1]')
G.add_edge('[NODE1]','BESS')


import matplotlib.pyplot as plt

nx.draw(G)
plt.show()