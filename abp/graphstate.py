"""
Provides an extremely basic graph structure, based on key/value pairs
"""

import itertools as it
import json
import qi, clifford, util
import random

class GraphState(object):

    def __init__(self, nodes=[]):
        self.adj, self.node = {}, {}
        self.add_nodes(nodes)

    def add_node(self, v, **kwargs):
        """ Add a node """
        assert not v in self.node
        self.adj[v] = {}
        self.node[v] = {"vop": clifford.by_name["hadamard"]}
        self.node[v].update(kwargs)

    def add_nodes(self, nodes):
        """ Add a buncha nodes """
        for n in nodes:
            self.add_node(n)

    def add_edge(self, v1, v2, data={}):
        """ Add an edge between two vertices in the self """
        assert v1 != v2
        self.adj[v1][v2] = data
        self.adj[v2][v1] = data

    def add_edges(self, edges):
        """ Add a buncha edges """
        for (v1, v2) in edges:
            self.add_edge(v1, v2)

    def del_edge(self, v1, v2):
        """ Delete an edge between two vertices in the self """
        del self.adj[v1][v2]
        del self.adj[v2][v1]

    def has_edge(self, v1, v2):
        """ Test existence of an edge between two vertices in the self """
        return v2 in self.adj[v1]

    def toggle_edge(self, v1, v2):
        """ Toggle an edge between two vertices in the self """
        if self.has_edge(v1, v2):
            self.del_edge(v1, v2)
        else:
            self.add_edge(v1, v2)

    def edgelist(self):
        """ Describe a graph as an edgelist """
        # TODO: inefficient
        edges = set(tuple(sorted((i, n)))
                    for i, v in self.adj.items()
                    for n in v)
        return tuple(edges)

    def remove_vop(self, a, avoid):
        """ Reduces VOP[a] to the identity """
        others = set(self.adj[a]) - {avoid}
        swap_qubit = others.pop() if others else avoid

        for v in reversed(clifford.decompositions[self.node[a]["vop"]]):
            if v == "x":
                self.local_complementation(a, "U ->")
            else:
                self.local_complementation(swap_qubit, "V ->")

    def local_complementation(self, v, prefix=""):
        """ As defined in LISTING 1 of Anders & Briegel """
        for i, j in it.combinations(self.adj[v], 2):
            self.toggle_edge(i, j)

        self.node[v]["vop"] = clifford.times_table[
            self.node[v]["vop"], clifford.by_name["msqx_h"]]
        for i in self.adj[v]:
            self.node[i]["vop"] = clifford.times_table[
                self.node[i]["vop"], clifford.by_name["sqz_h"]]

    def act_local_rotation(self, v, op):
        """ Act a local rotation """
        rotation = clifford.by_name[str(op)]
        self.node[v]["vop"] = clifford.times_table[
            rotation, self.node[v]["vop"]]

    def act_hadamard(self, qubit):
        """ Shorthand """
        self.act_local_rotation(qubit, 10)

    def lonely(self, a, b):
        """ Is this qubit lonely ? """
        return len(self.adj[a]) > (b in self.adj[a])

    def act_cz(self, a, b):
        """ Act a controlled-phase gate on two qubits """
        if self.lonely(a, b):
            self.remove_vop(a, b)

        if self.lonely(b, a):
            self.remove_vop(b, a)

        if self.lonely(a, b) and not clifford.is_diagonal(self.node[a]["vop"]):
            self.remove_vop(a, b)

        edge = self.has_edge(a, b)
        va = self.node[a]["vop"]
        vb = self.node[b]["vop"]
        new_edge, self.node[a]["vop"], self.node[b]["vop"] = \
            clifford.cz_table[edge, va, vb]
        if new_edge != edge:
            self.toggle_edge(a, b)

    def measure(self, node, basis):
        """ Measure in an arbitrary basis """
        basis = clifford.by_name[basis]
        ha = clifford.conjugation_table[self.node[node]["vop"]]
        basis, phase = clifford.conjugate(basis, ha)

        if basis == clifford.by_name["px"]:
            result = self.measure_x(node)
        elif basis == clifford.by_name["py"]:
            result = self.measure_y(node)
        elif basis == clifford.by_name["pz"]:
            result = self.measure_z(node)
        else:
            raise ValueError("You can only measure in {X,Y,Z}")

        # Flip the result if we have negative phase
        if phase == -1:
            result = not result

        return result

    def toggle_edges(a, b):
        """ Toggle edges between vertex sets a and b """
        done = {}
        for i, j in it.product(a, b):
            if i == j and not (i, j) in done:
                done.add((i, j), (j, i))
                self.toggle_edge(i, j)

    def measure_x(self, node, result=0):
        """ Measure the graph in the X-basis """
        if len(self.adj[node]) == 0:
            return 0

        result = random.choice([0, 1])

        # Pick a vertex
        friend = next(self.adj[node].iterkeys())

        # TODO: yuk yuk yuk
        if result:
            # Do a z on all ngb(vb) \ ngb(v) \ {v}, and some other stuff
            self.act_local_rotation(node, "pz")
            self.act_local_rotation(friend, "msqy")
            for n in set(self.adj[friend]) - set(self.adj(node)) - {node}:
                self.act_local_rotation(n, "pz")
        else:
            # Do a z on all ngb(v) \ ngb(vb) \ {vb}, and sqy on the friend
            self.act_local_rotation(friend, "sqy")
            for n in set(self.adj[node]) - set(self.adj(friend)) - {friend}:
                self.act_local_rotation(n, "pz")

        # TODO: Yuk. Just awful!
        a = set(self.adj[node].keys())
        b = set(self.adj[friend].keys())
        self.toggle_edges(a, b)
        intersection = a & b
        for i, j in it.combinations(intersection, 2):
            self.toggle_edge(i, j)

        for n in a - {friend}:
            self.toggle_edge(friend, n)

        return result

    def measure_y(self, node, result=None):
        """ Measure the graph in the Y-basis """

        result = random.choice([0, 1])

        # Do some rotations
        for neighbour in self.adj[node]:
            # NB: should these be hermitian_conjugated?
            self.act_local_rotation(neighbour, "sqz" if result else "msqz")

        # A sort of local complementation
        vngbh = set(self.adj[node]) | {node}
        for i, j in it.combinations(vngbh, 2):
            self.toggle_edge(i, j)

        self.act_local_rotation(node, "msqz" if result else "msqz_h")
        return result

    def measure_z(self, node, result=None):
        """ Measure the graph in the Z-basis """

        result = random.choice([0, 1])

        # Disconnect
        for neighbour in self.adj[node]:
            self.del_edge(node, neighbour)
            if result:
                self.act_local_rotation(neighbour, "pz")

        # Rotate
        if result:
            self.act_local_rotation(node, "px")

        self.act_local_rotation(node, "hadamard")
        return result

    def order(self):
        """ Get the number of qubits """
        return len(self.node)

    def __str__(self):
        """ Represent as a string for quick debugging """
        node = {key: clifford.get_name(value["vop"])
                for key, value in self.node.items()}
        nbstr = str(self.adj)
        return "graph:\n node: {}\n adj: {}\n".format(node, nbstr)

    def to_json(self, stringify=False):
        """
        Convert the graph to JSON form.
        JSON keys must be strings, But sometimes it is useful to have
        a JSON-like object whose keys are tuples!
        """
        if stringify:
            node = {str(key): value for key, value in self.node.items()}
            adj = {str(key): {str(key): value for key, value in ngbh.items()}
                   for key, ngbh in self.adj.items()}
            return {"node": node, "adj": adj}
        else:
            return {"node": self.node, "adj": self.adj}

    def from_json(self, data):
        """ Reconstruct from JSON """
        self.__init__([])
        # TODO

    def to_state_vector(self):
        """ Get the full state vector """
        if len(self.node) > 15:
            raise ValueError("Cannot build state vector: too many qubits")
        state = qi.CircuitModel(len(self.node))
        for i in range(len(self.node)):
            state.act_hadamard(i)
        for i, j in self.edgelist():
            state.act_cz(i, j)
        for i, n in self.node.items():
            state.act_local_rotation(i, clifford.unitaries[n["vop"]])
        return state

    def to_stabilizer(self):
        """ Get the stabilizer of this graph """
        output = {a: {} for a in self.node}
        for a, b in it.product(self.node, self.node):
            if a == b:
                output[a][b] = "X"
            elif a in self.adj[b]:
                output[a][b] = "Z"
            else:
                output[a][b] = "I"
        # TODO: signs
        return output

    def __eq__(self, other):
        """ Check equality between graphs """
        return self.adj == other.adj and self.node == other.node

