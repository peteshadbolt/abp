from numpy import *

px = matrix([[0, 1], [1, 0]], dtype=complex)
py = matrix([[0, -1j], [1j, 0]], dtype=complex)
pz = matrix([[1, 0], [0, -1]], dtype=complex)
i = matrix(eye(2, dtype=complex))
h = matrix([[1, 1], [1, -1]], dtype=complex) / sqrt(2)
p = matrix([[1, 0], [0, 1j]], dtype=complex)

s_set = [i, p, p*p, p*p*p]
c_set = [i, h, h*p, h*p*p, h*p*p*p, h*p*p*h]

def identify_pauli(m):
    for sign in [+1, -1]:
        for label, pauli in zip("XYZ", (px, py, pz)):
            if allclose(sign*pauli, m):
                return "{}{}".format("+" if sign>0 else "-", label)

for p in px, py, pz:
    for sign in [+1, -1]:
        print identify_pauli(sign*p)


print py
print h*px*h.H
print h*py*h.H
print h*pz*h.H

#names = []
#matrices = []
#for s, s_name in zip(s_set, s_names):
    #for c, c_name in zip(c_set, c_names):
        #names.append(s_name+c_name)
        #matrices.append(s*c)

#print " ".join(names)
#print len(names)

#for m in matrices:
    # print (m/abs(amax(m))).round(0).reshape(4)
    #print average(abs(array((m/abs(amax(m))).round(0).reshape(4).tolist()[0])))


    
