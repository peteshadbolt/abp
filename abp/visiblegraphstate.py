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

    """ Overloads the graph state with methods for sending to the browser over a websocket """

    def __init__(self, *args, **kwargs):
        """ Constructor """
        GraphState.__init__(self, *args, **kwargs)
        self.ws = create_connection("ws://localhost:5000")
        atexit.register(self.shutdown)

    def shutdown(self):
        """ The client should shut down automatically on close """
        self.update()
        self.ws.close()

    def to_json(self):
        """ We override to_json() so that we send the whole `ngbh` structure in JS-friendly form """
        ngbh = {a: {b: True for b in self.ngbh[a]}
                for a in self.ngbh}
        return {"vops": self.vops, "ngbh": ngbh, "meta": self.meta}

    def update(self):
        """ Call this function when you are ready to send data to the browser """
        data = json.dumps(self.to_json())
        self.ws.send(data)
