import requests
from tqdm import tqdm

s = requests.Session()
for i in tqdm(range(1, 5000)):
    r = requests.get(f"https://api.vam.ac.uk/v2/object/O{i}?response_format=json")

FIX BY SPLITTING BY UPPER
