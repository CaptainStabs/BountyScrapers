import csv
import json
import os
import re
import signal
import sys
import traceback as tb
from multiprocessing import Pool
from pathlib import Path
from utils import get_dates

import pandas as pd
import requests
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


def scraper(filename):
    # if os.path.exists(filename) and os.stat(filename).st_size > 515:
    #     start_id = get_last_id(filename, 515)
    # else:
    #     start_id = start_num

    columns = ['object_number', 'institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', 'credit_line', 'date_description', 'from_location', 'category', 'dimensions',  'description', 'materials', 'title', 'image_url', 'source_1', 'source_2', 'maker_full_name', 'maker_birth_year', 'maker_death_year', 'maker_role', 'drop_me']

    remove_escaped = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    with open("no_desc.csv", "r", encoding='utf-8') as input_csv:
        line_count = len([line for line in input_csv.readlines()])
        input_csv.seek(0)
        header = input_csv.readline().strip("\n").split(",")
        print(header)
        input_csv.seek(0)
        reader = csv.DictReader(input_csv)

        with open(filename, "a", encoding='utf-8', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=header)

            if os.stat(filename).st_size == 0:
                writer.writeheader()

            s = requests.Session()

            headers = {'host': 'api.smb.museum','Content-Type': 'text/plain'}
            s2 = requests.Session()

            s2.headers.update(headers)

            for row in tqdm(reader, total=line_count):
            # for page in range(start_id, end_num):
                url = row["source_1"]
                try:
                    jd = url_get(url, s)
                except KeyboardInterrupt:
                    return
                if not jd: continue

                try:
                    data = row
                    desc = jd.get("longDescription")
                    if desc:
                        if desc == "[SM8HF]":
                            desc = None

                    data["description"] = desc
                    data["current_location"] = jd.get("exhibitionSpace")

                    writer.writerow(data)

                    # with lock:
                    #     bar.update(1)

                except KeyboardInterrupt:
                    return

                except Exception:
                    print("\nCRASHED ID:",url)
                    tb.print_exc()
                    # print(json.dumps(jd, indent=4))
                    raise


scraper("descriptions_added.csv")
