import requests
import abp, json
import time


def _test_client():
    client = abp.Client(clear=True)

    client.clear()
    for i in range(100):
        client.add_node(i)
        client.act_local_rotation(i, 10)
    for i in range(100-1):
        client.act_cz(i, i+1)

    print client.get_state()

