import abp
import time

psi = abp.GraphState(use_server = True)

# This all happens instantly
psi.add_qubits(xrange(10))
psi.add_qubit(500)
psi.add_qubit(10) # fails

for i in range(10):
    psi.act_hadamard(i)

for i in range(10, 100)
    psi.act_local_rotation(i, "hadamard")

time.sleep(10)
# The user does some stuff and edits the state

print psi # We see the new qubits


