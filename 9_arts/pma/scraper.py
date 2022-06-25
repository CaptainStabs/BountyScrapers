import requests
import time
import json
import csv
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
    ]

with open(filename, "a", encoding='utf-8') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat(filename).st_size == 0:
        writer.writeheader()

    for i in range(0, 34901):
        url = f"https://hackathon.philamuseum.org/api/v0/collection/object?query={i}&api_token=jnFV09XMKDJ0yVYrcQd3si72VFN4EUeM15B479G6RkMfiu4BstY2GuaR19kI"
        r = requests.get(url, verify=False)

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
            "maker_birth_year": "|".join([x["Artist_Info"].split(",")[-1].split("-")[0].strip() for x in jd["Artists"]]),
            "maker_death_year": "|".join([x["Artist_Info"].split(",")[-1].split("-")[-1].strip() for x in jd["Artists"]]),
            "current_location": jd["Location"],
            "image_url": jd["Image"],
            "source_1": url
        }
        
        writer.writerow(data)
        break
