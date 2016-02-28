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

