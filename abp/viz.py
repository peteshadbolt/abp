"""
Allows us to visualize the state in a browser
"""

import atexit, json, time
from graphstate import GraphState
from websocket import create_connection

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

    def update(self, delay = 0.5):
        """ Call this function when you are ready to send data to the browser """
        data = json.dumps(self.to_json())
        self.ws.send(data)
        time.sleep(delay)

