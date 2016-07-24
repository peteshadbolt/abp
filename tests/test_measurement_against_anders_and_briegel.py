from abp import GraphState, clifford
from anders_briegel import graphsim
import numpy as np
from tqdm import tqdm
import dummy

N = 10
REPEATS = 10
m = {1: graphsim.lco_X, 2: graphsim.lco_Y, 3: graphsim.lco_Z}

def test_2qubit():
    """ Relentless testing of measurements """
    clifford.use_old_cz()
    for measurement in (3, 2, 1):
        for outcome in (0, 1):
            a, b = dummy.bell()
            a.measure(0, str(measurement), outcome)
            b.measure(0, m[measurement], None, outcome)
            assert a == b, (measurement, outcome)
                
def test_multiqubit():
    """ Relentless testing of measurements """
    for measurement in (3,2,1,):
        for i in tqdm(range(REPEATS), "Testing measurement {}".format(measurement)):
            for outcome in (0, 1):
                a, b = dummy.clean_random_state(N)
                a.measure(0, str(measurement), outcome)
                b.measure(0, m[measurement], None, outcome)
                assert a == b, (measurement, outcome)
                    
def test_multiqubit2():
    """ Relentless testing of measurements """
    for measurement in (3,):
        for i in tqdm(range(REPEATS), "Testing {} measurement".format(measurement)):
            for outcome in (0, 1):
                for rotation in range(24):
                    a, b = dummy.clean_random_state(3)
                    assert a == b
                    a.act_local_rotation(0, str(rotation))
                    b.local_op(0, graphsim.LocCliffOp(rotation))
                    
                    #print "{} ------------------".format(rotation)
                    #print "pjs b4:", a.to_json()
                    #print "a&b b4:", b.to_json()
                    oa = a.measure(0, str(measurement), outcome)
                    ob = b.measure(0, m[measurement], None, outcome)
                    assert oa == ob, (oa, ob, rotation)
                    #print "pjs af:", a.to_json()
                    #print "a&b af:", b.to_json()
                    assert a == b, (measurement, outcome, rotation)
                    #print
                    
