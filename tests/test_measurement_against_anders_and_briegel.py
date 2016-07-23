from abp import GraphState, clifford
from anders_briegel import graphsim
import numpy as np
from tqdm import tqdm
import dummy

N = 10
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


def test_2qubit():
    """ Relentless testing of measurements """
    for measurement in (3, 2, 1):
        for outcome in (0, 1):
            a, b = dummy.bell()
            a.measure(0, str(measurement), outcome)
            b.measure(0, m[measurement], None, outcome)
            assert a == b, "FUCK"
            #print a.to_json()
            #print b.to_json()
            assert a == b, (measurement, outcome)
                
def test_multiqubit():
    """ Relentless testing of measurements """
    for measurement in (1,):
        for i in tqdm(range(1000), "Testing {} measurement".format(measurement)):
            for outcome in (0, 1):
                a, b = dummy.random_state(N, messy=False)
                a.measure(0, str(measurement), outcome)
                b.measure(0, m[measurement], None, outcome)
                assert a == b, (measurement, outcome)
                    
