from abp import GraphState
from abp import Server
import time

server = Server()
server.start()

i=0
while True:
    server.update(i)
    i += 1
    time.sleep(1)

server.shutdown
