import requests
import json
from tqdm import tqdm

s = requests.Session()
for i in tqdm(range(1, 4283)):
    r = s.get(f"https://api.acmi.net.au/works/?page={i}")
    with open(f"F:\\museum-collections\\_acmi\\page_{i}.json", "w") as f:
        f.write(json.dumps(r.json()))
        
