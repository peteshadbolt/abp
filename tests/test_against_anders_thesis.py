from numpy import *
import clifford as lc

r = exp(-1j*pi/4)
ir2 = 1/sqrt(2)

anders = [
    matrix([[1, 0], [0, 1]], dtype=complex),
    matrix([[0, 1], [1, 0]], dtype=complex),
    matrix([[0, -1j], [1j, 0]], dtype=complex),
    matrix([[1, 0], [0, -1]], dtype=complex),
\
    r * matrix([[0, 1], [1j, 0]], dtype=complex),
    matrix([[1, 0], [0, 1j]], dtype=complex),
    matrix([[1, 0], [0, -1j]], dtype=complex),
    r * matrix([[0, 1], [-1j, 0]], dtype=complex),
\
    ir2 * matrix([[1,-1],[-1,-1]], dtype=complex),
    ir2 * matrix([[1,-1],[1,1]], dtype=complex),
    ir2 * matrix([[1,1],[1,-1]], dtype=complex),
    ir2 * matrix([[1,1],[-1,1]], dtype=complex),
\
    ir2 * matrix([[1,-1j],[1j,-1]], dtype=complex),
    ir2 * matrix([[1,1j],[-1j,-1]], dtype=complex),
    ir2 * matrix([[1,-1j],[-1j,1]], dtype=complex),
    ir2 * matrix([[1,1j],[1j,1]], dtype=complex),
\
    ir2 * matrix([[1,1j],[1,-1j]], dtype=complex),
    ir2 * matrix([[1,-1j],[-1,-1j]], dtype=complex),
    ir2 * matrix([[1,1j],[-1,1j]], dtype=complex),
    ir2 * matrix([[1,-1j],[1,1j]], dtype=complex),
\
    ir2 * matrix([[1,1],[-1j,1j]], dtype=complex),
    ir2 * matrix([[1,1],[1j,-1j]], dtype=complex),
    ir2 * matrix([[1,-1],[1j,1j]], dtype=complex),
    ir2 * matrix([[1,-1],[-1j,-1j]], dtype=complex),
]


def test_everything():
    for i, (a, b) in enumerate(zip(lc.vop_actions, anders)):
        a2 = lc.format_action(lc.get_action(b))
        if i %4==0:
            print
        print "({} {})".format(a, a2),
        #if not any([allclose(a, x) for x in anders]):
            #print lc.vop_gates[i], "is not in {anders}"

