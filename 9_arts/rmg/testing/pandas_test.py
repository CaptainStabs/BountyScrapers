import polars as pl
import pandas as pd
from tqdm import tqdm
import json
import requests
from lxml.html import fromstring

from pathlib import Path
import sys
import os
p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))
from _common import get_last_id
from _common.send_mail import send_mail


headers = {}

column = ['ID:', 'Collection:', 'Type:', 'Display location:', 'Creator:', 'Events:', 'Date made:', 'Credit:', 'Measurements:', 'Parts:', 'Places:', 'People:', 'Vessels:', 'Exhibition:', 'title', 'image_url', 'drop_me']


filename = "extracted_data.csv"

def url_get(url, s):
    x = 0
    while x < 5:
        try:
            r = s.get(url)
        # except KeyboardInterrupt:
        #     print("Ctrl-c detected, exiting")
        #     # import sys; sys.exit()
        #     raise KeyboardInterrupt
        except Exception as e:
            raise(e)
            x+=1
            continue

        if r.status_code == 404 or r.status_code == 500:
            return

        try:
            r = r.html()
            x=10
            return r
        except json.decoder.JSONDecodeError:

            if r.status_code == 200:
                return None
            print(r)
            # if x == 4:
            #     raise(e)
        x += 1

def scraper(filename, start_num=False, end_num=False):
    s = requests.Session()
    if os.path.exists(filename) and os.stat(filename).st_size > 515:
        start_id = get_last_id(filename, 515)
    else:
        start_id = start_num

    for i in tqdm(range(start_id, end_num, 5)):
        try:
            url = f"https://www.rmg.co.uk/collections/objects/rmgc-object-{i}"
            html = s.get(url).text
        except KeyboardInterrupt:
            break
        except:
            url = f"https://www.rmg.co.uk/collections/objects/rmgc-object-{i+1}"
            try:
                html = s.get(url).text
            except:
                continue

        try:
            df = pd.read_html(html)[0]
        except ValueError:
            continue

        df = df.transpose()
        df.columns = [x.strip(":").replace(" ", "_").lower() for x in df.iloc[0]]
        df = df.iloc[1:]

        parser = fromstring(html)
        title = parser.xpath('//*[@id="block-rmg-theme-content"]/div[1]/div[2]/div[3]/h2/text()')
        image_url = parser.xpath('//*[@id="block-rmg-theme-content"]/div[1]/div[2]/div[2]/div/div/div/div/div/div[1]/div/div/div/img/@data-img-full')

        df["title"] = title if title else pd.NA
        df["image_url"] = image_url[0] if image_url else pd.NA
        df["drop_me"] = i

        if i == 1:
            df.to_csv(filename, mode="a", index=False, header=True)
        else:
            df.to_csv(filename, mode="a", index=False, header=False)

scraper(filename, 1, 900)
