import networkx as nx
from matplotlib import pyplot as plt
import clifford
import numpy as np
from graph import GraphState

VOP_COLORS = ["red", "green", "blue", "orange", "yellow", "purple", "black", "white"]

def draw(state, filename="out.pdf", pos=None, ns=500):
    """ Draw a graph with networkx layout """
    plt.clf()
    graph = nx.from_edgelist(state.edgelist())
    pos = nx.spring_layout(graph) if pos==None else pos
    colors = [VOP_COLORS[vop % len(VOP_COLORS)] for vop in state.vops.values()]
    nx.draw_networkx_nodes(graph, pos, node_color="white", node_size=ns)
    nx.draw_networkx_nodes(graph, pos, node_color=colors, node_size=ns, alpha=.4)
    nx.draw_networkx_edges(graph, pos, edge_color="gray")
    nx.draw_networkx_labels(graph, pos, font_family="FreeSans")

    # tables.name_of(v)
    labels = {i: "no name" for i, v in state.vops.items()}
    pos = {k: v + np.array([0, -.1]) for k, v in pos.items()}
    nx.draw_networkx_labels(graph, pos, labels, font_family="FreeSans")
    plt.axis('off')
    plt.savefig(filename)
    return pos
