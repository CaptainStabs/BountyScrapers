import json

with open('objects.json', 'r', encoding='utf8') as f:
    data = json.load(f)

print(data["results"][0])
