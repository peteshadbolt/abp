from abp import GraphState
from anders_briegel import graphsim
from abp import clifford
import random, difflib, re
from copy import deepcopy


def isequal(a, b):
    """ TODO: Sketchy as you like. Remove this abomination """
    aa = a.get_adj_list()
    bb = b.adj_list()
    return re.sub("\\s", "", aa) == re.sub("\\s", "", bb)

clifford.use_old_cz()

N = 3

a = graphsim.GraphRegister(N)
b = GraphState(range(N))
previous_state, previous_cz = None, None
while isequal(a, b):
    if random.random()>0.5:
        j = random.randint(0, N-1)
        a.hadamard(j)
        b.act_hadamard(j)
    else:
        q = random.randint(0, N-2)
        if a!=b:
            a.cphase(q, q+1)
            b.act_cz(q, q+1)


