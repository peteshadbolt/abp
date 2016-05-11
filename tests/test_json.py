from abp import GraphState
from abp import clifford
from demograph import demograph
import time
import json

def test_json_basic():
    """ Test that we can export to JSON """
    g = demograph()
    js = g.to_json()
    assert "edges" in js
    assert "nodes" in js
    e = GraphState()
    assert e != g
    e.from_json(js)
    assert e == g


