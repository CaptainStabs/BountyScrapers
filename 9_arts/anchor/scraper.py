import csv
import json
import os
import re
import signal
import sys
import traceback as tb
from multiprocessing import Pool

import pandas as pd
import math
import requests
from tqdm import tqdm
import sys
from pathlib import Path

p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))
from _common import get_last_id
from _common.send_mail import send_mail


def url_get(url, page, s):
    payload = {"pageNumber":page,"seachType":"seeall"}
    x = 0
    while x < 5:
        try:
            r = s.post(url, data=payload)
        except KeyboardInterrupt:
            print("Ctrl-c detected, exiting")
            import sys; sys.exit()
            raise KeyboardInterrupt
        except Exception as e:
            raise(e)
            x+=1
            continue

        if r.status_code == 404:
            return

        try:
            r = r.json()
            x=10
            return r
        except json.decoder.JSONDecodeError:

            if r.status_code == 200:
                return None
            print(r)
            # if x == 4:
            #     raise(e)
        x += 1

def scraper(filename, mus_info):
    # filename, start_num, end_num = filename[0], filename[1], filename[2]
    # signal.signal(signal.SIGINT, signal.SIG_IGN)
    print(filename)
    if os.path.exists(filename) and os.stat(filename).st_size > 515:
        start_pg = get_last_id(filename, 515) - 1
    else:
        start_pg = 1
    print(start_pg)
    columns = ['institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', 'object_number', 'year_start', 'year_end', 'inscription', 'date_description', 'title', 'culture', 'accession_number', 'dimensions', 'provenance', 'materials', 'credit_line', 'description', 'maker_full_name', 'maker_first_name', 'maker_last_name', 'category', 'source_1', 'source_2', 'image_url', 'drop_me']

    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()
        # headers = {
        #   'Content-Type': 'application/json; charset=UTF-8',
        #   'host': 'onlinecollections.anchoragemuseum.org'
        # }
        s = requests.Session()
        # s.headers.update(headers)

        end_pg = 346
        url = "http://onlinecollections.anchoragemuseum.org/apiv2/api/getPageData/"
        for page in tqdm(range(start_pg, end_pg)):
            jd = url_get(url, page, s)
            if not jd: continue
            # make sure to save page to allow resuming
            for item in jd["artifacts"]:
                try:
                    obj = item["_object"]
                    arts = item["Artists"]
                    classif = item["classification"]
                    data = {
                        "institution_name": mus_info["institution_name"],
                        "institution_city": mus_info["institution_city"],
                        "institution_state": mus_info["institution_state"],
                        "institution_country": mus_info["institution_country"],
                        "institution_latitude": mus_info["institution_latitude"],
                        "institution_longitude": mus_info["institution_longitude"],
                        "object_number":  item["ObjectID"],
                        "year_start": obj["DateBegin"],
                        "year_end": obj["DateEnd"],
                        "inscription": obj["Inscribed"],
                        "date_description": item["Dated"],
                        "title": "|".join([x for x in [item["Title"], item["ObjectName"]]]),
                        "culture": item["CultureName"],
                        "accession_number": item["ObjectNumber"],
                        "dimensions": item["Dimensions"].replace("Overall Dimensions: ", "") if item["Dimensions"] else None,
                        "provenance": item["Provenance"],
                        "materials": "|".join(item["Medium"].split(",")) if item["Medium"] else None,
                        "credit_line": item["Credit"],
                        "description": item["PaperFileRef"],
                        "maker_full_name": "|".join([x["DisplayName"] for x in arts]) if arts else None,
                        "maker_first_name": "|".join([x["FirstName"] for x in arts]) if arts else None,
                        "maker_last_name": "|".join([x["LastName"] for x in arts]) if arts else None,
                        "category": "|".join([x["Classification1"] for x in classif]),
                        "source_1": "http://onlinecollections.anchoragemuseum.org/",
                        "source_2": "http://onlinecollections.anchoragemuseum.org/apiv2/api/getArtifacts/" + str(item["ObjectID"]) if item["ObjectID"] else None,
                        "image_url": "http://onlinecollections.anchoragemuseum.org/uploaded_files/" + item["media"][0]["fileName"] if len(item["media"]) else None,
                        "drop_me": page,
                    }

                    writer.writerow(data)

                except Exception:
                    # print(json.dumps(jd))
                    send_mail("script crashed", "")
                    raise

mus_info = {
    "institution_name": "Anchorage Museum",
    "institution_city": "Anchorage",
    "institution_state": "Alaska",
    "institution_country": "United States",
    "institution_latitude": 61.21622772677845,
    "institution_longitude": -149.88557847144895
}
scraper("extracted_data.csv", mus_info)
send_mail("Finished", "")
