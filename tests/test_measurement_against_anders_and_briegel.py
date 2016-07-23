from abp import GraphState, clifford
from anders_briegel import graphsim
import numpy as np
from tqdm import tqdm
import dummy

N = 2
REPEATS = 10
PZ = graphsim.lco_Z

def _test_multiqubit_measurement_pz():
    """ Test a multiqubit measurement """
    for i in tqdm(range(REPEATS)):
        a, b = dummy.random_state(messy=False)
        j = np.random.choice(range(N))
        k = "pz"
        a.measure(j, k, 0)
        print a.to_json()
        print b.to_json()
        print
        #assert a.to_json() == b.to_json(), a


def test_multiqubit_pz():
    for i in range(10):
        a, b = dummy.bell()
        assert a == b
        print a.measure(0, "pz", 1)
        print b.measure(0, PZ, None, 1)
        assert a == b
        
