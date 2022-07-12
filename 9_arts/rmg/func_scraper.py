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

column = ['id', 'collection', 'type', 'display_location', 'creator', 'events', 'date_made', 'credit', 'measurements', 'parts', 'places', 'people', 'vessels', 'exhibition', 'title', 'description', 'image_url', 'source_1', 'drop_me']

# filename = "extracted_data.csv"

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
            r = r.text
            x=10
            return r
        except Exception:
            print("\n", r.status_code)
            raise
        x += 1

def scraper(filename, start_num=False, end_num=False):
    try:
        if os.path.exists(filename) and os.stat(filename).st_size > 515:
            start_id = get_last_id(filename, 515)
        else:
            start_id = start_num

        s = requests.Session()
        for i in tqdm(range(start_id, end_num)):
            url = f"https://www.rmg.co.uk/collections/objects/rmgc-object-{i}"
            html = url_get(url, s)

            if not html: continue

            try:
                df = pd.read_html(html)[0]
            except ValueError:
                print("\nNo tables")
                continue

            df = df.transpose() # Data is vertical on the website, need the left column to be header
            df.columns = [x.strip(":").replace(" ", "_").lower() for x in df.iloc[0]] # standardize the col names
            df = df.iloc[1:] # select the data, skipping 0 that is the header source

            # Get non-tabulated data
            parser = fromstring(html)
            title = parser.xpath('//*[@id="block-rmg-theme-content"]/div[1]/div[2]/div[3]/h2/text()')
            if not title:
                title = parser.xpath('//*[@id="block-rmg-theme-content"]/div[1]/div[2]/div[2]/h2/text()')
            image_url = parser.xpath('//*[@id="block-rmg-theme-content"]/div[1]/div[2]/div[2]/div/div/div/div/div/div[1]/div/div/div/img/@data-img-full')
            desc = parser.xpath('//*[@id="block-rmg-theme-content"]/div[1]/div[2]/div[3]/div[1]/text()')
            desc = " ".join([x.replace("\n", "").strip() for x in desc if x.replace("n", "").strip()]) if desc else None
            if not desc:
                desc = parser.xpath('//*[@class="collections-object-page__description"]/text()')
                desc = " ".join([x.replace("\n", "").strip() for x in desc if x.replace("n", "").strip()]) if desc else None

            df["title"] = title if title else None
            df["image_url"] = image_url[0] if image_url else None
            df["description"] = desc if desc else None
            df["source_1"] = url
            df["drop_me"] = int(i)

            for col in column:
                if col not in df.columns.tolist():
                    df[col] = None
                    
            if i == start_id:
                df.to_csv(filename, mode="a+", index=False, columns=column, header=True)
            else:
                df.to_csv(filename, mode="a+", index=False, columns=column, header=False)
    except KeyboardInterrupt:
        return

# scraper(filename, 1, 1197899)
