import requests
import json
import csv
import os
import functools

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
def url_get(url)
    r = requests.get(url, headers=headers).json()
    return r

@functools.lru_cache(maxsize=None)
def get_category(url):
    r = requests.get(url, headers=headers).json()
    category = r["am:displayValue"][0]["value"]
    return category


def get_title(url):
    r = requests.get(url, headers=headers).json()
    return r["rdf:value"][0]["value"]

def get_material_url(url_list):
    mat_list = []

    for url in url_list:
        r = requests.get(url["value"], headers=headers).json()
        mats = r["ecrm:P2_has_type"]
        for uri in mats:
            mat_list.append(get_material(uri["value"]))
        return "|".join(mat_list)

@functools.lru_cache(maxsize=None)
def get_material(url):
    mat_list = []
    r = requests.get(url, headers=headers).json()
    for mats in r["am:displayValue"]:
        mat_list.append(mats["value"])
    return "|".join(mat_list)

def get_location_url(url):
    r = requests.get(url, headers=headers).json()
    url = r["ecrm:P7_took_place_at"][0]["value"]
    loc = get_location(url)
    return loc

@functools.lru_cache(maxsize=None)
def get_location(url):
    r = requests.get(url, headers=headers).json()
    return r["am:displayValue"][0]["value"]

def get_date(url):
    r = requests.get(url, headers=headers).json()



columns = []

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
        "title": get_title(r["am:nameTitle"][0]["value"]),
        "description": r["dc:description"][0]["value"],
        "materials": get_material_url(r["ecrm:P45_consists_of"]),
        "from_location": get_location_url(r["ecrm:P108i_was_produced_by"][0]["value"]),
        "culture": r["am:culturalOrigin"][0]["value"],
        "date_description"
    }

    print(json.dumps(data, indent=4))
