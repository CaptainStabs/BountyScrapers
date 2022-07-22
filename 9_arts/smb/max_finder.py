import requests
from tqdm import tqdm


s = requests.Session()

for page in tqdm(range(9980, 99999)):
    url = f"https://api.smb.museum/search/?offset={page}"
    r = requests.head(url)

    if r.status_code != 500:
        print(page, r.status_code)
