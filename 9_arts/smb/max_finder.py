import requests
from tqdm import tqdm


s = requests.Session()

for page in tqdm(range(2000400, 996867, -1)):
    url = f"https://api.smb.museum/search/{page}"
    r = s.head(url)

    if r.status_code == 200:
        print("\n",page, r.status_code)
        break
