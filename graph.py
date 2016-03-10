import networkx as nx
from matplotlib import pyplot as plt

vop_colors = ["red", "green", "blue"]

def graph(n):
    """ Generate a graph with Hadamards on each qubit """
    graph = [set() for i in xrange(n)]
    vops = [0 for i in xrange(n)]
    return graph, vops # TODO: seems ugly

def add_edge(graph, v1, v2):
    """ Add an edge between two vertices in the graph """
    graph[v1].add(v2)
    graph[v2].add(v1)

def del_edge(graph, v1, v2):
    """ Delete an edge between two vertices in the graph """
    graph[v1].remove(v2)
    graph[v2].remove(v1)

def has_edge(graph, v1, v2):
    """ Test existence of an edge between two vertices in the graph """
    return v2 in graph[v1]

def toggle_edge(graph, v1, v2):
    """ Toggle an edge between two vertices in the graph """
    if has_edge(graph, v1, v2):
        del_edge(graph, v1, v2)
    else:
        add_edge(graph, v1, v2)

def edgelist(graph):
    """ Describe a graph as an edgelist """
    edges = frozenset(frozenset((i, n))
            for i, v in enumerate(graph)
            for n in v)
    return [tuple(e) for e in edges]

def draw(graph, vops, filename="out.pdf", ns=500):
    """ Draw a graph with networkx layout """
    g = nx.from_edgelist(edgelist(graph))
    pos = nx.spring_layout(g)
    colors = [vop_colors[vop] for vop in vops]
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
