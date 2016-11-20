#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module implements Anders and Briegel's method for fast simulation of Clifford circuits.
"""

import itertools as it
import json, random
import qi, clifford, util
import abp
from stabilizer import Stabilizer


class GraphState(object):

    """
    This is the main class used to model stabilizer states.
    Internally it uses the same dictionary-of-dictionaries data structure as ``networkx``.
    """

    def __init__(self, data=(), vop="identity"):
        """ Construct a ``GraphState``

        :param data: An iterable of nodes used to construct the graph, or an integer -- the number of nodes, or a ``nx.Graph``.
        :param vop: The default VOP for new qubits. Setting ``vop="identity"`` initializes qubits in :math:`|+\\rangle`. Setting ``vop="hadamard"`` initializes qubits in :math:`|0\\rangle`.
        """

        self.adj, self.node = {}, {}
        try:
            # Cloning from a networkx graph
            self.adj = data.adj.copy()
            self.node = data.node.copy()
            for key, value in self.node.items():
                self.node[key]["vop"] = data.node[
                    key].get("vop", clifford.identity)
        except AttributeError:
            try:
                # Provided with a list of node names?
                for n in data:
                    self._add_node(n, vop=vop)
            except TypeError:
                # Provided with an integer?
                for n in range(data):
                    self._add_node(n, vop=vop)

    def add_node(self, *args, **kwargs):
        """ Add a node """
        self._add_node(self, *args, **kwargs)

    def _del_node(self, node):
        """ Remove a node. TODO: this is a hack right now. """
        if not node in self.node:
            return
        del self.node[node]
        for k in self.adj[node]:
            del self.adj[k][node]
        del self.adj[node]

    def del_qubit(self, node):
        """ Remove a qubit. TODO: this is a hack right now. """
        self._del_node(node)

    def _add_node(self, node, **kwargs):
        """ Add a node. 

        By default, nodes are initialized with ``vop=``:math:`I`, i.e. they are in the :math:`|+\\rangle` state.
        """
        if node in self.node:
            print "Warning: node {} already exists".format(node)
            return

        default = kwargs.get("default", "identity")
        self.adj[node] = {}
        self.node[node] = {}
        kwargs["vop"] = clifford.by_name[
            str(kwargs.get("vop", "identity"))]  # TODO: ugly
        self.node[node].update(kwargs)

    def add_qubit(self, name, **kwargs):
        """ Add a qubit to the state.

        :param name: The name of the node, e.g. ``9``, ``start``.
        :type name: Any hashable type
        :param kwargs: Any extra node attributes

        By default, qubits are initialized in the :math:`|0\\rangle` state. Provide the optional ``vop`` argument to set the initial state.

        Example of using node attributes ::

            >>> g._add_node(0, label="fred", position=(1,2,3))
            >>> g.node[0]["label"]
            fred 

        """
        kwargs["vop"] = clifford.by_name[
            str(kwargs.get("vop", "hadamard"))]  # TODO: ugly
        self._add_node(name, **kwargs)

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

    def act_czs(self, *pairs):
        """ Shorthand to act many CZs """
        for a, b in pairs:
            self.act_cz(a, b)

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

    def remove_vop(self, node, avoid):
        """ Attempts to remove the vertex operator on a particular qubit.

        :param node: The node whose vertex operator should be reduced to the identity.
        :param avoid: We will try to leave this node alone during the process (if possible).

        """
        others = set(self.adj[node]) - {avoid}
        if abp.DETERMINISTIC:
            swap_qubit = min(others) if others else avoid
        else:
            swap_qubit = others.pop() if others else avoid

        for v in reversed(clifford.decompositions[self.node[node]["vop"]]):
            if v == "x":
                self.local_complementation(node)
            else:
                self.local_complementation(swap_qubit)

    def local_complementation(self, v):
        """ As defined in LISTING 1 of Anders & Briegel """
        for i, j in it.combinations(self.adj[v], 2):
            self._toggle_edge(i, j)

        self.node[v]["vop"] = clifford.times_table[
            self.node[v]["vop"], clifford.msqx_h]
        for i in self.adj[v]:
            self.node[i]["vop"] = clifford.times_table[
                self.node[i]["vop"], clifford.sqz_h]

    def act_local_rotation(self, node, operation):
        """ Act a local rotation on a qubit

        :param node: The index of the node to act on
        :param operation: The Clifford-group operation to perform. You can use any of the names in the :ref:`Clifford group alias table <clifford>`.
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

    def measure(self, node, basis, force=None, detail=False, friend=None):
        """ Measure in an arbitrary basis

        :param node: The name of the qubit to measure.
        :param basis: The basis in which to measure.
        :param friend: Specify a node to toggle about when performing an :math:`X` measurement.
        :type friend: Any neighbour of ``node``.
        :type basis: :math:`\in` ``{"px", "py", "pz"}``
        :param force: Forces the measurement outcome.
        :type force: boolean
        :param detail: Get detailed information.
        :type detail: boolean

        Measurements in quantum mechanics are probabilistic. If you want to force a particular outcome :math:`\in\{0, 1\}`, use ``force``.

        You can get more information by setting ``detail=True``, in which case ``measure()`` returns a dictionary with the following keys:

        - ``outcome``: the measurement outcome.
        - ``determinate``: indicates whether the outcome was determinate or random. For example, measuring :math:`|0\\rangle`  in :math:`\sigma_x` always gives a deterministic outcome. ``determinate`` is overridden by ``force`` -- forced outcomes are always determinate.
        - ``conjugated_basis``: The index of the measurement operator, rotated by the vertex operator of the measured node, i.e. :math:`U_\\text{vop} \sigma_m U_\\text{vop}^\dagger`.
        - ``phase``: The phase of the cojugated basis, :math:`\pm 1`.
        - ``node``: The name of the measured node.
        - ``force``: The value of ``force``.

        """
        basis = clifford.by_name[basis]
        ha = clifford.conjugation_table[self.node[node]["vop"]]
        basis, phase = clifford.conjugate(basis, ha)

        # Flip a coin
        result = force if force != None else random.choice([0, 1])
        # Flip the result if we have negative phase
        if phase == -1:
            result = not result

        if basis == clifford.px:
            result, determinate = self._measure_graph_x(node, result, friend)
        elif basis == clifford.py:
            result, determinate = self._measure_graph_y(node, result)
        elif basis == clifford.pz:
            result, determinate = self._measure_graph_z(node, result)
        else:
            raise ValueError("You can only measure in {X,Y,Z}")

        # Flip the result if we have negative phase
        if phase == -1:
            result = not result

        if detail:
            return {"outcome": int(result),
                    "determinate": (determinate or force != None),
                    "conjugated_basis": basis,
                    "phase": phase,
                    "node": node,
                    "force": force}
        else:
            return int(result)

    def measure_x(self, node, force=None, detail=False, friend=None):
        """ Measure in the X basis """
        return self.measure(node, "px", force, detail, friend)

    def measure_y(self, node, force=None, detail=False):
        """ Measure in the Y basis """
        return self.measure(node, "py", force, detail)

    def measure_z(self, node, force=None, detail=False):
        """ Measure in the Z basis """
        return self.measure(node, "pz", force, detail)

    def measure_sequence(self, measurements, forces=None, detail=False):
        """ Measures a sequence of Paulis

        :param measurements: The sequence of measurements to be made, in the form [(node, basis), ...]
        :type force: list of tuples
        :param force: Measurements in quantum mechanics are probabilistic. If you want to force a particular outcome, use the ``force``. List outcome force values in same order as measurements
        :type force: list
        :param detail: Provide detailed information
        :type detail: boolean

        """
        forces = forces if forces != None else [
            random.choice([0, 1]) for i in range(len(measurements))]
        measurements = zip(measurements, forces)
        results = []
        for (node, basis), force in measurements:
            result = self.measure(node, basis, force, detail)
            results += [result]
        return results

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

    def _measure_graph_x(self, node, result, friend=None):
        """ Measure the bare graph in the X-basis """
        if len(self.adj[node]) == 0:
            return 0, True

        # Pick a friend vertex
        if friend == None:
            if abp.DETERMINISTIC:
                friend = sorted(self.adj[node].keys())[0]
            else:
                friend = next(self.adj[node].iterkeys())
        else:
            assert friend in self.adj[node].keys()  # TODO: unnecessary assert

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

        return result, False

    def _measure_graph_y(self, node, result):
        """ Measure the bare graph in the Y-basis """
        # Do some rotations
        for neighbour in self.adj[node]:
            self._update_vop(neighbour, "sqz" if result else "msqz")

        # A sort of local complementation
        vngbh = set(self.adj[node]) | {node}
        for i, j in it.combinations(vngbh, 2):
            self._toggle_edge(i, j)

        # TODO: naming: # lcoS.herm_adjoint() if result else lcoS
        self._update_vop(node, 5 if result else 6)
        return result, False

    def _measure_graph_z(self, node, result):
        """ Measure the bare graph in the Z-basis """
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

        return result, False

    def order(self):
        """ Get the number of qubits """
        return len(self.node)

    def __str__(self):
        """ Represent as a string for quick debugging """
        s = ""
        for key in sorted(self.node.keys()):
            s += "{}:  {}\t".format(key,
                                    clifford.get_name(self.node[key]["vop"]))
            if self.adj[key]:
                s += str(tuple(self.adj[key].keys())).replace(" ", "")
            else:
                s += "-"
            s += "\n"

        return s

    def to_json(self, stringify=False):
        """ Convert the graph to JSON-like form.

        :param stringify: JSON keys must be strings, But sometimes it is useful to have a JSON-like object whose keys are tuples.

        If you want to dump a graph to disk, do something like this::

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
        """ Construct the graph from JSON data
        :param data: JSON data to be read.
        """
        self.node = data["node"]
        self.adj = data["adj"]

    def to_state_vector(self):
        """ Get the full state vector corresponding to this stabilizer state. Useful for debugging, interface with other simulators.
            This method becomes very slow for more than about ten qubits!

        The output state is represented as a ``abp.qi.CircuitModel``::

            >>> print g.to_state_vector()
            |00000❭: 0.18+0.00j
            |00001❭: 0.18+0.00j ...

        """
        if len(self.node) > 15:
            raise ValueError("Cannot build state vector: too many qubits")
        state = qi.CircuitModel(len(self.node))
        mapping = {node: i for i, node in enumerate(sorted(self.node))}
        for n in self.node:
            state.act_hadamard(mapping[n])
        for i, j in self.edgelist():
            state.act_cz(mapping[i], mapping[j])
        for i, n in self.node.items():
            state.act_local_rotation(mapping[i], clifford.unitaries[n["vop"]])
        return state

    def to_stabilizer(self):
        """
        Get the stabilizer representation of the state::

            >>> print g.to_stabilizer()
               0    1    2    3    100  200
              ------------------------------
               X    Z    Z    X
               Z    X    Z
               Z    Z    X
             - Z              Z
                                   X    Z
                                   Z    X

        """
        return Stabilizer(self)

    def __eq__(self, other):
        """ Check equality between GraphStates """
        return self.adj == other.adj and self.node == other.node

    def copy(self):
        """ Make a copy of this graphstate """
        g = GraphState()
        g.node = self.node.copy()
        g.adj = self.adj.copy()
        return g

