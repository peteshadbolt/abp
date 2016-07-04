from anders_briegel import graphsim
from abp import clifford, qi
import itertools
import numpy as np

for i, j in itertools.product(range(4), range(24)):
    operation, phase = clifford.conjugate(i, j)
    vop_u = clifford.unitaries[i]
    transform_u = clifford.unitaries[j]
    u = np.dot(transform_u, np.dot(vop_u, qi.hermitian_conjugate(transform_u)))
    #print u.round(2)


