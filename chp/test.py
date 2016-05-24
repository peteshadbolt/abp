import chp

chp.init(5)
chp.act_hadamard(0)
chp.act_cnot(0, 1)
chp.act_phase(0)
print chp.get_ket()

