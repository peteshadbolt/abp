"""
Provides an extremely basic graph structure, based on neighbour lists
"""

from collections import defaultdict
import itertools as it
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

def cphase(g, vops, a, b):
    """ Act a controlled-phase gate on two qubits """
    if g[a]-{b}: remove_vop(g, vops, a, b)
    if g[b]-{a}: remove_vop(g, vops, b, a)
    if g[a]-{b}: remove_vop(g, vops, a, b)
    edge = has_edge(g, a, b)
    new_edge, vops[a], vops[b] = cphase_table[edge, vops[a], vops[b]]
    if new_edge != edge:
        toggle_edge(g, a, b)
    

def remove_vop(g, vops, a, avoid):
    """ Reduces VOP[a] to the identity, avoiding (if possible) the use of vertex b as a swapping partner """
    others = g[a] - {avoid}
    swap_qubit = others.pop() if others else avoid
    for v in reversed(clifford.decompositions[vops[a]]):
        local_complementation(g, vops, a if v == "x" else swap_qubit)


def local_complementation(g, vops, v):
    """ As defined in LISTING 1 of Anders & Briegel """
    for i, j in it.combinations(g[v], 2):
        toggle_edge(g, i, j)

    # Update VOPs
    vops[v] = clifford.times_table[vops[v]][clifford.by_name["sqx"]]
    for i in g[v]:
        vops[i] = clifford.times_table[vops[i]][clifford.by_name["msqz"]]

