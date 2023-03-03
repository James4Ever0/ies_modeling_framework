import networkx as nx

G = nx.DiGraph()

G.add_nodes_from([
    (PV, {"color": "red"}),
    (BESS, {"color": "green"}),
])


import matplotlib.pyplot as plt

nx.draw(G)
plt.show()