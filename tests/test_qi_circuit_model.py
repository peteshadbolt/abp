import numpy as np
from abp import qi

def test_init():
    """ Can you initialize some qubits """
    psi = qi.CircuitModel(5)
    assert psi.d == 32

def test_single_qubit_stuff():
    """ Try some sensible single-qubit things """
    psi = qi.CircuitModel(2)
    psi.act_local_rotation(0, qi.px)
    assert np.allclose(psi.state[1], 1)
    psi.act_local_rotation(0, qi.px)
    assert np.allclose(psi.state[0], 1)
    psi.act_local_rotation(0, qi.pz)


def test_more_single_qubit_stuff():
    """ Try some sensible single-qubit things """
    psi = qi.CircuitModel(2)
    psi.act_local_rotation(0, qi.px)
    psi.act_local_rotation(1, qi.px)
    psi.act_cz(0, 1)

def test_equality():
    """ Test that equality succeeds / fails as desired """
    a = qi.CircuitModel(2)
    b = qi.CircuitModel(2)
    assert a == b
    a.act_local_rotation(0, qi.px)
    assert a != b



def test_hadamard():
    """ What does CZ do ? """
    psi = qi.CircuitModel(3)
    psi.act_hadamard(0)
    psi.act_hadamard(1)
    assert np.allclose(psi.state, np.array([[1,1,1,1,0,0,0,0]]).T/2.)
    psi.act_hadamard(1)
    psi.act_hadamard(0)
    psi.act_hadamard(2)
    assert np.allclose(psi.state, qi.ir2*np.array([[1,0,0,0,1,0,0,0]]).T)


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

    psi.act_local_rotation(0, qi.ha)
    psi.act_local_rotation(1, qi.ha)
    psi.act_local_rotation(0, qi.ha)
    psi.act_local_rotation(1, qi.ha)
    assert np.allclose(psi.state[0], 1)


