import requests
import abp, json
import time

client = abp.Client(clear=True)

client.add_node(0)
client.add_node(1)
client.add_node(99)
client.act_local_rotation(0, 10)
client.act_local_rotation(1, 10)
client.act_local_rotation(99, 10)
client.act_cz(0, 1)
client.act_cz(0, 99)
client.act_cz(1, 99)
for i in range(10):
    client.add_node(i+10)
    client.act_local_rotation(i+10, 10)
    client.act_cz(0, i+10)

print client.get_state()
