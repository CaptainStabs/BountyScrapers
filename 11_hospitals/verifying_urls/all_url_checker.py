import requests
import pandas as pd
from tqdm import tqdm
from urllib.parse import urlparse
from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.simplefilter('ignore', InsecureRequestWarning)
# import heartrate; heartrate.trace(browser=True, daemon=True)

from urllib.parse import urlparse

import multiprocessing as mp
# import pandas.util.testing as pdt
import pandas.testing as pdt
import numpy as np

tqdm1 = tqdm.pandas()

def is_url(url):
    try:
        a = urlparse(url)
        return all([a.scheme, a.netloc])
    except ValueError:
        return False

def check_url(df):
    checked_urls = []
    compared_urls = []
    for url in tqdm(df):
        compared_urls.append(url)
        if not url:
            checked_urls.append(pd.NA)
            continue
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
            checked_urls.append(pd.NA)
            continue
        except Exception as e:
            print(e)
            print(url)
            checked_urls.append(url)
            continue

        if r.status_code == 200:
            checked_urls.append(url)
            continue
        elif r.status_code == 404:
            checked_urls.append(pd.NA)
            continue

        elif r.status_code == 301 or r.status_code == 302:
            new_loc = r.headers.get("location")
            if is_url(new_loc):
                checked_urls.append(new_loc)
            else:
                checked_urls.append(pd.NA)
            continue
        elif r.status_code != 200 and r.status_code != 404:
            # print(f"\nUnknown code: {r.status_code}")
            # print("\n",url)
            checked_urls.append(url)
            continue
    return checked_urls
    # if checked_urls != compared_urls:
    #     return checked_urls
    # else:
    #     return pd.NA
    


def process(df):
    cdu, ciu, hpg = "cdm_url", "cdm_indirect_url", "homepage"
    df[[cdu, hpg, ciu]] = df[[cdu, hpg, ciu]].progress_apply(check_url)
    return df

if __name__ == "__main__":
    p = mp.Pool(processes=8)

    filename = "non-null.csv"
    df = pd.read_csv(filename)
    split_df = np.array_split(df, 8)

    pool_results = p.map(process, split_df)
    p.close()
    p.join()
    


    parts = pd.concat(pool_results, axis=0)
    # print(parts)
    # pdt.assert_series_equal(parts["ccn"], df["ccn"])

    parts.to_csv(filename[:-4] + "_checked_urls.csv", index=False)
