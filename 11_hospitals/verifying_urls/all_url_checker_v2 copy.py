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

df = pd.read_csv("non-null.csv")
def is_url(url):
    try:
        a = urlparse(url)
        return all([a.scheme, a.netloc])
    except ValueError:
        return False

async def checker(session, url):
    print(url)
    try:
        async with session.head(url, allow_redirects = True, ssl = False) as r:
            if r.status == 200:
                return True
            elif r.status == 400:
                return False
            else:
                print(r.status)
                return False
    except aiohttp.ClientResponseError as e:
        print(e)
        return 'Error'


async def main():
    async with aiohttp.ClientSession(raise_for_status = True) as session:
        df = pd.read_csv("non-null.csv")  
        t = df[:20]
        col = 'homepage'
        t['valid_homepage'] = await tqdm.gather(*(checker(session, url) for url in t[col]))
        return t
    

# if __name__ == "__main__":
df = pd.read_csv("non-null.csv")  
t = await main() 

print(t)   
    # t = await main()
    # t.to_csv("verified_urls.csv", index = False)