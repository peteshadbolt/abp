import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import sys
import json
import threading
import time

class VizHandler(SimpleHTTPRequestHandler):
    """ Handles requests to the server """
    def __init__(self, *args, **kwargs):
        SimpleHTTPRequestHandler.__init__(self, *args, **kwargs)

    def get_state(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"state":"here is the state"}))
    
    def do_GET(self, *args, **kwargs):
        parsed_path = urlparse.urlparse(self.path)
        print parsed_path.path
        if parsed_path.path == "/state":
            return self.get_state()
        else:
            return SimpleHTTPRequestHandler.do_GET(self, *args, **kwargs)

class VizServer(SocketServer.TCPServer):
    """ Runs the server in a new thread """
    allow_reuse_address = True
    def __init__(self, port = 8000):
        self.port = port
        SocketServer.TCPServer.__init__(self, ("127.0.0.1", self.port), VizHandler)

    def run(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            "Caught keyboard interrupt"
            self.shutdown()

    def start(self):
        thread = threading.Thread(None, self.run)
        thread.daemon = True
        thread.start()
        print "Go to 127.0.0.0:{}".format(self.port)

if __name__ == '__main__':
    server = VizServer()
    server.start()
    time.sleep(5)
    server.shutdown()
