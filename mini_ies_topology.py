import networkx as nx

G = nx.DiGraph()

G.add_node(1,PhotoVoltaic='2pm')
G.add_node(2,BESS='2pm')
G.add_node(3,LOAD='2pm')
G.add_node(4,NODE1='2pm')
G.add_node(5,NODE2='2pm')
G.add_node(6,GRID='2pm')

G.add_edge(1,4)
G.add_edge(4,2)
G.add_edge(2,5)
G.add_edge(5,3)
G.add_edge(4,6)
G.add_edge(6,5)



import matplotlib.pyplot as plt

nx.draw(G)
plt.show()