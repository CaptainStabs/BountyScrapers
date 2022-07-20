import csv
import json
import math
import os
import re
import sys
import time
from pathlib import Path

import requests
from tqdm import tqdm

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

            if r.status_code == 429:
                print("\nSleeping for:", r.headers["retry-after"])
                time.sleep(int(r.headers["retry-after"]))
            print(r)
            # if x == 4:
            #     raise(e)
        x += 1

def scraper(filename, mus_info, limit=100):
    # filename, start_num, end_num = filename[0], filename[1], filename[2]
    # signal.signal(signal.SIGINT, signal.SIG_IGN)
    print(filename)
    if os.path.exists(filename) and os.stat(filename).st_size > 515:
        start_pg = get_last_id(filename, 515) - 1
    else:
        start_pg = 0
    print(start_pg)

    columns = ['institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', 'id', 'title', 'maker_full_name', 'maker_gender', 'maker_birth_year', 'maker_death_year', 'image_url', 'date_description', 'year_start', 'year_end', 'acccession_number', 'drop_me', 'source_1']
    dates_pat = re.compile(r"(\d{4}|\d{3} \d{4}|\d{3})")
    name_pat = re.compile(r", | and ")
    pat1 = re.compile(r"(?:(?:(\d{4}|\d{3})\/)|(:?|\d{4}|\d{3}))(?:(\d{4}|\d{3})|(\d{4}|\d{3})(?:\)))")
    pat2 = re.compile(r"((\d{4}|\d{3}) - (\d{4}|\d{3})-(\d{4}|\d{3}))|((?!\d)(\d{4}|\d{3}) - |(\d{4}|\d{3})-(\d{4}|\d{3}) - (\d{4}|\d{3}))")

    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        s = requests.Session()
        headers = {'host': 'api.chazen.wisc.edu'}
        s.headers.update(headers)

        url = "https://api.chazen.wisc.edu/api/artwork?page=1"
        meta = url_get(url, s)["meta"]

        end_pg = meta["last_page"]

        for page in tqdm(range(start_pg, end_pg)):
            url = f"https://api.chazen.wisc.edu/api/artwork?page={page}"

            jd = url_get(url, s).get("data", [])
            if not len(jd): continue
            # make sure to save page to allow resuming

            for item in jd:
                try:

                    artist = item["primary_artist"]

                    if artist:
                        bio = artist["bio"].replace(" \u2013 ", "-").replace("\u2013", "-") if artist["bio"] else None
                        # dates = re.findall(dates_pat, bio) if bio else None
                        # if dates and len(dates) > 2:
                        #     print("[!!!] Dates > 1", json.dumps(artist, indent=2))
                        #     # print("\nNames:", artist["display_name"], "\nDates:", artist["bio"])
                        if bio:
                            if re.findall(pat2, bio):
                                print("\nAAAA")
                                years = bio.split(" - ")
                                years = [y.replace("-", "/").strip("(").strip(")") for y in years]
                                years[0] = years[0].split(",")[1].strip() if len(years[0].split(",")) > 1 else years[0]

                            elif "/" not in bio:
                                years = re.findall(dates_pat, bio)
                            elif "/" in bio:
                                years = re.findall(pat1, bio)
                                years = [tuple(y for y in tup if y != '') for tup in years]
                                years = ["/".join(y) for y in years]


                            birth_years = "|".join([years[i] for i in range(0, len(years), 2)])
                            death_years = "|".join([years[i] for i in range(1, len(years), 2)])
                            if len(birth_years):
                                birth = birth_years
                            else:
                                birth = None
                            if len(death_years):
                                death = death_years
                            else:
                                death = None
                    else:
                        birth, death = None, None

                    years = re.findall(dates_pat, item["date"]) if item["date"] else None
                    if years:
                        yr_strt = years[0]
                        yr_end = years[-1] if len(years) > 1 else None
                    else:
                        yr_strt, yr_end = None, None

                    data = {
                        "institution_name": mus_info["institution_name"],
                        "institution_city": mus_info["institution_city"],
                        "institution_state": mus_info["institution_state"],
                        "institution_country": mus_info["institution_country"],
                        "institution_latitude": mus_info["institution_latitude"],
                        "institution_longitude": mus_info["institution_longitude"],
                        "id": item["id"],
                        "title": item["title"],
                        "maker_full_name": "|".join(re.split(name_pat, artist["full_name"])) if artist else None,
                        "maker_gender": artist["gender"] if artist else None,
                        "maker_birth_year": birth,
                        "maker_death_year": death,
                        "image_url": item["preview_url"],
                        "date_description": item["date"],
                        "year_start": yr_strt,
                        "year_end": yr_end,
                        "accession_number": item["accession_number"],
                        "source_1": url,
                        "drop_me": page,
                    }

                    writer.writerow(data)

                except Exception:
                    print("\n",id)
                    print(json.dumps(item, indent=2))
                    send_mail("script crashed", "")
                    raise

mus_info = {
    "institution_name": "Chazen Museum of Art",
    "institution_city": "Madison",
    "institution_state": "Wisconsin",
    "institution_country": "United States",
    "institution_latitude": 43.073844014010064,
    "institution_longitude": -89.39931929946827
}
scraper("extracted_data.csv", mus_info)
send_mail("FINSIHED", "FINSIHED")
