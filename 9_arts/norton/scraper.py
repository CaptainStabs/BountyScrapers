import csv
import json
import math
import os
import re
import sys
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
    columns = ['institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', 'image_url', 'title', 'date_description', 'maker_full_name', 'maker_birth_year', 'maker_death_year', 'object_number', 'culture', 'materials', 'credit_line', 'source_1', 'year_start', 'year_end', 'drop_me']


    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()
        s = requests.Session()
        headers = {
          'Accept': '*/*',
          'X-Requested-With': 'XMLHttpRequest'
        }
        s.headers.update(headers)

        url = f"https://www.nortonsimon.org/art/search-the-collection/search?offset=0&length=100&sort=1&show_only=&artists=&title=&select_earliest_year=&select_latest_year=&earliest_year=&latest_year=&object_type=&accession_id=&material="
        result_set = url_get(url, s)

        count = result_set["total"]
        end_pg = math.ceil(count / limit) # Get whole number of pages

        dates_pat = re.compile(r"\d{4}-\d{4}|\d{4}-")

        for page in tqdm(range(start_pg, end_pg)):
            url = f"https://www.nortonsimon.org/art/search-the-collection/search?offset={page}&length=100&sort=1&show_only=&artists=&title=&select_earliest_year=&select_latest_year=&earliest_year=&latest_year=&object_type=&accession_id=&material="

            jd = url_get(url, s).get("records", [])
            if not len(jd): continue
            # make sure to save page to allow resuming

            for item in jd:
                try:
                    dates = re.findall(dates_pat, item["maker_bio"]) if item["maker_bio"] else None
                    if dates and len(dates) > 1:
                        print("[!!!] Dates > 1", dates)
                    dates = dates[0] if dates else None
                    # dates = re.sub(num_only, "", dates) if dates else None
                    dates = dates.split("-") if dates else None

                    if dates:
                        death = dates[-1] if len(dates) > 1 else None
                    else:
                        death = None

                    data = {
                        "institution_name": mus_info["institution_name"],
                        "institution_city": mus_info["institution_city"],
                        "institution_state": mus_info["institution_state"],
                        "institution_country": mus_info["institution_country"],
                        "institution_latitude": mus_info["institution_latitude"],
                        "institution_longitude": mus_info["institution_longitude"],
                        "image_url": "https:" + item["desktopimage"],
                        "title": item["title"],
                        "date_description": item["dateMade"],
                        "maker_full_name": "|".join(item["maker_firstlast"].split(", ")),
                        "maker_birth_year": dates[0] if dates else None,
                        "maker_death_year": death,
                        "object_number": item["link"].split("/")[-1 ],
                        "culture": item["culture"],
                        "materials": item["materials"],
                        "credit_line": item["credit_line"],
                        "source_1": item["link"],
                        "year_start": item["earliest_year"],
                        "year_end": item["latest_year"],
                        "drop_me": page,
                    }

                    writer.writerow(data)

                except Exception:
                    print("\n",id)
                    print(json.dumps(jd))
                    # send_mail("script crashed", "")
                    raise

mus_info = {
    "institution_name": "Norton Simon Museum",
    "institution_city": "Pasadena",
    "institution_state": "California",
    "institution_country": "United States",
    "institution_latitude": 34.146348732221114,
    "institution_longitude": -118.1592639318127
}
scraper("extracted_data.csv", mus_info)
