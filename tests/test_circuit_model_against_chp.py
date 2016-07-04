import chp
from abp import qi
import numpy as np

n = 5

def get_chp_state():
    """ Convert CHP to CircuitModel """
    output = qi.CircuitModel(n)
    ket = chp.get_ket()
    nonzero = np.sqrt(len(ket))
    output.state[0, 0]=0
    for key, phase in ket.items():
        output.state[key] = np.exp(1j*phase*np.pi/2)/nonzero
    return output


def bell_test():
    chp.init(n)
    chp.act_hadamard(0)
    chp.act_cnot(0, 1)

    psi = qi.CircuitModel(n)
    psi.act_hadamard(0)
    psi.act_cnot(0, 1)
    assert psi == get_chp_state()

def random_test():
    chp.init(n)
    psi = qi.CircuitModel(n)
    for i in range(1000):
        if np.random.rand()>.5:
            a = np.random.randint(0, n-1)
            chp.act_hadamard(a)
            psi.act_hadamard(a)
        else:
            a, b = np.random.randint(0, n-1, 2)
            if a!=b:
                chp.act_cnot(a, b)
                psi.act_cnot(a, b)
        assert psi == get_chp_state()



