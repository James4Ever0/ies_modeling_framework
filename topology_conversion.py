# replace the original topology with other stuff.
import networkx

G = networkx.Graph()

a = G.add_node("a")
b = G.add_node("b")
c = G.add_node("c")

G.add_edge("a", "b")
G.add_edge("b", "c")
G.add_edge("c", "a")

# convert to other graph.
#                        b
#                        |
#   b                 [io_2]
#  / \              /        \  
# a - c  =>   a - [io_0] - [io_1] - c
# 
# ###########################