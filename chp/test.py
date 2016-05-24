import chp
import numpy as np

chp.init(5)
chp.act_hadamard(0)
chp.act_cnot(0, 1)
chp.act_phase(0)

for key, value in chp.get_ket().items():
    print bin(key), np.exp(1j * value * np.pi/2).round(2)

