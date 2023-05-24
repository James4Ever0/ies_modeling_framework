class A:
    def __init__(self):
        ...
    
    def B(self):
        return B(self)

class B:
    def __init__(self, a:A):
        self.a = a
        print("CLASS NAME?", self.__class__.__name__)
        print("CREATING B")

a = A()
b = a.B()

import networkx as nx

G = nx.Graph()

G.add_node(1, **{"val":1, "val2":2})
G.add_node(2, **{"val":1, "val2":2})
G.add_node(3, **{"val":1, "val2":2})

G.add_edge(1,2)

# G.neighbors(node_id)
for n_with_items in G.nodes.items():
    n,d = n_with_items
    print("NODE", n, type(n))
    print("DATA", d, type(d))
    