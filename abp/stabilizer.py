class Stabilizer(object):
    def __init__(self, g):
        """ Construct a Stabilizer from a Graphstate """
        pass

    def to_stabilizer(self):
        """ Get the stabilizer tableau.  Work in progress!
        """
        for a, b in it.product(self.node, self.node):
            output[a]["sign"] = 1
            if a == b:
                output[a][b] = "X"
            elif a in self.adj[b]:
                output[a][b] = "Z"
            else:
                output[a][b] = "I"
        return output

