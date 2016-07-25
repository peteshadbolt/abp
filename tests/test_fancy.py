import json
import networkx as nx
from abp import GraphState, fancy
from abp import clifford
from abp.util import xyz
from mock import simple_graph

def test_json_basic():
    """ Test that we can export to JSON """
    g = simple_graph()
    js = g.to_json()
    assert "adj" in js
    assert "node" in js

def test_tuple_keys():
    """ Test that we can use tuple-ish keys """
    g = fancy.GraphState()
    g.add_node("string")
    g.add_node((1, 2, 3))
    g.add_edge((1, 2, 3), "string")
    json.dumps(g.to_json(True))

def networkx_test():
    """ Test that fancy graph states really behave like networkx graphs """
    g = fancy.GraphState()
    g.add_node(0, position = xyz(10, 0, 0))
    g.add_node(1, position = xyz(1, 0, 0))
    g.act_hadamard(0)
    g.act_hadamard(1)
    g.act_cz(0, 1)
    g.copy()

    # TODO: more tests here!



