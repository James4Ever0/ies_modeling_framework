# import networkx as nx
# from aco_tsp import ACO, Graph

# # define the set of nodes/devices
# devices = ['Diesel source', 'Diesel generator', 'Solar power generator', 'Wind power generator', 'Power converter', 'Power lines', 'Power load']

# # define the set of rules
# rules = {
#     'Diesel source': ['Diesel generator'],
#     'Diesel generator': ['Power lines'],
#     'Solar power generator': ['Power lines'],
#     'Wind power generator': ['Power lines'],
#     'Power converter': ['Power lines', 'Power load'],
#     'Power lines': ['Diesel generator', 'Solar power generator', 'Wind power generator', 'Power converter'],
#     'Power load': ['Power converter']
# }

# # define the graph
# G = Graph(len(devices), devices)

# # add edges based on the rules
# for i in range(len(devices)):
#     for j in range(i+1, len(devices)):
#         if devices[j] in rules[devices[i]]:
#             G.add_edge(i, j, 1)  # add an edge with cost 1 if the nodes can be connected

# # define the ACO parameters
# aco = ACO(ants=10, generations=100, alpha=1.0, beta=10.0, rho=0.5, q=1.0)

# # run the ACO algorithm to generate the graph
# path, cost = aco.solve(G)

# # convert the path to a NetworkX graph
# edges = [(devices[path[i]], devices[path[i+1]]) for i in range(len(path)-1)]
# G_nx = nx.Graph(edges)

# # visualize the graph
# nx.draw(G_nx, with_labels=True)

# above code does not seem to be right.
# the library is fictional.
# TSP is not of our type of problem.

import networkx as nx

# set the maximum number of nodes/devices
max_nodes = 10

# create an empty graph
G = nx.Graph()

# add the initial nodes/devices
devices = [
    "Diesel source",
    "Diesel generator",
    "Solar power generator",
    "Wind power generator",
    "Power lines",
]
G.add_nodes_from(devices)

# add edges based on the rules
G.add_edge("Diesel source", "Diesel generator")
G.add_edge("Diesel generator", "Power lines")
G.add_edge("Solar power generator", "Power lines")
G.add_edge("Wind power generator", "Power lines")


import random

# use the BA model to add new nodes with connections
for i in range(len(devices), max_nodes):
    G.add_node(i)
    # connect to existing nodes with probability proportional to their degree
    targets = list(G.nodes())
    probabilities = [
        deg / sum(dict(G.degree()).values()) for deg in dict(G.degree()).values()
    ]
    for j in range(len(targets)):
        if i != targets[j]:
            if random.choices(
                [True, False], weights=[probabilities[j], 1 - probabilities[j]], k=1
            )[0]:
                # if nx.utils.random.choice([True, False], p=[probabilities[j], 1-probabilities[j]]):
                G.add_edge(i, targets[j])

import matplotlib.pyplot as plt

nx.draw(G)
plt.show()
