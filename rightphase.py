NAMES = [" ", "i", "-", "-i"]

class RightPhase(int):
    def __new__(cls, value):
        return  super(TestClass, cls).__new__(cls, value % 4)

a = TestClass(2)
b = TestClass(5)
print a, b
print a+b+b

