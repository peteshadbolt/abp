"""
Provides an extremely basic graph structure, based on neighbour lists
"""

import itertools as it
import clifford
import json
import qi

try:
    import networkx as nx
except ImportError:
    print "Could not import networkx."


class GraphState():

    def __init__(self, nodes=[]):
        self.ngbh, self.vops, self.meta = {}, {}, {}
        self.add_nodes(nodes)

    def add_node(self, v, meta={}):
        """ Add a node """
        self.ngbh[v] = set()
        self.vops[v] = clifford.by_name["hadamard"]
        self.meta[v] = meta

    def add_nodes(self, nodes):
        """ Add a buncha nodes """
        for n in nodes:
            self.add_node(n)

    def add_edge(self, v1, v2):
        """ Add an edge between two vertices in the self """
        assert v1 != v2
        self.ngbh[v1].add(v2)
        self.ngbh[v2].add(v1)

    def add_edges(self, edges):
        """ Add a buncha edges """
        for (v1, v2) in edges:
            self.add_edge(v1, v2)

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
        edges = set(tuple(sorted((i, n)))
                          for i, v in self.ngbh.items()
                          for n in v)
        return tuple(edges)

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

        msqx_h = clifford.conjugation_table[clifford.by_name["msqx"]]
        sqz_h = clifford.conjugation_table[clifford.by_name["sqz"]]
        self.vops[v] = clifford.times_table[self.vops[v], msqx_h]
        for i in self.ngbh[v]:
            self.vops[i] = clifford.times_table[self.vops[i], sqz_h]

    def act_local_rotation(self, v, op):
        """ Act a local rotation """
        rotation = clifford.by_name[str(op)]
        self.vops[v] = clifford.times_table[rotation, self.vops[v]]

    def act_hadamard(self, qubit):
        """ Shorthand """
        self.act_local_rotation(qubit, 10)

    def act_cz(self, a, b):
        """ Act a controlled-phase gate on two qubits """
        if self.ngbh[a] - {b}:
            self.remove_vop(a, b)
        if self.ngbh[b] - {a}:
            self.remove_vop(b, a)
        if self.ngbh[a] - {b}:
            self.remove_vop(a, b)
        edge = self.has_edge(a, b)
        new_edge, self.vops[a], self.vops[
            b] = clifford.cz_table[edge, self.vops[a], self.vops[b]]
        if new_edge != edge:
            self.toggle_edge(a, b)

    def measure_z(self, node, force=None):
        """ Measure the graph in the Z-basis """
        res = force if force else np.random.choice([0, 1])

        # Disconnect
        for neighbour in self.ngbh[node]:
            self.del_edge(node, neighbour)
            if res:
                self.act_local_rotation(neighbour, "pz")

        # Rotate
        if res:
            self.act_local_rotation(node, "px")
            self.act_local_rotation(node, "hadamard")
        else:
            self.act_local_rotation(node, "hadamard")

        return res

    def measure_x(self, i):
        """ Measure the graph in the X-basis """
        # TODO
        pass

    def measure_y(self, i):
        """ Measure the graph in the Y-basis """
        # TODO
        pass

    def order(self):
        """ Get the number of qubits """
        return len(self.vops)

    def __str__(self):
        """ Represent as a string for quick debugging """
        vopstr = {key: clifford.get_name(value)
                  for key, value in self.vops.items()}
        nbstr = str(self.ngbh)
        return "graph:\n vops: {}\n ngbh: {}\n".format(vopstr, nbstr)

    def to_json(self):
        """ Convert the graph to JSON form """
        meta = {key: value for key, value in self.meta.items()}
        edge = self.edgelist()
        return {"nodes": self.vops, "edges": edge, "meta": meta}

    def from_json(self, data):
        """ Reconstruct from JSON """
        self.__init__([])
        self.vops = {int(key): value for key, value in data["nodes"].items()}
        self.meta = {int(key): value for key, value in data["meta"].items()}
        self.ngbh = {int(key): set() for key in self.vops}
        self.add_edges(data["edges"])

    def to_networkx(self):
        """ Convert the graph to a networkx graph """
        g = nx.Graph()
        g.edge = {node: {neighbour: {} for neighbour in neighbours}
                  for node, neighbours in self.ngbh.items()}
        g.node = {node: {"vop": vop} for node, vop in self.vops.items()}
        for node, metadata in self.meta.items():
            g.node[node].update(metadata)
        return g

    def to_state_vector(self):
        """ Get the full state vector """
        if len(self.vops) > 15:
            raise ValueError("Cannot build state vector: too many qubits")
        state = qi.CircuitModel(len(self.vops))
        for i in range(len(self.vops)):
            state.act_hadamard(i)
        for i, j in self.edgelist():
            state.act_cz(i, j)
        for i, u in self.vops.items():
            state.act_local_rotation(i, clifford.unitaries[u])
        return state

    def layout(self):
        """ Automatically lay out the graph """
        if self.order() == 0:
            return
        g = self.to_networkx()
        pos = nx.spring_layout(g, dim=3, scale=10)
        average = lambda axis: sum(p[axis]
                                   for p in pos.values()) / float(len(pos))
        ax, ay, az = average(0), average(1), average(2)
        for key, (x, y, z) in pos.items():
            self.meta[key]["pos"] = {
                "x": x - ax,
                "y": y - ay,
                "z": z - az}

    def to_stabilizer(self):
        """ Get the stabilizer of this graph """
        # TODO: VOPs are not implemented yet
        output = ""
        for a in self.ngbh:
            for b in self.ngbh:
                if a == b:
                    output += " X "
                elif a in self.ngbh[b]:
                    output += " Z "
                else:
                    output += " I "
            output += "\n"
        return output

    def adj_list(self):
        """ For comparison with Anders and Briegel's C++ implementation """
        rows = []
        for key, vop in self.vops.items():
            ngbh = " ".join(map(str, sorted(self.ngbh[key])))
            vop = clifford.get_name(vop)
            s = "Vertex {}: VOp {}, neighbors {}".format(key, vop, ngbh)
            rows.append(s)
        return " \n".join(rows) + " \n"

    def __eq__(self, other):
        """ Check equality between graphs """
        return self.ngbh == other.ngbh and self.vops == other.vops



