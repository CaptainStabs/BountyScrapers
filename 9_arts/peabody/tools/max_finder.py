import requests
from tqdm import tqdm

s = requests.Session()

for i in tqdm(range(556989, 668999)):
    r = requests.head(f"https://collections.peabody.harvard.edu/objects/details/{i}")

    if r.status_code == 200:
        print(i)
