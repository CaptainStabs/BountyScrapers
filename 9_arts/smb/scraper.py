import csv
import json
import os
import re
import signal
import sys
import traceback as tb
from multiprocessing import Pool
from pathlib import Path

import pandas as pd
import requests
from dateutil import parser as dateparser
from tqdm import tqdm

import logging; logging.basicConfig(level=logging.INFO)
p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))
from _common import get_last_id
from _common.send_mail import send_mail

# import heartrate; heartrate.trace(browser=True, daemon=True)


def url_get(url, s):
    x = 0
    while x < 5:
        try:
            r = s.get(url)
        # except KeyboardInterrupt:
        #     print("Ctrl-c detected, exiting")
        #     import sys; sys.exit()
        #     raise KeyboardInterrupt
        except Exception as e:
            raise(e)
            x+=1
            continue

        if r.status_code in (404, 500, 401):
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

dates_pat = re.compile(r"((?<=\.)(\d{3,4})( - )(.*?(?<=\.)(\d{3,4})|(\d{3,4})))")
dates_pat2 = re.compile(r"(\d{3,4} - \d{3,4})")
pat1 = re.compile(r"(?:(?:(\d{4}|\d{3})\/)|(:?|\d{4}|\d{3}))(?:(\d{4}|\d{3})|(\d{4}|\d{3})(?:\)))")
pat2 = re.compile(r"((\d{4}|\d{3}) - (\d{4}|\d{3})-(\d{4}|\d{3}))|((?!\d)(\d{4}|\d{3}) - |(\d{4}|\d{3})-(\d{4}|\d{3}) - (\d{4}|\d{3}))")
born_pat = re.compile(r"(?: born )(\d{4})(?:\))")

# print(re.findall(pat, string))

def get_dates(dates: list, url) -> tuple:
    year_list = []
    for bio in dates:
        if not any(x.isdigit() for x in bio):
            year_list.append("b")
            continue

        if re.findall(born_pat, bio):
            years = re.findall(born_pat, bio)
            # print("years:", years)
            year_list.append([x for x in years])

        elif re.findall(dates_pat2, bio):
            years = re.findall(dates_pat2, bio)[0]
            year_list.append(years)

        elif "/" not in bio and re.findall(dates_pat, bio):
            years = re.findall(dates_pat, bio)[0]
            year_list.append(years[0])

        elif "/" in bio:
            year_list.append("b")
            continue

        else:
            print("UNKNOWN FORMAT:", bio, url)
            year_list.append("b")
            continue

def get_image(id, s):
    url = "https://api.smb.museum/v1/graphql"

    payload = "{\"query\":\"query FetchPrimaryAttachmentsForObjects($object_ids: [bigint!]!) {\\n  smb_objects(where: {id: {_in: $object_ids}}) {\\n    id\\n    attachments(order_by: [{primary: desc}, {attachment: asc}], limit: 1) {\\n      attachment\\n    }\\n  }\\n}\\n\",\"variables\":{\"object_ids\":[" + str(id) + "]},\"operationName\":\"FetchPrimaryAttachmentsForObjects\"}"

    r = s.post(url, data=payload)
    r = r.json()

    data = r["data"]["smb_objects"]

    if data:
        f = data[0]["attachments"]
        if f:
            img = f[0]["attachment"].strip(".jpg")
            img = "".join(["https://recherche.smb.museum/images/", img, "_1000x600.jpg"])
            return img


def scraper(filename, start_num, end_num, position, mms):
    # with open("museums.json", "r", encoding="utf-8") as f:
    #     mms = json.load(f)
    # filename, start_num, end_num = filename[0], filename[1], filename[2]
    # signal.signal(signal.SIGINT, signal.SIG_IGN)
    # print(start_num, end_num, filename)
    if os.path.exists(filename) and os.stat(filename).st_size > 515:
        start_id = get_last_id(filename, 515)
    else:
        start_id = start_num
    # print(start_id)
    columns = ['institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', 'credit_line', 'date_description', 'from_location', 'category', 'dimensions', 'from_location', 'object_number', 'description', 'materials', 'title', 'image_url', 'source_1', "maker_full_name", "maker_role", "drop_me", "maker_death_year", "maker_birth_year", "source_2"]

    remove_escaped = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        s = requests.Session()

        headers = {'host': 'api.smb.museum','Content-Type': 'text/plain'}
        s2 = requests.Session()

        s2.headers.update(headers)

        # for page in tqdm(range(start_id, end_num), desc=f"Page, t {position}", leave=False, position=position):
        for page in range(start_id, end_num):
            url = f"https://api.smb.museum/search/?offset={page}"

            jd1 = url_get(url, s)
            if not jd1: continue
            # make sure to save page to allow resuming
            # for jd in tqdm(jd1["objects"], desc="       Item", leave=False, position=position*2+1):
            try:
                jd1["objects"]
            except:
                print(json.dumps(jd1, indent=4))
            for jd in jd1["objects"]:
                try:
                    dating = "|".join(jd.get("dating", []))
                    dates = [jd.get("dateRange"), dating]
                    dates = [x for x in dates if x]

                    inst_name = jd["collection"]

                    birth_date = jd.get("involvedParties")

                    names, roles = [], []
                    birth, death = None, None
                    if birth_date:
                        birth, death = get_dates(birth_date, url)


                        for name in birth_date:
                            names.append(name.split("(")[0].strip())
                            roles.append(name.split(",")[-1].strip())


                    cate = [jd.get("technicalTerm"), jd.get("compilation")]
                    cate = [x for x in cate if x]

                    desc = jd.get("longDescription")
                    if desc:
                        if desc == "[SM8HF]":
                            desc = None

                    m = mms[inst_name]
                    data = {
                        "institution_name": inst_name,
                        "institution_city": m["city"],
                        "institution_state": m["state"],
                        "institution_country": "Germany",
                        "institution_latitude": m["lat"],
                        "institution_longitude": m["lon"],
                        "credit_line": "|".join(jd.get("acquisition", [])) if jd.get("acquisition") else None,
                        "date_description": ", ".join(dates) if dates else None,
                        "from_location": jd.get("compilation"),
                        "category": "|".join(cate),
                        "dimensions": " ".join(jd.get("dimensionsAndWeight", [])),
                        "from_location": ", ".join(jd.get("geographicalReferences", [])),
                        "object_number": jd.get("identNumber"),
                        "description": desc,
                        "materials": "|".join(jd.get("materialAndTechnique", [])),
                        "title": " | ".join(jd.get("titles", [])),
                        "image_url": get_image(jd.get("id"), s2),
                        "source_1": url,
                        "source_2": f"https://recherche.smb.museum/detail/{jd.get('id')}",
                        "maker_full_name": "|".join(names),
                        "maker_birth_year": birth,
                        "maker_death_year": death,
                        "maker_role": "|".join(roles),
                        "drop_me": page,
                    }

                    writer.writerow(data)

                except KeyboardInterrupt:
                    return

                except Exception:
                    print("\nCRASHED ID:",url)
                    tb.print_exc()
                    print(json.dumps(jd1, indent=4))
                    raise


# scraper("extracted_data.csv", 0, 9980)
