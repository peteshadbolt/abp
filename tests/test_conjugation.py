from anders_briegel import graphsim
from abp import clifford
import itertools

#//! replaces op by trans * op * trans^dagger and returns a phase,
#/*! either +1 or -1 (as RightPhase(0) or RightPhase(2)) */
#RightPhase conjugate (const LocCliffOp trans);

def test_conjugation():
    """ Test that clifford.conugate() agrees with graphsim.LocCliffOp.conjugate """
    for operation_index, transform_index in itertools.product(range(4), range(24)):
        transform = graphsim.LocCliffOp(transform_index)
        operation = graphsim.LocCliffOp(operation_index)

        phase = operation.conjugate(transform).ph
        phase = [1, 0, -1][phase]
        new_operation = operation.op

        NEW_OPERATION, PHASE = clifford.conjugate(operation_index, transform_index)
        assert new_operation == NEW_OPERATION
        assert PHASE == phase

