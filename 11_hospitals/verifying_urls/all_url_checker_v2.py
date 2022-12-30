import requests
import pandas as pd
from tqdm.asyncio import tqdm

from urllib.parse import urlparse
from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.simplefilter('ignore', InsecureRequestWarning)
# import heartrate; heartrate.trace(browser=True, daemon=True)

from urllib.parse import urlparse
import aiohttp
import asyncio
import numpy as np

tqdm1 = tqdm.pandas()

def is_url(url):
    try:
        a = urlparse(url)
        return all([a.scheme, a.netloc])
    except ValueError:
        return False

async def checker(session, url):
    if not url:
        return pd.NA

    try:
        
        async with session.head(url, allow_redirects=True, ssl=False) as r:
            if r.status == 200:
                return url
            elif r.status == 404:
                return pd.NA
            elif r.status == 301 or r.status == 302:
                new_loc = r.headers.get('location')
                if is_url(new_loc):
                    return new_loc
                else:
                    return pd.NA
            elif r.status != 200 and r.status != 404:
                print(f"\nUnkknown code: {r.status} {url}")
                return url

    except Exception as e:
        print(e)
        return pd.NA

async def main():
    async with aiohttp.ClientSession(raise_for_status = True) as session:
        cols = "homepage" #["cdm_url", "cdm_indirect_url", "homepage"]
        df[cols] = await tqdm.gather(*(checker(session, url) for url in df[cols]))
        return df
    

# if __name__ == "__main__":
df = pd.read_csv("non-null.csv")  
t = main() 
print(t)   
    # t = await main()
    # t.to_csv("verified_urls.csv", index = False)