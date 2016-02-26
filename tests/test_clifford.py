import clifford as lc
from numpy import *

def test_identify_pauli():
    assert lc.identify_pauli(lc.px) == (1, "x")
    assert lc.identify_pauli(-lc.px) == (-1, "x")
    assert lc.identify_pauli(-lc.pz) == (-1, "z")

#def test_against_anders_table():
    #assert allclose(lc.vop_unitaries[0], lc.i)
    #assert allclose(lc.vop_unitaries[10], lc.h)

    #yb = matrix([[1,0],[0,1j]])
    #assert allclose(lc.vop_unitaries[5], yb)

    #xb = matrix([[1,0],[0,-1j]])
    #assert allclose(lc.vop_unitaries[6], xb)

    #ye = matrix([[1,-1j],[-1,-1j]])/sqrt(2)
    #print lc.vop_unitaries[17]
    #print ye
    #assert allclose(lc.vop_unitaries[17], ye)

#def test_some_anders():
    #u = matrix([[1,0],[0,1j]])
    #print u
    #print lc.format_action(lc.get_action(u))
    #print lc.vop_by_name["xb"]

    #u = matrix([[1,0],[0,0-1j]])
    #print u
    #print lc.format_action(lc.get_action(u))
    #print lc.vop_by_name["yb"]


#def _test_anders_problem():
    #bi = lc.vop_by_name["bi"]
    #print bi["name"]
    #print bi["action"]
    #print bi["unitary"]

    #u = exp(-1j*pi/4)*matrix([[0,1],[1j,0]])
    #print u
    #print lc.format_action(lc.get_action(u))
    #print lc.format_action(lc.identify_pauli(u*p*u.H) for p in lc.paulis)
    #u = lc.vop_unitaries[4]
    #print lc.format_action(lc.identify_pauli(u*p*u.H) for p in lc.paulis)

