import requests
import abp, json
import time

client = abp.Client()

client.add_node(0)
client.add_node(1)

print client.get_state()
