import requests
import abp, json

class Client(object):
    def __init__(self, host="localhost", port=5000, clear=False):
        self.session = requests.Session()
        self.root = "http://{}:{}".format(host, port)
        if clear:
            self.clear()

    def get(self, endpoint):
        url =self.root+endpoint
        response = self.session.get(url)
        assert response.status_code == 200
        return response.content

    def get_state(self):
        response = self.get("/state")
        output = abp.GraphState()
        output.from_json(json.loads(response))
        return output

    def set_state(self, state):
        return self.session.post(self.root+"/state", data=state.to_json())

    def add_node(self, node):
        return self.get("/add_node/{}".format(node))

    def act_local_rotation(self, node, operation):
        return self.get("/act_local_rotation/{}/{}".format(node, operation))

    def act_cz(self, a, b):
        return self.get("/act_cz/{}/{}".format(a, b))

    def clear(self):
        return self.get("/clear")

    def kill(self):
        self.session.close()
