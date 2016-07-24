from abp import GraphState, clifford
from anders_briegel import graphsim
import numpy as np
from tqdm import tqdm
import itertools as it
import dummy
from config import *

N = 10
m = {1: graphsim.lco_X, 2: graphsim.lco_Y, 3: graphsim.lco_Z}

def test_1():
    """ Check that single qubits work """
    space = it.product(range(24), (3,2,1), (0,1))
    for rotation, measurement, outcome in tqdm(space, "Testing single qubit measurements"):
        #print "\nr{} m{} o{}".format(rotation, measurement, outcome)
        a, b = dummy.onequbit()
        #print a.to_json()["node"][0]["vop"], b.to_json()["node"][0]["vop"]
        a.measure(0, str(measurement), outcome)
        b.measure(0, m[measurement], None, outcome)
        #print a.to_json()["node"][0]["vop"], b.to_json()["node"][0]["vop"]
        assert a == b, (a.to_json()["node"][0], b.to_json()["node"][0])
                    
