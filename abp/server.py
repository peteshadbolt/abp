import json
from websocket_server import WebsocketServer
import abp


clients = []

def new_message(client, server, message):
    decoded_message = json.loads(message)
    if "diff" in decoded_message:
        server.send_message_to_all(message)
    elif "method" in decoded_message:
        message = compute_diff(decoded_message)
        server.send_message_to_all(message)
    else:
        print "Could not interpret message"


def new_client(client, server):
    print "Client {} connected.".format(client["id"])
    clients.append(client)

def client_left(client, server):
    print "Client {} disconnected.".format(client["id"])
    clients.remove(client)

if __name__ == '__main__':
    server = WebsocketServer(5000)
    server.set_fn_new_client(new_client)
    server.set_fn_message_received(new_message)
    server.set_fn_client_left(client_left)
    server.run_forever()

