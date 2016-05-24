"""
Provides an extremely basic graph structure, based on neighbour lists
"""

import itertools as it
import json
import qi, clifford, util
import random

output = open("debug_pete.txt", "w")
def debug(x):
    output.write(str(x)+"\n")

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

    def add_edge(self, v1, v2, data = {}):
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
        debug("deling edge")
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
        # TODO: sucks!
        others = set(self.adj[a]) - {avoid}
        swap_qubit = others.pop() if others else avoid

        debug("remove_byprod_op called: (v, avoid, vb):")
        self.print_adj_list_line(a)
        self.print_adj_list_line(avoid)
        self.print_adj_list_line(swap_qubit)
        converted = clifford.decompositions[self.node[a]["vop"]]
        converted = "".join("U" if x == "x" else "V" for x in converted)
        debug("using {}".format(converted))

        for v in reversed(clifford.decompositions[self.node[a]["vop"]]):
            if v == "x":
                self.local_complementation(a, "U ->")
            else:
                self.local_complementation(swap_qubit, "V ->")

        assert self.node[a]["vop"]==0

        debug("remove_byprod_op: after (v, avoid, vb):")
        self.print_adj_list_line(a)
        self.print_adj_list_line(avoid)
        self.print_adj_list_line(swap_qubit)

        assert self.node[a]["vop"] == 0

    def local_complementation(self, v, prefix = ""):
        """ As defined in LISTING 1 of Anders & Briegel """
        debug("{}Inverting about {}".format(prefix, self.get_adj_list_line(v)))
        for i, j in it.combinations(self.adj[v], 2):
            self.toggle_edge(i, j)

        msqx_h = clifford.conjugation_table[clifford.by_name["msqx"]]
        sqz_h = clifford.conjugation_table[clifford.by_name["sqz"]]
        self.node[v]["vop"] = clifford.times_table[self.node[v]["vop"], msqx_h]
        for i in self.adj[v]:
            self.node[i]["vop"] = clifford.times_table[self.node[i]["vop"], sqz_h]

    def act_local_rotation(self, v, op):
        """ Act a local rotation """
        rotation = clifford.by_name[str(op)]
        self.node[v]["vop"] = clifford.times_table[rotation, self.node[v]["vop"]]

    def act_hadamard(self, qubit):
        """ Shorthand """
        self.act_local_rotation(qubit, 10)

    def act_cz(self, a, b):
        """ Act a controlled-phase gate on two qubits """
        debug("before cphase between {} and {}".format(a, b))
        self.print_adj_list_line(a)
        self.print_adj_list_line(b)

        ci = self.get_connection_info(a, b)
        if ci["non1"]:
            debug("cphase: left vertex has NONs -> putting it to Id")
            self.remove_vop(a, b)

        ci = self.get_connection_info(a, b)
        if ci["non2"]:
            debug("cphase: right vertex has NONs -> putting it to Id")
            self.remove_vop(b, a)

        ci = self.get_connection_info(a, b)
        if ci["non1"] and not clifford.is_diagonal(self.node[a]["vop"]):
            debug("cphase: left one needs treatment again -> putting it to Id")
            self.remove_vop(a, b)

        self.cz_with_table(a, b)

    def get_connection_info(self, a, b):
        if self.has_edge(a, b):
            return {"was_edge": True,
                    "non1": len(self.adj.get(a)) > 1,
                    "non2": len(self.adj.get(b)) > 1}
        else:
            return {"was_edge": False,
                    "non1": len(self.adj.get(a)) > 0,
                    "non2": len(self.adj.get(b)) > 0}

    def cz_with_table(self, a, b):
        """ Run the table """
        debug("cphase_with_table called on:")
        self.print_adj_list_line(a)
        self.print_adj_list_line(b)

        ci = self.get_connection_info(a, b)
        try:
            assert ci["non1"]==False or clifford.is_diagonal(self.node[a]["vop"])
            assert ci["non2"]==False or clifford.is_diagonal(self.node[b]["vop"])
        except AssertionError:
            debug(ci)
            debug(self.node[a]["vop"])
            debug(self.node[b]["vop"])
            
        edge = self.has_edge(a, b)
        new_edge, self.node[a]["vop"], self.node[
            b]["vop"] = clifford.cz_table[edge, self.node[a]["vop"], self.node[b]["vop"]]
        if new_edge != edge:
            self.toggle_edge(a, b)

        debug("cphase_with_table: after")
        self.print_adj_list_line(a)
        self.print_adj_list_line(b)

        ci = self.get_connection_info(a, b)
        assert ci["non1"]==False or clifford.is_diagonal(self.node[a]["vop"])
        assert ci["non2"]==False or clifford.is_diagonal(self.node[b]["vop"])

    def measure_z(self, node, force=None):
        """ Measure the graph in the Z-basis """
        res = force if force!=None else random.choice([0, 1])

        # Disconnect
        for neighbour in self.adj[node]:
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
        return len(self.node)

    def __str__(self):
        """ Represent as a string for quick debugging """
        node = {key: clifford.get_name(value["vop"])
                  for key, value in self.node.items()}
        nbstr = str(self.adj)
        return "graph:\n node: {}\n adj: {}\n".format(node, nbstr)

    def to_json(self):
        """ Convert the graph to JSON form """
        return {"node": self.node, "adj": self.adj}

    def from_json(self, data):
        """ Reconstruct from JSON """
        self.__init__([])
        #TODO

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
        output = {a:{} for a in self.node}
        for a, b in it.product(self.node, self.node):
            if a == b:
                output[a][b] = "X"
            elif a in self.adj[b]:
                output[a][b] = "Z"
            else:
                output[a][b] = "I"
        return output

    def adj_list(self):
        """ For comparison with Anders and Briegel's C++ implementation """
        rows = []
        for key, node in self.node.items():
            adj = " ".join(map(str, sorted(self.adj[key])))
            vop = clifford.get_name(node["vop"])
            s = "Vertex {}: VOp {}, neighbors {}".format(key, vop, adj)
            rows.append(s)
        return " \n".join(rows) + " \n"

    def get_adj_list_line(self, key):
        """ TODO: delete """
        node = self.node[key]
        adj = " ".join(map(str, sorted(self.adj[key])))
        vop = clifford.get_name(node["vop"])
        s = "Vertex {}: VOp {}, neighbors {}".format(key, vop, adj)
        return s

    def print_adj_list_line(self, key):
        debug(self.get_adj_list_line(key))


    def __eq__(self, other):
        """ Check equality between graphs """
        return self.adj == other.adj and self.node == other.node

