import csv
import json
import os

import pandas as pd
import requests
from tqdm import tqdm

import logging; logging.basicConfig(level=logging.INFO)

def url_get(url, s):
    x = 0
    while x < 5:
        try:
            r = s.get(url)
        except:
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

def dimensions(dim):
    if len(list(set(list(dim.values())))) != 1:
        dimension = " x ".join([str(dim["height"]), str(dim["width"]), str(dim["depth"]), str(dim["diameter"])])
        dimension = " ".join([dimension, str(dim["unitLength"])])
        if not isinstance(dim["weight"], type(None)):
            dimension = " ".join([dimension, str(dim["weight"]), dim["unitWeight"]])
        return dimension
    else:
        return ""

if __name__ == '__main__':
    filename = "extracted_data.csv"
    if os.path.exists(filename) and os.stat(filename).st_size > 283:
        df = pd.read_csv(filename)

        # Get the last row from df
        last_row = df.tail(1)
        # Access the corp_id
        last_id = last_row["drop_me"].values[0]
        last_id += 1
        # last_id = 3169
    else:
        last_id = 1

    columns = [
        "object_number",
        "institution_name",
        "institution_city",
        "institution_state",
        "institution_country",
        "institution_latitude",
        "institution_longitude",
        "category",
        "title",
        "description",
        "dimensions", #
        "accession_year",
        "credit_line",
        "source_1",
        "date_description",
        "from_location",
        "maker_full_name",
        "maker_role",
        "year_start",
        "year_end",
        "accession_number",
        "drop_me"
        ]
    with open(filename, "a", encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        for id in tqdm(range(last_id, 999999)):
            try:
                s = requests.Session()

                url = f"https://api.maas.museum/v2/objects/{id}"
                jd = url_get(url, s)
                if not jd: continue

                data = {
                    "object_number": jd["_id"],
                    "accession_number": jd["registrationNumber"],
                    "institution_name": "Museum of Applied Arts & Sciences",
                    "institution_city": "Ultimo",
                    "institution_state": "New South Wales",
                    "institution_country": "Australia",
                    "institution_latitude": -33.87848680715133,
                    "institution_longitude": 151.19954179528983,
                    "category": "|".join(jd["category"]),
                    "title": jd["title"],
                    "description": jd["description"][:10000],
                    "dimensions": dimensions(jd['dimensions']),
                    "accession_year": jd["accessionedYear"],
                    "source_1": url,
                    "drop_me": id,
                }

                events = jd["events"]
                years = jd["years"]
                history = jd["history"]

                if len(events):
                    data["date_description"] = "|".join([x['date'] for x in events if not isinstance(x['date'], type(None))])
                    data["from_location"] = "|".join([x['place'] for x in events if not isinstance(x['place'], type(None))])[:4000]
                    data["maker_full_name"] = "|".join([str(x['creator']) for x in events])
                    data["maker_role"] = "|".join([x['role'] for x in events])

                if len(history) and not len(events):
                    logging.info("Using history not events")
                    data["date_description"] = "|".join([x['date'] for x in history if not isinstance(x['date'], type(None))])
                    data["from_location"] = "|".join([x['place'] for x in history if not isinstance(x['place'], type(None))])[:4000]
                    data["maker_full_name"] = "|".join([str(x['creator']) for x in history])
                    data["maker_role"] = "|".join([x['role'] for x in history])

                if len(jd["production"]) and not len(events) and not len(history):
                    prod = jd["production"]
                    logging.info("Using production not events or history")
                    data["date_description"] = "|".join([x['date'] for x in prod if not isinstance(x['date'], type(None))])
                    data["from_location"] = "|".join([x['place'] for x in prod if not isinstance(x['place'], type(None))])[:4000]
                    data["maker_full_name"] = "|".join([str(x['creator']) for x in prod])
                    data["maker_role"] = "|".join([x['role'] for x in prod])


                if len(years) and "date_description" not in data.keys():
                    logging.info("Adding date_description from years")
                    data["date_description"] = "-".join([years[0], years[-1]])

                if len(years):
                    data["year_start"] = years[0]
                    data["year_end"] = years[-1]

                if "acquisitionCreditLine" in jd.keys():
                    data["credit_line"] = jd["acquisitionCreditLine"]

                writer.writerow(data)

            except Exception as e:
                print("\n",id)
                print(json.dumps(jd, indent=4))
                raise e
