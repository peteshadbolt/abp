from abp import GraphState
from abp import qi
import numpy as np

def test_single_qubit():
    """ Test some single-qubit stuff """
    g = GraphState()
    g.add_node(0)
    g.add_node(1)
    g.act_local_rotation_by_name(0, "hadamard")
    g.act_local_rotation_by_name(1, "hadamard")
    g.act_cz(0, 1)
    assert np.allclose(g.to_state_vector().state, qi.bond)


