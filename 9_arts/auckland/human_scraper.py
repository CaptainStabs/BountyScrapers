import requests
import json
import csv
import os
import functools
import html

url = "https://api.aucklandmuseum.com/id/humanhistory/object/100299"
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

@functools.lru_cache(maxsize=None)
def url_get(url):
    r = requests.get(url, headers=headers).json()
    return r

@functools.lru_cache(maxsize=None)
def get_category(url):
    r = url_get(url)
    category = r["am:displayValue"][0]["value"]
    return category


def get_title(url):
    r = url_get(url)
    return r["rdf:value"][0]["value"]

def get_material_url(url_list):
    mat_list = []

    for url in url_list:
        r = url_get(url["value"])
        mats = r["ecrm:P2_has_type"]
        for uri in mats:
            mat_list.append(get_material(uri["value"]))
        return "|".join(mat_list)

@functools.lru_cache(maxsize=None)
def get_material(url):
    mat_list = []
    r = url_get(url)
    for mats in r["am:displayValue"]:
        mat_list.append(mats["value"])
    return "|".join(mat_list)

def get_location_url(url):
    r = url_get(url)
    url = r["ecrm:P7_took_place_at"][0]["value"]
    loc = get_location(url)
    return loc

@functools.lru_cache(maxsize=None)
def get_location(url):
    r = url_get(url)
    return r["am:displayValue"][0]["value"]

def get_date(url):
    r = url_get(url)
    d = url_get(r["ecrm:P10_falls_within"][0]["value"])
    return d["rdf:type"][0]["value"].strip("ecrm:").replace("_", " ")

def accession_year(an):
    a = an.split(".")[0]
    if len(a) == 4 and a.isdigit():
        return a
    else:
        return None


columns = ['object_number', 'institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', 'category', 'title', 'description', 'materials', 'from_location', 'culture', 'date_description', 'accession_number', 'accession_year', 'credit_line', 'source_1']

with open("extracted_data.csv", "a") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat("extracted_data.csv").st_size == 0:
        writer.writeheader()

    i = 100299
    response = requests.request("GET", url, headers=headers)

    r = response.json()

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
        "category": get_category(r["am:classification"][0]["value"]),
        "title": r["dc:title"][0]["value"],
        "description": r["dc:description"][0]["value"],
        "materials": get_material_url(r["ecrm:P45_consists_of"]),
        "from_location": get_location_url(r["ecrm:P108i_was_produced_by"][0]["value"]),
        "culture": r["am:culturalOrigin"][0]["value"],
        "date_description": get_date(r["ecrm:P108i_was_produced_by"][0]["value"]),
        "accession_number": r["am:accessionNumber"][0]["value"],
        "accession_year": accession_year(r["am:accessionNumber"][0]["value"]),
        "credit_line": str(r["am:creditLine"][0]["value"]),
        "source_1": url
    }

    print(list(data.keys()))

    print(json.dumps(data, indent=4))
