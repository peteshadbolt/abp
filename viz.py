"""
Utility function for plotting graphs nicely
"""

import networkx as nx
from matplotlib import pyplot as plt
from graph import *

VOP_COLORS = ["red", "green", "blue"]

def draw(graph, vops, filename="out.pdf", ns=500):
    """ Draw a graph with networkx layout """
    g = nx.from_edgelist(edgelist(graph))
    pos = nx.spring_layout(g)
    colors = [VOP_COLORS[vop % len(VOP_COLORS)] for vop in vops]
    nx.draw_networkx_nodes(g, pos, node_color="white", node_size=ns)
    nx.draw_networkx_nodes(g, pos, node_color=colors, node_size=ns, alpha=.4)
    nx.draw_networkx_labels(g, pos)
    nx.draw_networkx_edges(g, pos)
    plt.axis('off')
    plt.savefig(filename)

if __name__ == '__main__':
    g, vops = graph(10)
    add_edge(g, 0, 1)
    add_edge(g, 1, 3)
    add_edge(g, 3, 2)
    add_edge(g, 3, 0)
    add_edge(g, 2, 0)
    edgelist(g)
    draw(g, vops)

