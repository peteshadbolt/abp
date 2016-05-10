from abp.graphstate import GraphState
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
    json.loads(js)


