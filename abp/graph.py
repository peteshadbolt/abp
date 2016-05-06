"""
Provides an extremely basic graph structure, based on neighbour lists
"""

from collections import defaultdict
import itertools as it
import clifford


class GraphState(object):

    def __init__(self):
        self.ngbh = defaultdict(set)
        self.vops = defaultdict(int)

    def add_edge(self, v1, v2):
        """ Add an edge between two vertices in the self """
        if not v1 in self.ngbh:
            self.vops[v1] = clifford.by_name["hadamard"]
        if not v2 in self.ngbh:
            self.vops[v2] = clifford.by_name["hadamard"]
        self.ngbh[v1].add(v2)
        self.ngbh[v2].add(v1)

    def del_edge(self, v1, v2):
        """ Delete an edge between two vertices in the self """
        self.ngbh[v1].remove(v2)
        self.ngbh[v2].remove(v1)

    def has_edge(self, v1, v2):
        """ Test existence of an edge between two vertices in the self """
        return v2 in self.ngbh[v1]

    def toggle_edge(self, v1, v2):
        """ Toggle an edge between two vertices in the self """
        if self.has_edge(v1, v2):
            self.del_edge(v1, v2)
        else:
            self.add_edge(v1, v2)

    def edgelist(self):
        """ Describe a graph as an edgelist """
        edges = frozenset(tuple(sorted((i, n)))
                          for i, v in self.ngbh.items()
                          for n in v)
        return [tuple(e) for e in edges]

    def remove_vop(self, a, avoid):
        """ Reduces VOP[a] to the identity """
        others = self.ngbh[a] - {avoid}
        swap_qubit = others.pop() if others else avoid
        for v in reversed(clifford.decompositions[self.vops[a]]):
            self.local_complementation(a if v == "x" else swap_qubit)

    def local_complementation(self, v):
        """ As defined in LISTING 1 of Anders & Briegel """
        for i, j in it.combinations(self.ngbh[v], 2):
            self.toggle_edge(i, j)

        # Update VOPs
        self.vops[v] = clifford.times_table[
            self.vops[v]][clifford.by_name["sqx"]]
        for i in self.ngbh[v]:
            self.vops[i] = clifford.times_table[
                self.vops[i]][clifford.by_name["msqz"]]

    def cphase(self, a, b):
        """ Act a controlled-phase gate on two qubits """
        if self.ngbh[a] - {b}:
            self.remove_vop(a, b)
        if self.ngbh[b] - {a}:
            self.remove_vop(b, a)
        if self.ngbh[a] - {b}:
            self.remove_vop(a, b)
        edge = self.has_edge(a, b)
        new_edge, vops[a], vops[b] = cphase_table[edge, vops[a], vops[b]]
        if new_edge != edge:
            self.toggle_edge(a, b)

