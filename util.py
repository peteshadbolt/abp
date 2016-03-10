""" 
Useful but messy crap
"""
import cPickle
import networkx as nx
from matplotlib import pyplot as plt
from graph import *
import clifford
import numpy as np

VOP_COLORS = ["red", "green", "blue", "orange", "yellow", "purple", "black", "white"]

def cache_to_disk(file_name):
    """ A decorator to cache the output of a function to disk """
    def wrap(func):
        def modified(*args, **kwargs):
            try:
                output = cPickle.load(open(file_name, "r"))
            except (IOError, ValueError):
                output = func(*args, **kwargs)
                with open(file_name, "w") as f:
                    cPickle.dump(output, f)
            return output
        return modified
    return wrap


def draw(graph, vops, filename="out.pdf", pos=None, ns=500):
    """ Draw a graph with networkx layout """
    plt.clf()
    g = nx.from_edgelist(edgelist(graph))
    pos = nx.spring_layout(g) if pos==None else pos
    colors = [VOP_COLORS[vop % len(VOP_COLORS)] for vop in vops]
    nx.draw_networkx_nodes(g, pos, node_color="white", node_size=ns)
    nx.draw_networkx_nodes(g, pos, node_color=colors, node_size=ns, alpha=.4)
    nx.draw_networkx_edges(g, pos, edge_color="gray")
    nx.draw_networkx_labels(g, pos, font_family="FreeSans")

    labels = {i: clifford.name_of(vops[i]) for i in g.nodes()}
    pos = {k: v + np.array([0, -.1]) for k, v in pos.items()}
    nx.draw_networkx_labels(g, pos, labels, font_family="FreeSans")
    plt.axis('off')
    plt.savefig(filename)
    return pos

