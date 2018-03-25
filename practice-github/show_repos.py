import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.github.com")
conn.request("GET", "/users/lasonata/repos", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

print("the number of repositories is:", len(repos))

print("The owner of the first repository is", repo['owner']['login'])

