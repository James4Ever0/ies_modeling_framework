import networkx as nx

G = nx.DiGraph()

G.add_node('PhotoVoltaic')
G.add_node('BESS')
G.add_node('LOAD')
G.add_node('[NODE1]')
G.add_node('[NODE2]')
G.add_node('GRID')

G.add_edge('PhotoVoltaic','[NODE1]')
G.add_edge('[NODE1]','BESS')
G.add_edge('BESS','[NODE2]')
G.add_edge('[NODE2]','LOAD')



import matplotlib.pyplot as plt

nx.draw(G)
plt.show()