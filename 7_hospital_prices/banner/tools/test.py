import json
from base64 import b64decode

file = json.loads(open("response.json", "r").read())

contentbytes = b64decode(file["contentBytes"])
print(contentbytes[:100000])