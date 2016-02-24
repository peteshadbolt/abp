
class LocCliffOp:
    def __init__(self, op):
        self.op = op
        self.name = names[op]

    def __str__(self):
        return self.name


if __name__ == '__main__':
    l = LocCliffOp(0)
    print l

