from abp.graphstate import GraphState
from abp.qi import CircuitModel
from abp import clifford
import numpy as np
import random

def multi_qubit_test():
    """ A multi qubit test """
    n = 3
    g = GraphState(range(n))
    c = CircuitModel(n)

    for i in range(n):
        g.act_hadamard(i)
        c.act_hadamard(i)

    assert np.allclose(g.to_state_vector().state, c.state)

    g.act_cz(0, 1)
    c.act_cz(0, 1)
    g.act_cz(1, 2)
    c.act_cz(1, 2)

    s1 = clifford.normalize_global_phase(g.to_state_vector().state)
    s2 = clifford.normalize_global_phase(c.state)
    assert np.allclose(s1, s2)


