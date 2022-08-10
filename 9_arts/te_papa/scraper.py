import csv
import json
import os
import re
import signal
import sys
import traceback as tb
from multiprocessing import Pool

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

def check_url(id, s):
    url = f"https://collections.tepapa.govt.nz/object/{id}"
    r = s.head(url)

    if r.status_code == 200:
        return url
    else:
        return

def get_contrib(jd, name=False, location=False):
    if name:
        names = None
        if "production" in jd.keys():
            names = "|".join([x.get("contributor", {}).get("title") if x.get("contributor", {}).get("title") else "" for x in jd["production"]])
        elif "evidenceFor" in jd.keys():
            rec_by = jd["evidenceFor"]["atEvent"].get("recordedBy", [])
            if len(rec_by):
                names = "|".join([x.get("title") if x.get("title") else "" for x in rec_by])
        # else:
        #     print(json.dumps(jd, indent=2))
        #     print(" [!!!] Neither production or evidenceFor, name")

        return names

    if location:
        locations = None
        if "production" in jd.keys():
            locations = "|".join([x.get("spatial", {}).get("title") if x.get("spatial", {}).get("title") else "" for x in jd["production"]]) if len(jd["production"]) else None
            if locations == "|":
                locations = None

        elif "evidenceFor" in jd.keys():
            loc_stuff = jd["evidenceFor"].get("atEvent", {}).get("atLocation", {})
            title_country = [loc_stuff.get("title"), loc_stuff.get("country")]
            locations = ",".join([x for x in title_country if x])
        # else:
        #     print(json.dumps(jd, indent=2))
        #     print(" [!!!] Neither production nor evidenceFor, location")
        return locations

def get_dates(jd, start=False, end=False, desc=False):
    if "evidenceFor" in jd.keys():
        at_event = jd["evidenceFor"].get("atEvent", {})

        if start:
                eventDate = at_event.get("eventDate")
                if eventDate:
                    ed = eventDate.split("-")[0]
                    if ed:
                        ed = "".join(filter(str.isdigit, ed))
                else:
                    ed = None
                return ed

        if desc:
            return at_event.get("verbatimEventDate")
    elif "production" in jd.keys():
        if len(jd["production"]):
            prod = jd["production"]
            if desc:
                descs = "|".join([x.get("createdDate") if x.get("createdDate") else "" for x in prod])
                if descs == "|": descs = None
                return descs
            elif start:
                start = prod[0]["verbatimCreatedDate"].split("-")[0] if prod[0].get("verbatimCreatedDate") else None
                if start:
                    start = "".join(filter(str.isdigit, start))
                return start

            elif end:
                end_d = prod[0]["verbatimCreatedDate"].split("-")[-1] if prod[0].get("verbatimCreatedDate") else None
                if end_d:
                    return "".join(filter(str.isdigit, end_d))
    else:
        return

def scraper(filename, start_num=False, end_num=False):
    # filename, start_num, end_num = filename[0], filename[1], filename[2]
    # signal.signal(signal.SIGINT, signal.SIG_IGN)
    print(start_num, end_num, filename)
    if os.path.exists(filename) and os.stat(filename).st_size > 515:
        start_id = get_last_id(filename, 515)
    else:
        start_id = start_num
    print(start_id)
    columns = ["object_number","institution_name","institution_city","institution_state","institution_country","institution_latitude","institution_longitude","category","title","description","dimensions","materials","technique","from_location","date_description","year_start","year_end","maker_full_name","maker_birth_year","maker_death_year","maker_role","accession_number","image_url","source_1","source_2", "drop_me"]

    remove_escaped = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()
        headers = {
      'Content-Type': 'application/json',
      'x-api-key': 'v8iPNJ2a5UNJE3MJrqITiUFE3sPnoOTc4fB8iCij', # api was hardcoded into website
        }
        s = requests.Session()
        s.headers.update(headers)
        for id in tqdm(range(start_id, end_num)):
            try:
                url = f"https://data.tepapa.govt.nz/collection/object/{id}"
                jd = url_get(url, s)
                if not jd: continue

                data = {
                    "institution_name": "Museum of New Zealand Te Papa Tongarewa",
                    "institution_city": "Wellington",
                    "institution_state": "",
                    "institution_country": "New Zealand",
                    "institution_latitude": -41.29044416649501,
                    "institution_longitude": 174.78208939970705,
                    "object_number": jd["id"],
                    "category": jd["collection"],
                    "title": jd.get("title"),
                    "maker_full_name": get_contrib(jd, name=True),
                    "maker_role": "|".join([x.get("role") if x.get("role") else "" for x in jd["production"]]) if jd.get("production") else None,
                    "maker_birth_year": "|".join([x.get("contributor", {}).get("birthDate").split("-")[0] if x.get("contributor", {}).get("birthDate") else "" for x in jd["production"]]) if jd.get("production") else None,
                    "maker_death_year": "|".join([x.get("contributor", {}).get("deathDate").split("-")[0] if x.get("contributor", {}).get("deathDate") else "" for x in jd["production"]]) if jd.get("production") else None,
                    "technique": "|".join([x.get("title") for x in jd["productionUsedTechnique"]]) if jd.get("productionUsedTechnique") else None,
                    "category": "|".join([x.get("title") for x in jd["isTypeOf"]]) if "isTypeOf" in jd.keys() else None,
                    "materials": "|".join([x.get("title") for x in jd["isMadeOf"]]) if "isMadeOf" in jd.keys() else None,
                    "source_1": url,
                    "source_2": check_url(id, s),
                    "image_url": jd.get("hasRepresentation", [])[0].get("contentUrl") if len(jd.get("hasRepresentation", [])) else None,
                    "description": jd.get("caption"),
                    "accession_number": jd.get("identifier"),
                    "dimensions": "|".join([x["title"] for x in jd.get("observedDimension") if x.get("title")]) if len(jd.get("observedDimension", [])) else None,
                    "from_location": get_contrib(jd, location=True),
                    "date_description": get_dates(jd, desc=True),
                    "year_start": get_dates(jd, start=True),
                    "year_end": get_dates(jd, end=True),
                    "drop_me": id,
                }

                writer.writerow(data)

            except Exception:
                print("\n",id)
                print(json.dumps(jd, indent=4))
                send_mail("script crashed", "")
                raise

# if __name__ == "__main__":
#         arguments = []
#         end_id = 5176 #45899
#         # start_num is supplemental for first run and is only used if the files don't exist
#         for i in range(5):
#             if i == 0:
#                 start_num = 0
#             else:
#                 # Use end_id before it is added to
#                 start_num = end_id - 5176
#             print("Startnum: " + str(start_num))
#             arguments.append([f"./files/extracted_data{i}.csv", start_num, end_id])
#             end_id = end_id + 5176
#         print(arguments)
#
#         try:
#             pool = Pool(processes=len(arguments))
#             pool.starmap(scraper, arguments)
#             # for _ in tqdm(pool.istarmap(scraper, arguments), total=len(arguments)):
#             #     pass
#             pool.close()
#             send_mail("Finished", "")
#             # pool.starmap(scraper, arguments), total=len(arguments)
#         except KeyboardInterrupt:
#             print("Quitting")
#             pool.terminate()
#             sys.exit()
#         except Exception as e:
#             raise(e)
#             print(e)
#             tb.print_exc()
#             pool.terminate()
#         finally:
#             print("   [*] Joining pool...")
#             pool.join()
#             send_mail("Scraper crashed", "")
#             sys.exit()
#             print("   [*] Finished joining...")
#             sys.exit(1)

scraper("extracted_data.csv", 0, 25878)
