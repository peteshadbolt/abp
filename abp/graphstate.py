"""
This module implements Anders and Briegel's method for fast simulation of Clifford circuits.
"""

import itertools as it
import json, random
import qi, clifford, util


class GraphState(object):

    """
    This is the main class used to model stabilizer states.
    Internally it uses the same dictionary-of-dictionaries data structure as ``networkx``.
    """

    def __init__(self, nodes=[], deterministic=False):
        """ Construct a ``GraphState``

        :param nodes: An iterable of nodes used to construct the graph.
        :param deterministic: If ``True``, the behaviour of the graph is deterministic up to but not including the choice of measurement outcome. This is slightly less efficient, but useful for testing. If ``False``, the specific graph representation will sometimes be random -- of course, all possible representations still map to the same state vector.
        """

        self.adj, self.node = {}, {}
        self.add_nodes(nodes)
        self.deterministic = deterministic

    def add_node(self, node, **kwargs):
        """ Add a node.
        
        :param node: The name of the node, e.g. ``9``, ``start``
        :type node: Any hashable type
        :param kwargs: Any extra node attributes
            
        Example of using node attributes ::

            >>> g.add_node(0, label="fred", position=(1,2,3))
            >>> g.node[0]["label"]
            fred
            
        """
        assert not node in self.node, "Node {} already exists".format(v)
        self.adj[node] = {}
        self.node[node] = {"vop": clifford.by_name["hadamard"]}
        self.node[node].update(kwargs)

    def add_nodes(self, nodes):
        """ Add many nodes in one shot. """
        for n in nodes:
            self.add_node(n)

    def act_circuit(self, circuit):
        """ Run many gates in one call.

        :param circuit: An iterable containing tuples of the form ``(node, operation)``.  If ``operation`` is a name for a local operation (e.g. ``6``, ``hadamard``) then that operation is performed on ``node``.  If ``operation`` is ``cz`` then a CZ is performed on the two nodes in ``node``.

        Example (makes a Bell pair)::
            
            >>> g.act_circuit([(0, "hadamard"), (1, "hadamard"), ((0, 1), "cz")])

        """
        for node, operation in circuit:
            if operation == "cz":
                self.act_cz(*node)
            else:
                self.act_local_rotation(node, operation)

    def _add_edge(self, v1, v2, data={}):
        """ Add an edge between two vertices """
        self.adj[v1][v2] = data
        self.adj[v2][v1] = data

    def _del_edge(self, v1, v2):
        """ Delete an edge between two vertices """
        del self.adj[v1][v2]
        del self.adj[v2][v1]

    def has_edge(self, v1, v2):
        """ Test existence of an edge between two vertices  """
        return v2 in self.adj[v1]

    def _toggle_edge(self, v1, v2):
        """ Toggle an edge between two vertices  """
        if self.has_edge(v1, v2):
            self._del_edge(v1, v2)
        else:
            self._add_edge(v1, v2)

    def edgelist(self):
        """ Describe a graph as an edgelist # TODO: inefficient """
        edges = set(tuple(sorted((i, n)))
                    for i, v in self.adj.items()
                    for n in v)
        return tuple(edges)

    def remove_vop(self, a, avoid):
        """ Reduces VOP[a] to the identity """
        others = set(self.adj[a]) - {avoid}
        if self.deterministic:
            swap_qubit = min(others) if others else avoid
        else:
            swap_qubit = others.pop() if others else avoid

        for v in reversed(clifford.decompositions[self.node[a]["vop"]]):
            if v == "x":
                self.local_complementation(a, "U ->")
            else:
                self.local_complementation(swap_qubit, "V ->")

    def local_complementation(self, v, prefix=""):
        """ As defined in LISTING 1 of Anders & Briegel """
        for i, j in it.combinations(self.adj[v], 2):
            self._toggle_edge(i, j)

        self.node[v]["vop"] = clifford.times_table[
            self.node[v]["vop"], clifford.by_name["msqx_h"]]
        for i in self.adj[v]:
            self.node[i]["vop"] = clifford.times_table[
                self.node[i]["vop"], clifford.by_name["sqz_h"]]

    def act_local_rotation(self, node, operation):
        """ Act a local rotation on a qubit

        :param node: The index of the node to act on
        :param operation: The Clifford-group operation to perform.
        """
        rotation = clifford.by_name[str(operation)]
        self.node[node]["vop"] = clifford.times_table[
            rotation, self.node[node]["vop"]]

    def _update_vop(self, v, op):
        """ Update a VOP - only used internally"""
        rotation = clifford.by_name[str(op)]
        self.node[v]["vop"] = clifford.times_table[
            self.node[v]["vop"], rotation]

    def act_hadamard(self, qubit):
        """ Shorthand for ``self.act_local_rotation(qubit, "hadamard")`` """
        self.act_local_rotation(qubit, 10)

    def _lonely(self, a, b):
        """ Is this qubit _lonely ? """
        return len(self.adj[a]) > (b in self.adj[a])

    def act_cz(self, a, b):
        """ Act a controlled-phase gate on two qubits

        :param a: The first qubit
        :param b: The second qubit
        """
        if self._lonely(a, b):
            self.remove_vop(a, b)

        if self._lonely(b, a):
            self.remove_vop(b, a)

        if self._lonely(a, b) and not clifford.is_diagonal(self.node[a]["vop"]):
            self.remove_vop(a, b)

        edge = self.has_edge(a, b)
        va = self.node[a]["vop"]
        vb = self.node[b]["vop"]
        new_edge, self.node[a]["vop"], self.node[b]["vop"] = \
            clifford.cz_table[int(edge), va, vb]
        if new_edge != edge:
            self._toggle_edge(a, b)

    def measure(self, node, basis, force=None):
        """ Measure in an arbitrary basis 

        :param node: The name of the qubit to measure.
        :param basis: The basis in which to measure.
        :type basis: :math:`\in` ``{"px", "py", "pz"}``
        :param force: Measurements in quantum mechanics are probabilistic. If you want to force a particular outcome, use the ``force``.
        :type force: boolean
        
        """
        basis = clifford.by_name[basis]
        ha = clifford.conjugation_table[self.node[node]["vop"]]
        basis, phase = clifford.conjugate(basis, ha)

        # Flip a coin
        result = force if force != None else random.choice([0, 1])
        # Flip the result if we have negative phase
        if phase == -1:
            result = not result

        if basis == clifford.by_name["px"]:
            result = self._measure_x(node, result)
        elif basis == clifford.by_name["py"]:
            result = self._measure_y(node, result)
        elif basis == clifford.by_name["pz"]:
            result = self._measure_z(node, result)
        else:
            raise ValueError("You can only measure in {X,Y,Z}")

        # Flip the result if we have negative phase
        if phase == -1:
            result = not result

        return result

    def _toggle_edges(self, a, b):
        """ Toggle edges between vertex sets a and b """
        # TODO: i'm pretty sure this is just a single-line it.combinations or
        # equiv
        done = set()
        for i, j in it.product(a, b):
            if i != j and not (i, j) in done:
                done.add((i, j))
                done.add((j, i))
                self._toggle_edge(i, j)

    def _measure_x(self, node, result):
        """ Measure the graph in the X-basis """
        if len(self.adj[node]) == 0:
            return 0

        # Pick a vertex
        if self.deterministic:
            friend = sorted(self.adj[node].keys())[0]
        else:
            friend = next(self.adj[node].iterkeys())

        # Update the VOPs. TODO: pretty ugly
        if result:
            # Do a z on all ngb(vb) \ ngb(v) \ {v}, and some other stuff
            self._update_vop(friend, "msqy")
            self._update_vop(node, "pz")

            for n in set(self.adj[friend]) - set(self.adj[node]) - {node}:
                self._update_vop(n, "pz")
        else:
            # Do a z on all ngb(v) \ ngb(vb) \ {vb}, and sqy on the friend
            self._update_vop(friend, "sqy")
            for n in set(self.adj[node]) - set(self.adj[friend]) - {friend}:
                self._update_vop(n, "pz")

        # Toggle the edges. TODO: Yuk. Just awful!
        a = set(self.adj[node].keys())
        b = set(self.adj[friend].keys())
        self._toggle_edges(a, b)
        intersection = a & b
        for i, j in it.combinations(intersection, 2):
            self._toggle_edge(i, j)

        for n in a - {friend}:
            self._toggle_edge(friend, n)

        return result

    def _measure_y(self, node, result):
        """ Measure the graph in the Y-basis """
        # Do some rotations
        for neighbour in self.adj[node]:
            self._update_vop(neighbour, "sqz" if result else "msqz")

        # A sort of local complementation
        vngbh = set(self.adj[node]) | {node}
        for i, j in it.combinations(vngbh, 2):
            self._toggle_edge(i, j)

        self._update_vop(node, 5 if result else 6)
                         # TODO: naming: # lcoS.herm_adjoint() if result else
                         # lcoS
        return result

    def _measure_z(self, node, result):
        """ Measure the graph in the Z-basis """
        # Disconnect
        for neighbour in tuple(self.adj[node]):
            self._del_edge(node, neighbour)
            if result:
                self._update_vop(neighbour, "pz")

        # Rotate
        if result:
            self._update_vop(node, "px")
            self._update_vop(node, "hadamard")
        else:
            self._update_vop(node, "hadamard")

        return result

    def order(self):
        """ Get the number of qubits """
        return len(self.node)

    def __str__(self):
        """ Represent as a string for quick debugging """
        s = ""
        for key in sorted(self.node.keys()):
            s += "{}:  {}\t".format(
                key, clifford.get_name(self.node[key]["vop"]).replace("YC", "-"))
            if self.adj[key]:
                s += str(tuple(self.adj[key].keys())).replace(" ", "")
            else:
                s += "-"
            s += "\n"

        return s

    def to_json(self, stringify=False):
        """ Convert the graph to JSON-like form.
        
        :param stringify: JSON keys must be strings, But sometimes it is useful to have a JSON-like object whose keys are tuples.

        If you want to dump a graph do disk, do something like this::
            
            >>> import json
            >>> with open("graph.json") as f:
                    json.dump(graph.to_json(True), f)

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
        """ Get the full state vector corresponding to this stabilizer state. Useful for debugging, interface with other simulators.

        The output state is represented as a ``abp.qi.CircuitModel``::
        
            >>> print g.to_state_vector()
            |00000>: 0.18+0.00j
            |00001>: 0.18+0.00j ...
        
        .. warning::
            Obviously this method becomes very slow for more than about ten qubits!

        """
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
        """ Get the stabilizer tableau.  Work in progress!
        """
        return
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
        """ Check equality between GraphStates """
        return self.adj == other.adj and self.node == other.node

if __name__ == '__main__':
    g = GraphState()
    g.add_nodes(range(10))
    g._add_edge(0, 5)
    g.act_local_rotation(6, 10)
    print g
    print g.to_state_vector()
