"""
Provides an extremely basic graph structure, based on neighbour lists
"""

from collections import defaultdict
import itertools as it
import clifford
import json
try:
    import networkx as nx
except ImportError:
    print "Could not import networkx: layout will not work"


class GraphState(object):

    def __init__(self):
        self.ngbh = defaultdict(set)
        self.vops = defaultdict(int)
        self.meta = defaultdict(dict)

    def add_vertex(self, v):
        """ Add a vertex if it doesn't already exist """
        if not v in self.ngbh:
            self.ngbh[v] = set()
            self.vops[v] = clifford.by_name["hadamard"]

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

        # Update VOPs: TODO check ordering and replace by self.act_local_rotation
        self.vops[v] = clifford.times_table[
            self.vops[v]][clifford.by_name["sqx"]]
        for i in self.ngbh[v]:
            self.vops[i] = clifford.times_table[
                self.vops[i]][clifford.by_name["msqz"]]

    def act_local_rotation(self, a, op):
        """ Act a local rotation """
        self.vops[a] = clifford.times_table[op,self.vops[a]]

    def act_cz(self, a, b):
        """ Act a controlled-phase gate on two qubits """
        if self.ngbh[a] - {b}:
            self.remove_vop(a, b)
        if self.ngbh[b] - {a}:
            self.remove_vop(b, a)
        if self.ngbh[a] - {b}:
            self.remove_vop(a, b)
        edge = self.has_edge(a, b)
        new_edge, self.vops[a], self.vops[b] = clifford.cz_table[edge, self.vops[a], self.vops[b]]
        if new_edge != edge:
            self.toggle_edge(a, b)

    def __str__(self):
        """ Represent as a string for quick debugging """
        return "graph:\n vops: {}\n ngbh: {}\n"\
                .format(str(dict(self.vops)), str(dict(self.ngbh)))

    def to_json(self):
        """ Convert the graph to JSON form """
        ngbh = {key: tuple(value) for key, value in self.ngbh.items()}
        meta = {key: value for key, value in self.meta.items()}
        return json.dumps({"vops": self.vops, "ngbh": ngbh, "meta": meta})

    def to_networkx(self):
        """ Convert the graph to a networkx graph """
        g = nx.Graph()
        g.edge = {node: {neighbour: {} for neighbour in neighbours} 
                for node, neighbours in self.ngbh.items()}
        g.node = {node: {"vop": vop} for node, vop in self.vops.items()}
        for node, metadata in self.meta.items():
            g.node[node].update(metadata)
        return g

    def layout(self):
        """ Automatically lay out the graph """
        g = self.to_networkx()
        pos = nx.spring_layout(g, dim=3, scale=10)
        for key, (x, y, z) in pos.items():
            self.meta[key]["pos"] = {"x": round(x, 0), "y": round(y, 0), "z": round(z, 0)}

        
