import networkx as nx

G = nx.DiGraph()

G.add_node('PhotoVoltaic')
G.add_node('BESS')
G.add_node('LOAD')
G.add_node('[NODE1]')
G.add_node('[NODE2]')
G.add_node('GRID')

G.add_edge

G.add_edge('PhotoVoltaic','[NODE1]')

import matplotlib.pyplot as plt

nx.draw(G)
plt.show()