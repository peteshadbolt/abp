"""
This is a sketch of a consistent language for defining resource states and lattices.
"""

import networkx as nx
from abp.fancy import GraphState

def union(*graphs):
    """ Assumes that all graphs are completely independent and uniquely labelled """
    output = nx.Graph()
    output.node = dict(i for g in graphs for i in g.node.items())
    output.adj = dict(i for g in graphs for i in g.adj.items())
    return output

def relabel(g, label):
    """ Shorthand relabel """
    return nx.relabel_nodes(g, lambda x: (label, x))

def fuse(psi, na, nb):
    """ Deterministic fusion for testing purposes """
    neighbors_a, neighbors_b = psi.neighbors(na), psi.neighbors(nb)
    new_edges = ((i, j) for i in neighbors_a for j in neighbors_b if i != j)
    psi.add_edges_from(new_edges)
    psi.remove_nodes_from((na, nb))
    return psi

def ghz(label):
    """ A 3-GHZ state """
    psi = nx.Graph(((0, 1), (1, 2)))
    return relabel(psi, label)

def microcluster(label):
    """ A microcluster """
    psi = union(ghz(0), ghz(1), ghz(2))
    psi = fuse(psi, (0, 1), (1, 0))
    psi = fuse(psi, (1, 2), (2, 1))
    return relabel(psi, label)

def unit_cell(label):
    """ A simple ring-like unit cell """
    psi = union(microcluster(0), microcluster(1), microcluster(2), microcluster(3))
    psi = fuse(psi, (0, (0, 2)), (1, (2, 2)))
    psi = fuse(psi, (1, (0, 2)), (2, (2, 2)))
    psi = fuse(psi, (2, (0, 2)), (3, (2, 2)))
    psi = fuse(psi, (3, (0, 2)), (0, (2, 2)))
    return relabel(psi, label)

def position(node):
    print node
    return {}

def annotate(g, f):
    """ Annotate a graph """
    for node in g.nodes():
        g.node[node].update(f(node))

if __name__ == '__main__':
    psi = union(unit_cell((0, 0)), unit_cell((2, 0)))
    annotate(psi, position)
    g = GraphState(psi)

