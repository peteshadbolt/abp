import networkx as nx
from abp.fancy import GraphState

def fast_union(graphs):
    """ Assumes that all graphs are completely independent and uniquely labelled """
    output = nx.Graph()
    output.node = dict(i for g in graphs for i in g.node.items())
    output.adj = dict(i for g in graphs for i in g.adj.items())
    return output

def relabel(g, label):
    """ Shorthand relabel """
    return nx.relabel_nodes(g, lambda x: (label, x))

def fuse(a, b, na, nb):
    """ Deterministic fusion for testing purposes """
    psi = fast_union((a, b))
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
    psi = fuse(ghz(0), ghz(1), (0, 1), (1, 0))
    psi = fuse(psi, ghz(2), (1, 2), (2, 1))
    return relabel(psi, label)

if __name__ == '__main__':
    print ghz(0).nodes()
    print ghz(1).nodes()
    print fuse(ghz(0), ghz(1), (0, 2), (1, 0)).adj
    print microcluster("pete").nodes()

    g = GraphState()
    g.from_nx(microcluster("pete"))
    print g.to_stabilizer()

