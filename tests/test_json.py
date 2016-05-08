from abp.graphstate import GraphState
from abp import clifford
import time
import json


def demograph():
    """ A graph for testing with """
    g = GraphState()
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(0, 3)
    g.add_edge(100, 200)
    return g


def test_json_basic():
    """ Test that we can export to JSON """
    g = demograph()
    js = g.to_json()
    assert "ngbh" in js
    assert "vops" in js
    json.loads(js)


