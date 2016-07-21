from abp import GraphState, clifford
from abp.fancy import GraphState as Fancy
from anders_briegel import graphsim
import random
import numpy as np
from tqdm import tqdm
import time
import itertools as it
import sys

REPEATS = 100000
N=9

def compare(A, B):
    keys_same = set(A["node"].keys()) == set(B["node"].keys())
    vops_same = all(A["node"][i]["vop"] == B["node"][i]["vop"] for i in A["node"].keys())
    edges_same = A["adj"] == B["adj"]
    if keys_same and vops_same and edges_same:
        return True

    sys.exit(0)
    print "doing a state vector check"
    alice = GraphState(range(N))
    alice.node = A["node"]
    alice.adj = A["adj"]

    bob = GraphState(range(N))
    bob.node = B["node"]
    bob.adj = B["adj"]
    if alice.to_state_vector() == bob.to_state_vector():
        return True
    

    return False


if __name__ == '__main__':
    
    clifford.use_old_cz()

    a = graphsim.GraphRegister(N)
    b = Fancy(range(N))

    # Keep comparing until fail
    while compare(a.to_json(), b.to_json()):
        if random.random()>0.5:
            j = np.random.randint(0, N)
            u = random.randint(0, 23)
            print "> Acting U{} on {}".format(u, j)
            a.local_op(j, graphsim.LocCliffOp(u))
            b.act_local_rotation(j, u)
            print "Done"
        else:
            i, j= np.random.randint(0, N, 2)
            if i!=j:
                print "> Acting CZ on {} & {}".format(i, j)
                a.cphase(i, j)
                b.act_cz(i, j)
                print "Done"
        #b.update(delay=0.1)


    # Show the diff
    A = a.to_json()["node"]
    B = b.to_json()["node"]
    for i in range(N):
        if A[i]["vop"] != B[i]["vop"]:
            print "{}/ them: {}, me: {}".format(i, A[i]["vop"], B[i]["vop"])

    # Now construct unitaries
    A = a.to_json()
    B = b.to_json()
    alice = GraphState(range(N))
    alice.node = A["node"]
    alice.adj = A["adj"]

    bob = GraphState(range(N))
    bob.node = B["node"]
    bob.adj = B["adj"]
    print alice.to_state_vector() == bob.to_state_vector()


    b.layout()



        




