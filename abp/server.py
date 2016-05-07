import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import sys
import json
import threading
import time
import os
from graph import GraphState


class VizHandler(SimpleHTTPRequestHandler):

    """ Handles requests to the server """

    def __init__(self, *args, **kwargs):
        SimpleHTTPRequestHandler.__init__(self, *args, **kwargs)

    def get_state(self):
        """ Get the current graph state """
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        state = self.server.state
        self.wfile.write(state.to_json())

    def do_GET(self, *args, **kwargs):
        """ Someone belled the server """
        parsed_path = urlparse.urlparse(self.path)
        if parsed_path.path == "/state":
            return self.get_state()
        else:
            return SimpleHTTPRequestHandler.do_GET(self, *args, **kwargs)


class Server(SocketServer.TCPServer):

    """ Serves the good stuff """
    allow_reuse_address = True

    def __init__(self, port=8000):
        self.port = port
        self.state = None
        SocketServer.TCPServer.__init__(
            self, ("127.0.0.1", self.port), VizHandler)

    def update(self, state):
        """ Update the in-memory state """
        self.state = state

    def run(self):
        """ Run in such a way that keyboard interrupts are caught properly """
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            self.shutdown()

    def start(self):
        """ Start in a new thread """
        thread = threading.Thread(None, self.run)
        thread.daemon = True
        thread.start()
        print "Server running at http://localhost:{}/".format(self.port)



def demograph():
    """ A graph for testing with """
    g = GraphState()
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(0, 3)
    g.add_edge(100, 200)
    return g


if __name__ == '__main__':
    os.chdir("/home/pete/physics/abp/static")
    server = Server()
    server.start()

    g = demograph()


    while True:
        server.update(g)
        time.sleep(1)

    server.shutdown()
