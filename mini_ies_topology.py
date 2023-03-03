import networkx as nx

G = nx.DiGraph()

n1 =
n2 ={'attr':'b'}

G.add_edge(n1,n2,)

import matplotlib.pyplot as plt

nx.draw(G)
plt.show()