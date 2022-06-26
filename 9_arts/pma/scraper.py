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

global key_list

def sleep_counter(seconds):
    for remaining in range(seconds, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("Too many requests, waiting for {:2d} seconds.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)

def url_get(id, key, s):
    url = f"https://hackathon.philamuseum.org/api/v0/collection/object?query={id}&api_token={cur_key}"
    return s.get(url, verify=False)

def key_iter(keys):
    k = next(keys)
    if k == cur_key:
        k = next(keys)
        return k
    else:
        return k


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
    key_list = ["jnFV09XMKDJ0yVYrcQd3si72VFN4EUeM15B479G6RkMfiu4BstY2GuaR19kI", "wfXOpPLeYwgissXKDoT5MzygR4ApP8Ev14HIR83LtHNMFY4JdHRuVyk3qJK7", "T3UWvnmQdtMSeZUZcjqi75gu7PTpjWJItRYdcicMtWx0xXEri1dBhW6RpfPd", "d3INVaCoZxa1PbuLmm3RhghHcdSJQzF0XHhXqxVWQez0VCBREn8cgGtajOK5"]
    keys = iter(key_list)

    cur_key = key_list[0]
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.path.exists(filename) and os.stat(filename).st_size > 283:
        start_id = get_last_id(filename)
    else:
        start_id = 0

    if os.stat(filename).st_size == 0:
        writer.writeheader()

    s = requests.Session()
    for i in tqdm(range(start_id, 298920)):
        url = f"https://hackathon.philamuseum.org/api/v0/collection/object?query={i}"
        r = url_get(i, cur_key, s)
        ratelimit_remaining = int(r.headers['X-RateLimit-Remaining'])
        # print(ratelimit_remaining)
        if ratelimit_remaining < 20:
            print("\n", ratelimit_remaining)

        if ratelimit_remaining == 10:
            print("Sleeping for 60")
            # sleep_counter(120)

            try:
                cur_key = key_iter(keys)
            except StopIteration:
                keys = iter(key_list)
                cur_key = key_iter(keys)
            r = url_get(i, cur_key, s)

            print("ratelimit remaining under 10", r.headers["X-RateLimit-Remaining"])
            if r.headers["x-RateLimit-Remaining"] == 1: # don't use var here because we need to check current r headers
                print("Has not reset, exiting.")
                os.exit(1)
        elif ratelimit_remaining < 10:
            try:
                cur_key = key_iter(keys)
            except StopIteration:
                keys = iter(key_list)
                cur_key = key_iter(keys)
            r = url_get(i, cur_key, s)

        print(r.status_code)
        if r.status_code == 429:
            retry_after = int(r.headers["retry-after"]) + 1
            # sleep_counter(retry_after)
            try:
                cur_key = key_iter(keys)
            except StopIteration:
                keys = iter(key_list)
                cur_key = key_iter(keys)
            r = url_get(i, cur_key, s)

            if not r.headers["x-RateLimit-Remaining"]: # don't use var here because we need to check current r headers
                print("Has not reset, exiting.")
                os.exit(1)

        if r.status_code != 500 and r.status_code != 429:
            jd = r.json()

            data = {
                "object_number": jd["ObjectNumber"],
                "category": jd["Classification"],
                "date_description": jd["Dated"],
                "year_start": jd["DateBegin"],
                "year_end": jd["DateEnd"],
                "materials": jd["Medium"],
                "credit_line": jd["CreditLine"],
                "provenance": jd["Provenance"],
                "title": jd["Title"],
                "technique": jd["Style"],
                "maker_full_name": "|".join([x["Artist"] for x in jd["Artists"]]),
                "maker_role": "|".join([x["Role"] for x in jd["Artists"]]),
                "current_location": jd["Location"],
                "image_url": jd["Image"],
                "source_1": url,
                "drop_me": i
            }

            if len(jd["Artists"]) > 1:
                try:
                    data["maker_birth_year"] = "|".join([x["Artist_Info"].split(",")[-1].split("-")[0].strip() if x["Artist_Info"] else "" for x in jd["Artists"]])
                    data["maker_death_year"] = "|".join([x["Artist_Info"].split(",")[-1].split("-")[-1].strip() if x["Artist_Info"] else "" for x in jd["Artists"] if x["Artist_Info"]])
                except AttributeError:
                    print("Artist info is null")
                    print(jd["Artists"])

            elif len(jd["Artists"]) == 1:
                if "unknown" in jd["Artists"][0]["Artist"]:
                    data["maker_role"] = ""
                    print("Nulling maker_role for", jd["Artists"])

            if jd["Dimensions"]:
                data["dimensions"] = jd["Dimensions"].replace("\r\n", "")

            if jd["Geography"]:
                data["from_location"] = jd["Geography"].replace("\\u", "\\u")

            writer.writerow(data)
