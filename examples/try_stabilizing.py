import abp
import numpy as np
from anders_briegel import graphsim

def wah():
    N = 10
    a = graphsim.GraphRegister(N)

    for i in range(1000):
        if np.random.random()>0.5:
            j = np.random.randint(0, N-1)
            a.hadamard(j)
        else:
            q = np.random.randint(0, N-2)
            a.cphase(q, q+1)

    a.print_stabilizer()


u = abp.GraphState(xrange(2))
print u.to_stabilizer()
