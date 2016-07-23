from abp import GraphState, clifford
from anders_briegel import graphsim

def random_state(N=10, messy=True):
    """ A state to test on """
    a = GraphState(range(N))
    b = graphsim.GraphRegister(N)
    clifford.use_old_cz()

    for i in range(N):
        a.act_hadamard(i)
        b.hadamard(i)

    for i in range(10):
        j, k= np.random.choice(range(N), 2, replace=False)
        a.act_cz(j, k)
        b.cphase(j, k)

    if not messy: return a, b

    for i in range(10):
        j = np.random.choice(range(N))
        k = np.random.choice(range(24))
        a.act_local_rotation(j, k)
        b.local_op(j, graphsim.LocCliffOp(k))

    for i in range(10):
        j, k= np.random.choice(range(N), 2, replace=False)
        a.act_cz(j, k)
        b.cphase(j, k)

    return a, b

def bell():
    a = GraphState(range(2))
    b = graphsim.GraphRegister(2)
    a.act_hadamard(0); a.act_hadamard(1); 
    b.hadamard(0); b.hadamard(1); 
    a.act_cz(0,1)
    b.cphase(0,1)
    return a, b
