from __future__ import absolute_import
import mock
import abp

def test_json():
    """ Test to_json and from_json """
    a = mock.named_node_graph()
    j = a.to_json()

    b = abp.GraphState()
    b.from_json(j)
    assert a == b


def test_json_again():
    """ Test to_json and from_json """
    # Make a random graph
    a = abp.GraphState(10)
    a.act_circuit(mock.random_graph_circuit())

    # Dump it to JSON
    j = a.to_json()

    # Reconstruct from JSON
    b = abp.GraphState()
    b.from_json(j)

    # Check equality
    assert a == b



