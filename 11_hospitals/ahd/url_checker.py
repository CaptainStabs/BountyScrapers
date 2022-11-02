import requests
import pandas as pd
from tqdm import tqdm

tqdm = tqdm.pandas()


s = requests.Session()
s.headers.update({
    "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
})
def check_url(url, s):
    try:
        r = s.head(url)
    except Exception as e:
        raise(e)
        return url

    if r.status_code == 200:
        return url
    elif r.status_code == 404:
        return False

    elif r.status_code == 301 or r.status_code == 302:
        return r.headers.get("location")
    elif r.status_code != 200 and r.status_code != 404:
        print(f"\nUnknown code: {r.status_code}")
        print(url)
        return url

filename = "url_added.csv"
df = pd.read_csv(filename)
df["homepage_url"] = df["homepage_url"].progress_apply(lambda x: x if check_url(x, s) else pd.NA)

df = df.drop_na(subset=["homepage_url"])

df.to_csv(filename[:-4] + "cleaned.csv", index=False)
