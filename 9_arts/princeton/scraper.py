import requests
import json

r = requests.get("https://data.artmuseum.princeton.edu/objects/2496").json()

print(json.dumps(r, indent=4))
