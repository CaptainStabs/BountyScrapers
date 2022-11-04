import requests
import pandas as pd
from tqdm import tqdm
from urllib.parse import urlparse
from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

import multiprocessing as mp
import pandas.util.testing as pdt
import numpy as np

tqdm = tqdm.pandas()


s = requests.Session()
def check_url(url):
    if not url:
        return pd.NA
    try:
        headers = {
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
         }

        r = requests.head(url, verify=False)

    except requests.exceptions.ConnectionError:
        return pd.NA
    except Exception as e:
        # print(e)
        # print(url)
        return url

    if r.status_code == 200:
        return url
    elif r.status_code == 404:
        return pd.NA

    elif r.status_code == 301 or r.status_code == 302:
        return r.headers.get("location")
    elif r.status_code != 200 and r.status_code != 404:
        # print(f"\nUnknown code: {r.status_code}")
        # print("\n",url)
        return url


def process(df):
    res = df["homepage_url"].progress_apply(check_url)
    return res

if __name__ == "__main__":
    p = mp.Pool(processes=16)

    filename = "not_null_og.csv"
    df = pd.read_csv(filename)
    split_df = np.array_split(df, 16)

    pool_results = p.map(process, split_df)
    p.close()
    p.join()

    parts = pd.concat([df, parts], axis=1)
    pdt.assert_series_equal(parts["ccn"], df["ccn"])
    df["homepage_url"] = df["homepage_url"].progress_apply(check_url)

    df = df.dropna(subset=["homepage_url"])

    df.to_csv(filename[:-4] + "_fixed.csv", index=False)
