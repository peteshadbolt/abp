from anders_briegel import graphsim

for i in range(4):
    for j in range(24):
        a = graphsim.LocCliffOp(i)
        b = graphsim.LocCliffOp(j)
        print
        print i, j
        print i, j, a.op, b.op
        output = a.conjugate(b)
        print i, j, a.op, b.op, output.ph


