import requests
import json
import csv
import os
from cachetools import cached
from cachetools.keys import hashkey
from functools import lru_cache
import html
from tqdm import tqdm
import pandas as pd

# url = "https://api.aucklandmuseum.com/id/humanhistory/object/100299"
headers = {
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
}

@cached(cache={}, key=lambda url, s: hashkey(url))
def url_get(url, s):
    r = s.get(url, headers=headers).json()
    return r

def get_category(url, s):
    r = url_get(url, s)
    category = r["am:displayValue"][0]["value"]
    return category

def get_title(url, s):
    r = url_get(url, s)
    return r["rdf:value"][0]["value"]

def get_material_url(url_list, s):
    mat_list = []
    for url in url_list:
        r = url_get(url["value"], s)
        mats = r["ecrm:P2_has_type"]
        for uri in mats:
            mat_list.append(get_material(uri["value"]))
        return "|".join(mat_list)

def get_material(url, s):
    mat_list = []
    r = url_get(url, s)
    for mats in r["am:displayValue"]:
        mat_list.append(mats["value"])
    return "|".join(mat_list)

def get_location_url(url, s):
    r = url_get(url, s)
    url = r["ecrm:P7_took_place_at"][0]["value"]
    loc = get_location(url, s)
    return loc

def get_location(url, s):
    r = url_get(url, s)
    return r["am:displayValue"][0]["value"]

def get_date(url, s):
    r = url_get(url, s)
    d = url_get(r["ecrm:P10_falls_within"][0]["value"], s)
    return d["rdf:type"][0]["value"].strip("ecrm:").replace("_", " ")

@lru_cache(maxsize=None)
def accession_year(an):
    a = an.split(".")[0]
    if len(a) == 4 and a.isdigit():
        return a
    else:
        return None


filename = "extracted_data.csv"
if os.path.exists(filename) and os.stat(filename).st_size > 260:
    df = pd.read_csv(filename)

    # Get the last row from df
    last_row = df.tail(1)
    # Access the corp_id
    last_id = last_row["object_number"].values[0]
    last_id += 1
else:
    last_id = 1

columns = ['object_number', 'institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', 'category', 'title', 'description', 'materials', 'from_location', 'culture', 'date_description', 'accession_number', 'accession_year', 'credit_line', 'source_1']

with open(filename, "a") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat(filename).st_size == 0:
        writer.writeheader()

    for i in tqdm(range(last_id, 100300)):
        url = f"https://api.aucklandmuseum.com/id/humanhistory/object/{i}"
        s = requests.Session()
        s.headers.update(headers)
        response = requests.request("GET", url, headers=headers)

        r = response.json()

        print(r)
        if len(r["am:culturalOrigin"]) > 1:
            print(url)

        data = {
            "object_number": i,
            "institution_name": "Auckland Museum",
            "institution_city": "Auckland",
            "institution_state": "",
            "institution_country": "New Zealand",
            "institution_latitude": 33.9211533,
            "institution_longitude": -84.3692509,
            "category": get_category(r["am:classification"][0]["value"], s),
            "title": r["dc:title"][0]["value"],
            "description": r["dc:description"][0]["value"],
            "materials": get_material_url(r["ecrm:P45_consists_of"], s),
            "from_location": get_location_url(r["ecrm:P108i_was_produced_by"][0]["value"], s),
            "culture": r["am:culturalOrigin"][0]["value"],
            "date_description": get_date(r["ecrm:P108i_was_produced_by"][0]["value"], s),
            "accession_number": r["am:accessionNumber"][0]["value"],
            "accession_year": accession_year(r["am:accessionNumber"][0]["value"], s),
            "credit_line": str(r["am:creditLine"][0]["value"]),
            "source_1": url
        }

        writer.writerow(data)
