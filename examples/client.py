import requests
import abp, json

s = requests.Session()
output = s.get("http://localhost:5000/state").content
s.post("http://localhost:5000/state", output).content

s.get("http://localhost:5000/add/99")
s.get("http://localhost:5000/add/100")

print s.get("http://localhost:5000/state").content

s.get("http://localhost:5000/clear")
s.close()

