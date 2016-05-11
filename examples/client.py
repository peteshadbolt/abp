import requests
import abp, json

s = requests.Session()
output = json.loads(s.get("http://localhost:5000/state").content)
print output
state = json.loads(s.post("http://localhost:5000/state").content)

