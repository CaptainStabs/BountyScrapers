import requests
import json
from tqdm import tqdm

with open("urls.csv", "a") as o_f, open("ia.csv", "r") as f:
    next(f)
    for line in tqdm(f):
        line = line.split(",")
        # Get available snapshots
        r = requests.get("https://archive.org/wayback/available?url=" + str(line[0]))
        r = json.loads(r.text)
        url = r["archived_snapshots"]["closest"]["url"]
        file = url.split("/")[-1]
        o_f.write(f"{file},{url}\n")
        # break
