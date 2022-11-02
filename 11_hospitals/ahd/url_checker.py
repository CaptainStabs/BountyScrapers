import requests
import pandas as pd
from tqdm import tqdm

tqdm = tqdm.pandas()


s = requests.Session()
def check_url(url, s):
    r = s.head(url)
    if r.status_code == 200:
        return True
    elif r.status_code == 404:
        return False

    elif r.status_code == 301 or r.status_code == 302:
        print(r.headers)
    elif r.status_code != 200 and r.status_code != 404:
        print(f"\nUnknown code: {r.status_code}")
        return True

filename = "url_added.csv"
df = pd.read_csv(filename)
df["homepage_url"] = df["homepage_url"].progress_apply(lambda x: x if check_url(x, s) else pd.NA)

df = df.drop_na(subset=["homepage_url"])

df.to_csv(filename[:-4] + "cleaned.csv", index=False)
