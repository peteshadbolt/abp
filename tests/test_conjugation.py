from anders_briegel import graphsim
import itertools

#//! replaces op by trans * op * trans^dagger and returns a phase,
#/*! either +1 or -1 (as RightPhase(0) or RightPhase(2)) */
#RightPhase conjugate (const LocCliffOp trans);

def test_conjugation():
    """ Test that clifford.conugate() agrees with graphsim.LocCliffOp.conjugate """
    for i, j in it.product(range(4), range(24)):
        a = graphsim.LocCliffOp(i)
        b = graphsim.LocCliffOp(j)
        output = a.conjugate(b)
        print i, j, a.op, b.op, output.ph

