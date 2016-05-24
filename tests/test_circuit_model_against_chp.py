import chp
from abp import qi
import numpy as np

n = 10

def get_chp_state():
    """ Convert CHP to CircuitModel """
    output = qi.CircuitModel(n)
    ket = chp.get_ket()
    nonzero = np.sqrt(len(ket))
    for key, phase in ket.items():
        output.state[key] = np.exp(1j*phase*np.pi/2)/nonzero
    return output


def test1():
    chp.init(5)
    chp.act_hadamard(0)
    chp.act_cnot(0, 1)

    yy = qi.CircuitModel(n)
    yy.act_hadamard(0)
    yy.act_hadamard(1)
    yy.act_cz(0, 1)
    yy.act_hadamard(1)
    assert yy == get_chp_state()


