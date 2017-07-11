from __future__ import absolute_import
import numpy as np
from abp import qi, GraphState
from tqdm import tqdm
import mock
import nose
from six.moves import range

DEPTH = 1000

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
    psi.act_local_rotation(0, qi.px)
    psi.act_local_rotation(0, qi.pz)
    psi.act_local_rotation(0, qi.px)
    assert np.allclose(psi.state[0], -1)


def test_further_single_qubit_stuff():
    """ Try some sensible single-qubit things """
    psi = qi.CircuitModel(2)
    psi.act_local_rotation(0, qi.py)
    psi.act_local_rotation(1, qi.py)
    psi.act_local_rotation(0, qi.pz)
    psi.act_local_rotation(1, qi.py)
    psi.act_local_rotation(0, qi.hadamard)
    psi.act_local_rotation(0, qi.pz)
    psi.act_local_rotation(0, qi.px)


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
    assert np.allclose(psi.state, np.array([[1, 1, 1, 1, 0, 0, 0, 0]]).T / 2.)
    psi.act_hadamard(1)
    psi.act_hadamard(0)
    psi.act_hadamard(2)
    assert np.allclose(
        psi.state, qi.ir2 * np.array([[1, 0, 0, 0, 1, 0, 0, 0]]).T)


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


def test_dumbness():
    """ Check that I haven't done something really dumb """
    a = qi.CircuitModel(1)
    b = qi.CircuitModel(1)
    assert a == b
    a.act_local_rotation(0, qi.px)
    assert not (a == b)
    a.act_local_rotation(0, qi.px)
    assert (a == b)


def test_to_state_vector_single_qubit():
    """ Test some single-qubit stuff """
    g = GraphState()
    g.add_qubit(0)
    g.add_qubit(1)
    g.act_local_rotation(0, "hadamard")
    g.act_local_rotation(1, "hadamard")
    g.act_cz(0, 1)
    assert np.allclose(g.to_state_vector().state, qi.bond)


def test_normalize_global_phase():
    """ We should be able to see that two states are equivalent up to a global phase """
    for i in range(10):
        u = qi.pz
        phase = np.random.uniform(0, 2 * np.pi)
        m = np.exp(1j * phase) * u
        normalized = qi.normalize_global_phase(m)
        assert np.allclose(normalized, u)


def test_against_chp(n=5):
    """ Test against CHP if it is installed """
    try:
        import chp
    except ImportError:
        raise nose.SkipTest("CHP is not installed")

    def get_chp_state():
        """ Helper to convert CHP to CircuitModel """
        output = qi.CircuitModel(n)
        ket = chp.get_ket()
        nonzero = np.sqrt(len(ket))
        output.state[0, 0] = 0
        for key, phase in ket.items():
            output.state[key] = np.exp(1j * phase * np.pi / 2) / nonzero
        return output

    # Run a simple circuit
    chp.init(n)
    chp.act_hadamard(0)
    chp.act_cnot(0, 1)
    psi = qi.CircuitModel(n)
    psi.act_hadamard(0)
    psi.act_cnot(0, 1)
    assert psi == get_chp_state()

    # Run a random circuit
    chp.init(n)
    psi = qi.CircuitModel(n)
    for i in tqdm(list(range(DEPTH)), "Testing CircuitModel against CHP"):
        if np.random.rand() > .5:
            a = np.random.randint(0, n - 1)
            chp.act_hadamard(a)
            psi.act_hadamard(a)
        else:
            a, b = np.random.randint(0, n - 1, 2)
            if a != b:
                chp.act_cnot(a, b)
                psi.act_cnot(a, b)
        assert psi == get_chp_state()

def test_sqrt_notation(n=2):
    """ Test that SQRT notation looks nice """
    c = mock.random_stabilizer_circuit(n)
    g = GraphState(list(range(n)))
    g.act_circuit(c)

def test_indexint():
    """ Test that we can index into state vectors """
    psi = qi.CircuitModel(0)
    assert psi[0] == 1+0j
    psi[0] = 42
    assert psi[0] == 42

