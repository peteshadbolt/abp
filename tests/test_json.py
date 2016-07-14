from abp import GraphState, fancy
from abp import clifford
from demograph import demograph
import time
import json

def test_json_basic():
    """ Test that we can export to JSON """
    g = demograph()
    js = g.to_json()
    assert "adj" in js
    assert "node" in js
    e = GraphState()

def test_tuple_keys():
    """ Test that we can write tuple-ish keys """
    g = fancy.GraphState()
    g.add_node("string")
    g.add_node((1, 2, 3))
    g.add_edge((1, 2, 3), "string")
    print json.dumps(g.to_json(True))



