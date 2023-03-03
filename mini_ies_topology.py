import networkx as nx

G = nx.DiGraph()

G.nodes.data()
NodeDataView({1: {'time': '5pm', 'room': 714}, 3: {'time': '2pm'}})


import matplotlib.pyplot as plt

nx.draw(G)
plt.show()