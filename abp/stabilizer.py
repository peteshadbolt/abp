"""
Implements a simple Stabilizer object.
"""

import itertools as it
from abp import clifford

I = clifford.by_name["identity"]
X = clifford.by_name["px"]
Z = clifford.by_name["pz"]

class Stabilizer(object):
    def __init__(self, g):
        """ Construct a Stabilizer from a Graphstate """
        self.tableau = {i:{j: I for j in g.node} for i in g.node}
        self.phases = {i: 1 for i in g.node}
        for a, b in it.product(g.node, g.node):
            if a == b:
                self.tableau[a][b] = X
            elif a in g.adj[b]:
                self.tableau[a][b] = Z
            self.conjugate(a, b, g.node[b]["vop"])

    def conjugate(self, a, b, vop):
        """ Do a little conjugation """
        op, phase = clifford.conjugate(self.tableau[a][b], vop)
        self.tableau[a][b] = op
        self.phases[a] *= phase

    def to_dictionary(self):
        """ For comparison with old A&B code """
        m = {1: 0, 1j:1, -1: 2, -1j: 3}
        return {"paulis": self.tableau,
                "phases": {key: m[value] for key, value in self.phases.items()}}

    def __str__(self):
        """ Represent as a string """
        keys = map(str, self.tableau.keys())
        w = max(len(k) for k in keys)
        keys = [k.ljust(w) for k in keys]
        s = "   {}\n".format("  ".join(map(str, keys)))
        s += "  " + "-"*len(keys)*(w+2) + "\n"
        for i in sorted(self.phases):
            sign = self.phases[i]
            sign = {1: "  ", -1: " -", 1j: " i", -1j: "-i"}[sign]
            row = (self.tableau[i][j] for j in sorted(self.phases))
            row = (" XYZ"[i].ljust(w) for i in row)
            row = "  ".join(row)
            s += "{} {}\n".format(sign, row)
        return s

