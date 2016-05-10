from abp.graphstate import GraphState
from abp.qi import CircuitModel
from abp import clifford
import numpy as np
import random

def multi_qubit_test():
    """ A multi qubit test """
    n = 6
    g = GraphState(range(n))
    c = CircuitModel(n)

    for i in range(n):
        g.act_hadamard(i)
        c.act_hadamard(i)

    assert np.allclose(g.to_state_vector().state, c.state)

    for i in range(100):
        a, b = np.random.randint(0, n-1, 2)
        if a != b:
            g.act_cz(a, b)
            c.act_cz(a, b)

    s1 = clifford.normalize_global_phase(g.to_state_vector().state)
    s2 = clifford.normalize_global_phase(c.state)
    assert np.allclose(s1, s2)


