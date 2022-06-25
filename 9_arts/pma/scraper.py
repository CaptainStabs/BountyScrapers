import csv
import json
import os
import time

import pandas as pd
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tqdm import tqdm

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import sys
from pathlib import Path

p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))
from _common import get_last_id

filename =  "extracted_data.csv"

columns = [
    "object_number",
    "category",
    "date_description",
    "year_start",
    "year_end",
    "materials",
    "dimensions",
    "credit_line",
    "provenance",
    "title",
    "technique",
    "from_location",
    "maker_full_name",
    "maker_role",
    "maker_birth_year",
    "maker_death_year",
    "current_location",
    "image_url",
    "source_1",
    "drop_me"
    ]

with open(filename, "a", encoding='utf-8', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.path.exists(filename) and os.stat(filename).st_size > 283:
        start_id = get_last_id(filename)
    else:
        start_id = 0

    if os.stat(filename).st_size == 0:
        writer.writeheader()

    for i in tqdm(range(start_id, 298920)):
        url = f"https://hackathon.philamuseum.org/api/v0/collection/object?query={i}&api_token=jnFV09XMKDJ0yVYrcQd3si72VFN4EUeM15B479G6RkMfiu4BstY2GuaR19kI"
        r = requests.get(url, verify=False)

        ratelimit_remaining = int(r.headers['X-RateLimit-Remaining'])
        if ratelimit_remaining < 40:
            print(ratelimit_remaining)

        if ratelimit_remaining == 2:
            print("Sleeping for 60")
            time.sleep(60)
            r = requests.get(url, verify=False)
            if r.headers["x-RateLimit-Remaining"] == 1: # don't use var here because we need to check current r headers
                print("Has not reset, exiting.")
                os.exit(1)

        jd = r.json()

        data = {
            "object_number": jd["ObjectNumber"],
            "category": jd["Classification"],
            "date_description": jd["Dated"],
            "year_start": jd["DateBegin"],
            "year_end": jd["DateEnd"],
            "materials": jd["Medium"],
            "dimensions": jd["Dimensions"].replace("\r\n", ""),
            "credit_line": jd["CreditLine"],
            "provenance": jd["Provenance"],
            "title": jd["Title"],
            "technique": jd["Style"],
            "from_location": jd["Geography"].replace("\\u", "\\u"),
            "maker_full_name": "|".join([x["Artist"] for x in jd["Artists"]]),
            "maker_role": "|".join([x["Role"] for x in jd["Artists"]]),
            "current_location": jd["Location"],
            "image_url": jd["Image"],
            "source_1": url,
            "drop_me": i
        }

        try:
            data["maker_birth_year"] = "|".join([x["Artist_Info"].split(",")[-1].split("-")[0].strip() for x in jd["Artists"]])
            data["maker_death_year"] = "|".join([x["Artist_Info"].split(",")[-1].split("-")[-1].strip() for x in jd["Artists"]])
        except AttributeError:
            print("Artist info is null")
            print(jd["Artists"])

        if len(jd["Artists"]) == 1:
            if "unknown" in jd["Artists"][0]["Artist"]:
                data["maker_role"] = ""
                print("Nulling maker_role for", jd["Artists"])

        writer.writerow(data)
