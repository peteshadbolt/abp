import clifford as lc
from numpy import *

def test_identify_pauli():
    assert lc.identify_pauli(lc.px) == (1, "x")
    assert lc.identify_pauli(-lc.px) == (-1, "x")
    assert lc.identify_pauli(-lc.pz) == (-1, "z")

def test_crap():
    assert allclose(lc.vop_unitaries[0], lc.i)
    assert allclose(lc.vop_unitaries[10], lc.h)

