"""
Allows us to visualize the state in a browser
"""

import atexit
import threading
import time
from websocket import create_connection
from graphstate import GraphState
import json

class VisibleGraphState(GraphState):

    def __init__(self, *args, **kwargs):
        GraphState.__init__(self, *args, **kwargs)
        self.ws = create_connection("ws://localhost:5001")
        atexit.register(self.shutdown)
        #self.ws.send(json.dumps({"method":"clear"}))

    def shutdown(self):
        self.update()
        self.ws.close()

    def to_json(self):
        ngbh = {a: {b : True for b in self.ngbh[a]} 
                for a in self.ngbh}
        return {"vops": self.vops, "ngbh": ngbh, "meta": self.meta}

    def update(self):
        data = json.dumps(self.to_json())
        self.ws.send(data)


