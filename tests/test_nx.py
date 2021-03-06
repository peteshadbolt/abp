import json
import networkx as nx
from abp import GraphState, NXGraphState
from abp import clifford
from abp.util import xyz
import mock


def test_json_basic():
    """ Test that we can export to JSON """
    g = mock.simple_graph()
    js = g.to_json()
    assert "adj" in js
    assert "node" in js


def test_tuple_keys():
    """ Test that we can use tuple-ish keys """
    g = NXGraphState()
    g.add_qubit("string")
    g.add_qubit((1, 2, 3))
    g.add_edge((1, 2, 3), "string")
    json.dumps(g.to_json(True))


def networkx_test():
    """ Test that NXGraphStates really behave like networkx graphs """
    g = NXGraphState()
    g.add_qubit(0, position=xyz(10, 0, 0))
    g.add_qubit(1, position=xyz(1, 0, 0))
    g.act_hadamard(0)
    g.act_hadamard(1)
    g.act_cz(0, 1)
    g.copy()


def test_from_nx():
    """ Test that making graphs from networkx objects goes smoothly """
    g = nx.random_geometric_graph(100, 2)
    psi = NXGraphState(g)
    assert psi.node[0]["vop"] == 0
    assert len(psi.edges()) > 0
    psi.measure(0, "px", detail=True)

    psi = NXGraphState(nx.Graph(((0, 1),)))
