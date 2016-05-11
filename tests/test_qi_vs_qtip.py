from abp import qi
from qutip import *
import numpy as np

def test_1():
    q = QubitCircuit(4)
    q.add_gate("CPHASE", 1, 2, arg_value=np.pi)
    #print gate_sequence_product(q.propagators())

