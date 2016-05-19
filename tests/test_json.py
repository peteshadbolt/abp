from abp import GraphState
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

#TODO
def _test_to_json():
    """ Nah """
    assert e != g
    e.from_json(js)
    assert e == g


