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
# import heartrate; heartrate.trace(browser=True, daemon=True)

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
    x = 0
    while x < 5:
        r = s.get(url, headers=headers)
        if r.status_code == 404:
            return
        try:
            r = r.json()
            x=10
            return r
        except json.decoder.JSONDecodeError:
            print(r)
            if x == 4:
                raise(json.decoder.JSONDecodeError)
        x += 1


def get_category(url, s):
    r = url_get(url, s)
    if not r: return
    category = r["am:displayValue"][0]["value"]
    return category

def get_title(url, s):
    r = url_get(url, s)
    return r["rdf:value"][0]["value"]

def get_material_url(url_list, s):
    try:
        url_list = url_list["ecrm:P45_consists_of"]
        mat_list = []
        for url in url_list:
            r = url_get(url["value"], s)
            if not r: raise(KeyError)
            mats = r["ecrm:P2_has_type"]
            for uri in mats:
                a = get_material(uri["value"], s)
                if a == None: return None
                mat_list.append(a)
            return "|".join(mat_list)
    except KeyError:
        return None



def get_material(url, s):
    mat_list = []
    r = url_get(url, s)
    for mats in r["am:displayValue"]:
        mat_list.append(mats["value"])
    return "|".join(mat_list)

def get_location_url(url, s):
    try:
        url = url["ecrm:P108i_was_produced_by"][0]["value"]
        r = url_get(url, s)
        if not r: raise(KeyError)
        url = r["ecrm:P7_took_place_at"][0]["value"]
        r = url_get(url, s)
        if not r: raise(KeyError)
        if "am:displayValue" in r.keys():
            return r["am:displayValue"][0]["value"]
        else:
            return r["dc:title"][0]["value"]
    except KeyError:
        return None

def get_date(url, s):
    try:
        url = url["ecrm:P108i_was_produced_by"][0]["value"]
        r = url_get(url, s)
        d = url_get(r["ecrm:P10_falls_within"][0]["value"], s)
        return d["rdf:type"][0]["value"].strip("ecrm:").replace("_", " ")
    except KeyError:
        return None


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
    # last_id = 3169
else:
    last_id = 1

columns = ['object_number', 'institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', 'category', 'title', 'description', 'materials', 'from_location', 'culture', 'date_description', 'accession_number', 'accession_year', 'credit_line', 'source_1']

with open(filename, "a", encoding='utf-8') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat(filename).st_size == 0:
        writer.writeheader()
                                #100300
    for i in tqdm(range(last_id, 21398)):
        url = f"https://api.aucklandmuseum.com/id/humanhistory/object/{i}"
        s = requests.Session()
        s.headers.update(headers)

        request_tries = 0

        while request_tries < 4:
            try:
                response = s.request("GET", url, headers=headers)
                request_tries = 11
            except requests.exceptions.ConnectionError:
                print("  [!] Connection Closed! Retrying in 5...")
                request_tries += 1

            except requests.exceptions.ReadTimeout:
                print("   [!] Read timeout! Retrying in 5...")
                request_tries += 1

        print(url)
        try:
            r = response.json()
        except json.decoder.JSONDecodeError:
            print("404ed")
            print(response.status_code)
            continue

        data = {
            "object_number": i,
            "institution_name": "Auckland Museum",
            "institution_city": "Auckland",
            "institution_state": "",
            "institution_country": "New Zealand",
            "institution_latitude": 33.9211533,
            "institution_longitude": -84.3692509,
            # "title": r["dc:title"][0]["value"],
            "materials": get_material_url(r, s),
            "from_location": get_location_url(r, s),
            "date_description": get_date(r, s),
            "source_1": url
        }

        ac = "am:classification"
        if ac in r.keys():
            data["category"] = get_category(r[ac][0]["value"], s)

        aco = "am:culturalOrigin"
        if  aco in r.keys():
            if len(r[aco]) > 1:
                print(url)
            data["culture"] = r[aco][0]["value"]

        aan = "am:accessionNumber"
        if aan in r.keys():
            data["accession_number"] = r[aan][0]["value"]
            data["accession_year"] = accession_year(r[aan][0]["value"])

        if "dc:description" in r.keys():
            data["description"] = r["dc:description"][0]["value"]

        if "am:creditLine" in r.keys():
            data["credit_line"] = str(r["am:creditLine"][0]["value"])

        if "dc:title" in r.keys():
            data["title"] = r["dc:title"][0]["value"]

        writer.writerow(data)
