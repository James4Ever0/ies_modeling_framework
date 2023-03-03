import networkx as nx

G = nx.DiGraph()

G.add_node(1,'PhotoVoltaic')
G.add_node(2,'BESS')
G.add_node(3,'LOAD')
G.add_node(4,'[NODE1]')
G.add_node(5,'[NODE2]')
G.add_node(6,'GRID')

G.add_edge('PhotoVoltaic','[NODE1]')
G.add_edge('[NODE1]','BESS')
G.add_edge('BESS','[NODE2]')
G.add_edge('[NODE2]','LOAD')
G.add_edge('[NODE1]','GIRD')
G.add_edge('GIRD','[NODE2]')



import matplotlib.pyplot as plt

nx.draw(G)
plt.show()