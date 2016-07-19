from websocket_server import WebsocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from SocketServer import ThreadingMixIn
import os, sys, threading
import webbrowser
import argparse

clients = []

def new_message(client, server, message):
    print "Received update from client {}.".format(client["id"])
    server.send_message_to_all(message)

def new_client(client, server):
    print "Client {} connected.".format(client["id"])
    clients.append(client)

def client_left(client, server):
    print "Client {} disconnected.".format(client["id"])
    clients.remove(client)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ Handle requests in a separate thread """

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "ABP websocket server")
    parser.add_argument("-v", action="store_false", help="Launch browser")
    args = parser.parse_args()

    # Change to the right working dir
    where = os.path.join(sys.path[0], "../static")
    os.chdir(where)

    # Start the HTTP server
    httpserver = ThreadedHTTPServer(('', 5001), SimpleHTTPRequestHandler)
    thread = threading.Thread(target = httpserver.serve_forever)
    thread.daemon = True
    thread.start()

    if args.v:
        webbrowser.open("http://localhost:5001/")

    # Start the websocket server
    server = WebsocketServer(5000)
    server.set_fn_new_client(new_client)
    server.set_fn_message_received(new_message)
    server.set_fn_client_left(client_left)
    server.run_forever()
    httpserver.shutdown()

