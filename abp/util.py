""" 
Utility functions for ABP
"""

import json

def xyz(x, y, z=0):
    return {"x": x, "y": y, "z": z}

class ABPJsonEncoder(json.JSONEncoder):
    def default(self, thing):
        print thing

if __name__ == '__main__':
    j = ABPJsonEncoder()
    print j.encode({1:2})
    j = ABPJsonEncoder()
    print j.encode({1:2})
    print j.encode({(1,2):2})

