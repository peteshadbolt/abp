import numpy as np
from abp import qi

def test_init():
    """ Can you initialize some qubits """
    psi = qi.CircuitModel(5)
    assert psi.d == 32

def test_hadamard():
    """ What does CZ do ? """
    psi = qi.CircuitModel(10)
    psi.act_hadamard(0)
    psi.act_hadamard(0)
    assert np.allclose(psi.state[0], 1)


def test_cz():
    """ What does CZ do ? """
    psi = qi.CircuitModel(2)
    psi.act_hadamard(0)
    psi.act_hadamard(1)
    psi.act_cz(0, 1)
    assert np.allclose(psi.state, qi.bond)


def test_local_rotation():
    """ Do local rotations work okay? ? """
    psi = qi.CircuitModel(2)
    psi.act_local_rotation(0, qi.ha)
    psi.act_local_rotation(0, qi.ha)
    assert np.allclose(psi.state[0], 1)


