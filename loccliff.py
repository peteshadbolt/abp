NAMES = [" ", "i", "-", "-i"]

class RightPhase(int):
    def __init__(self, phase):
        self.ph = phase % 4

    def get_name(self):
        return NAMES[self.ph]


