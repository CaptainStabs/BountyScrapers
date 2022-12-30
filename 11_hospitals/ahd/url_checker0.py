import requests
import pandas as pd
from tqdm import tqdm
from urllib.parse import urlparse
from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

tqdm = tqdm.pandas()


s = requests.Session()

def check_url(url, s):
    try:
        s.headers.update({
          'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'DNT': '1',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
          'Sec-Fetch-Site': 'none',
          'Sec-Fetch-Mode': 'navigate',
          'Sec-Fetch-User': '?1',
          'Sec-Fetch-Dest': 'document',
          'host': urlparse(url).netloc,

         })
        r = s.head(url, verify=False)

    except requests.exceptions.ConnectionError:
        return False
    except Exception as e:
        print(e)
        print(url)
        return url

    if r.status_code == 200:
        return url
    elif r.status_code == 404:
        return False

    elif r.status_code == 301 or r.status_code == 302:
        return r.headers.get("location")
    elif r.status_code != 200 and r.status_code != 404:
        print(f"\nUnknown code: {r.status_code}")
        print("\n",url)
        return url

filename = "url_addedcleaned.csv"
df = pd.read_csv(filename)
df["homepage_url"] = df["homepage_url"].progress_apply(lambda x: x if check_url(x, s) else pd.NA)

df = df.dropna(subset=["homepage_url"])

df.to_csv(filename[:-4] + "_2.csv", index=False)
