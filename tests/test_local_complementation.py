from abp import GraphState
from abp import qi

def test_local_comp():
    """ Test that local complementation works okay """
    psi = GraphState()
    psi.add_node(0)
    psi.add_node(1)
    psi.add_node(2)
    psi.add_node(3)

    for n in psi.node:
        psi.act_hadamard(n)

    psi.act_cz(0, 1)
    psi.act_cz(0, 3)
    psi.act_cz(1, 3)
    psi.act_cz(1, 2)

    before = psi.copy()
    psi.local_complementation(1)
    assert before.edgelist() != psi.edgelist()
    assert before.to_state_vector() == psi.to_state_vector()

