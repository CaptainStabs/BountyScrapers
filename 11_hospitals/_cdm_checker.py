import pandas as pd
import requests
from tqdm import tqdm

def create_headers(url):
    headers= {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
    "Host": urlparse(url).netloc,
    "Referer": urlparse(url).netloc
    }
    return headers

def url_checker(url):
    r = requests.get(url).status_code
    if r == 200:
        return True
    else:
        print(f"{r} on {url}")
        return False
tqdm = tqdm.pandas()

df = pd.read_csv("possible_indirects.csv")
df = df.dropna(subset=["cdm_url"])

df["cdm_url"] = df["cdm_url"].progress_apply(lambda x: x if url_checker(x) else pd.NA)
print(df)