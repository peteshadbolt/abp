import clifford as lc
from numpy import *

def test_identify_pauli():
    assert lc.identify_pauli(lc.px) == (1, "x")
    assert lc.identify_pauli(-lc.px) == (-1, "x")
    assert lc.identify_pauli(-lc.pz) == (-1, "z")

def test_against_anders_table():
    assert allclose(lc.vop_unitaries[0], lc.i)
    assert allclose(lc.vop_unitaries[10], lc.h)

    yb = matrix([[1,0],[0,1j]])
    assert allclose(lc.vop_unitaries[5], yb)

    xb = matrix([[1,0],[0,-1j]])
    assert allclose(lc.vop_unitaries[6], xb)

    #ye = matrix([[1,-1j],[-1,-1j]])/sqrt(2)
    #print lc.vop_unitaries[17]
    #print ye
    #assert allclose(lc.vop_unitaries[17], ye)

    u = exp(-1j*pi/4)*matrix([[0,1],[1j,0]])
    print lc.format_action(lc.identify_pauli(u*p*u.H) for p in lc.paulis)
    u = lc.vop_unitaries[4]
    print lc.format_action(lc.identify_pauli(u*p*u.H) for p in lc.paulis)

