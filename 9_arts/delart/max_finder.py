import requests
from tqdm import tqdm

s = requests.Session()

for i in tqdm(range(10290, 10289, -1)):
    url = f"https://emuseum.delart.org/objects/{id}"
    r = s.head(url)

    if r.status_code == 200:
        print("Found!:", id)
