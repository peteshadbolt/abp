from abp import GraphState, clifford
from abp.fancy import GraphState as Fancy
from anders_briegel import graphsim
import random
import time
import numpy as np
from tqdm import tqdm

REPEATS = 100000

def assert_equal(a, b, debug=""):
    assert a.to_json() == b.to_json(), "\n\n" + debug + "\n\n" + str(a.to_json()) + "\n\n" + str(b.to_json())


def test_cz_hadamard(N=9):
    """ Test CZs and Hadamards at random """

    clifford.use_old_cz()

    a = graphsim.GraphRegister(N)
    b = Fancy(range(N))
    while a.to_json() == b.to_json():
        if random.random()>0.5:
            j = random.randint(0, N-1)
            a.hadamard(j)
            b.act_hadamard(j)
        else:
            q = random.randint(0, N-2)
            a.cphase(q, q+1)
            b.act_cz(q, q+1)
    




