import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import sys
import json
import threading
import time
import os

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
        self.wfile.write(json.dumps({"state":"{}".format(state)}))
    
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

    def __init__(self, port = 8000):
        self.port = port
        self.state = None
        SocketServer.TCPServer.__init__(self, ("127.0.0.1", self.port), VizHandler)

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

if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(__file__), "../static"))
    print os.curdir
    server = Server()
    server.start()

    i=0
    while True:
        server.update(i)
        i += 1
        time.sleep(1)

    server.shutdown()

