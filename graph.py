"""
Provides an extremely basic graph structure, based on neighbour lists
"""

from collections import defaultdict
import clifford

def graph():
    """ Generate a graph with Hadamards on each qubit """
    #return defaultdict(set), defaultdict(lambda: clifford.by_name["hadamard"])
    return [set() for i in range(100)], [clifford.by_name["hadamard"] for i in range(100)]


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

def edgelist(g):
    """ Describe a graph as an edgelist """
    edges = frozenset(frozenset((i, n))
            for i, v in enumerate(g)
            for n in v)
    return [tuple(e) for e in edges]

