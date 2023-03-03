import networkx as nx

G = nx.DiGraph()

G.add_nodes_from([
    (4, {"color": "red"}),
    (5, {"color": "green"}),
])


import matplotlib.pyplot as plt

nx.draw(G)
plt.show()