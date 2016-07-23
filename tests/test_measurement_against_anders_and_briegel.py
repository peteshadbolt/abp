from abp import GraphState, clifford
from anders_briegel import graphsim
import numpy as np
from tqdm import tqdm
import dummy

N = 2
REPEATS = 10
m = {1: graphsim.lco_X, 2: graphsim.lco_Y, 3: graphsim.lco_Z}

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
    for measurement in (3, 2,):
        for outcome in (0, 1):
            a, b = dummy.bell()
            a.measure(0, str(measurement), outcome)
            b.measure(0, m[measurement], None, outcome)
            print a.to_json()
            print b.to_json()
            assert a == b, (measurement, outcome)
                
