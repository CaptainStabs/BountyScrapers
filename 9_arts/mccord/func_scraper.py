import csv
import json
import os
import re
import signal
import sys
import traceback as tb
from multiprocessing import Pool
from lxml.html import fromstring

import pandas as pd
import requests
from tqdm import tqdm
import sys
import logging; logging.basicConfig(level=logging.INFO)
from pathlib import Path
p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))
from _common import get_last_id
from _common.send_mail import send_mail


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

        if r.status_code == 404:
            return

        try:
            r = r.text
            x=10
            return r
        except Exception:
            print("\n", r.status_code)
            raise
        x += 1

def scraper(url, filename, start_num=False, end_num=False):
    print(start_num, end_num, filename)
    if os.path.exists(filename) and os.stat(filename).st_size > 515:
        start_id = get_last_id(filename, 515)
    else:
        start_id = start_num
    print(start_id)
    columns = ['institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', 'object_number', 'maker_full_name', 'category', 'date_description', 'department', 'year_start', 'inscription', 'year_end', 'material', 'dimensions', 'image_url', 'title', 'from_location', 'image_url', 'description', 'source_1', 'source_2', 'source_2', "maker_full_name", "description", 'drop_me']

    remove_escaped = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        s = requests.Session()

        next = True
        while next = True:
            try:
                url = f"https://www.warmuseum.ca/_api/en/collections/artifact/{id}"
                jd = url_get(url, s)
                if not jd: continue
                if jd["type"] != "artifact":
                    print(jd["type"])
                    continue

                meta = jd["_meta_"]
                data = {
                    "institution_name": "Canadian War Museum",
                    "institution_city": "Ottawa",
                    "institution_state": "Ontario",
                    "institution_country": "Canada",
                    "institution_latitude": 45.4171028137207,
                    "institution_longitude": 75.7169418334961,
                    "object_number": jd["object_number"],
                    "category": "|".join(["|".join([x for x in jd.get("category", [])]), "|".join([x for x in jd["classification"]])]),
                    "date_description": jd["date_made"] if jd.get("date_made") else None,
                    "department": "|".join([x for x in jd["department"]]) if jd.get("department") else None,
                    "year_start": jd["earliest"].split("/")[0] if jd.get("earliest") and len(jd["earliest"].split("/")) else None,
                    "inscription": jd["inscription"] if jd.get("inscription") else None,
                    "year_end": jd["latest"].split("/")[0] if jd.get("latest") and len(jd["latest"].split("/")) else None,
                    "material": "|".join([x for x in jd["material"]]) if jd.get("material") else None,
                    "dimensions": jd["measurements"] if jd.get("measurements") else None,
                    "title": jd.get("title"),
                    "from_location": "|".join([", ".join([x.get("municipality", ""), x.get("country", ""), x.get("continent", "")]) for x in jd["places"]["origins"]]) if jd.get("places") and len(jd["places"]["origins"]) else None,
                    "image_url": jd["media"][0]["url"] if len(jd.get("media", [])) else None,
                    "description": jd.get("model", ""),
                    "maker_full_name": "|".join([x for x in jd["artist_maker"]]) if jd.get("artist_maker") else None,
                    "source_1": f"https://www.warmuseum.ca/collections/artifact/{id}",
                    "source_2": f"https://www.warmuseum.ca/_api/en/collections/artifact/{id}",
                    "drop_me": id,
                }

                writer.writerow(data)

            except KeyboardInterrupt:
                return

            except Exception:
                print("\n",id)
                print(json.dumps(jd, indent=4))
                send_mail("script crashed", tb.print_exc())
                raise


scraper("extracted_data.csv", 0, 18130)
# send_mail("Finished", "Finished")
