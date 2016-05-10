from abp import qi

def test_init():
    """ Can you initialize some qubits """
    psi = qi.CircuitModel(5)
    assert psi.d == 32

def test_cz():
    """ What does CZ do ? """
    psi = qi.CircuitModel(2)
    #psi.act_hadamard(0)
    psi.act_hadamard(0)
    print psi
    psi.act_hadamard(1)
    print psi
    psi.act_cz(0, 1)
    print psi
    psi.act_cz(0, 1)
    print psi
    #psi.act_cz(0, 1)


