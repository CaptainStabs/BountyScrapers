import csv
import json
import os
import re
import signal
import sys
import traceback as tb
from multiprocessing import Pool

import pandas as pd
import math
import requests
from tqdm import tqdm
import sys
import logging; logging.basicConfig(level=logging.INFO)
from pathlib import Path
import re
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

def scraper(filename, mus_info, org_id):
    # filename, start_num, end_num = filename[0], filename[1], filename[2]
    # signal.signal(signal.SIGINT, signal.SIG_IGN)
    print(filename)
    if os.path.exists(filename) and os.stat(filename).st_size > 515:
        start_pg = get_last_id(filename, 515)
    else:
        start_pg = 1
    print(start_pg)
    columns = ["object_number","institution_name","institution_city","institution_state","institution_country","institution_latitude","institution_longitude","category","title","description", "culture", "materials","from_location","date_description", "maker_full_name","maker_birth_year","maker_death_year","image_url", "credit_line", "source_1","source_2", "drop_me"]

    remove_escaped = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    dates_pat = re.compile(r"\((.*?)\)")
    by_pat = re.compile(r"^By *")
    num_only = re.compile(r"[^0-9-]")
    names_only = re.compile(r"\([^)]*\)")

    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()
        headers = {
          'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
          'Accept': 'application/json, text/plain, */*',
          'DNT': '1',
          'sec-ch-ua-mobile': '?0',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
          'x-api-key': 'aaa',
          'sec-ch-ua-platform': '"Windows"',
          'Sec-Fetch-Site': 'same-origin',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Dest': 'empty',
          'host': 'colbase.nich.go.jp'
        }
        s = requests.Session()
        s.headers.update(headers)

        url = f"https://colbase.nich.go.jp/colbaseapi/v2/collection_items?locale=en&page=1&limit=100&with_image_file=0&only_parent=0&organization_id={org_id}"
        result_set = url_get(url, s)["resultset"]

        count, limit = result_set["count"], result_set["limit"]
        end_pg = math.ceil(count / limit) # Get whole number of pages

        for page in tqdm(range(start_pg, end_pg)):
            url = f"https://colbase.nich.go.jp/colbaseapi/v2/collection_items?locale=en&page={page}&limit=100&with_image_file=0&only_parent=0&organization_id={org_id}"

            jd = url_get(url, s)
            if not jd: continue
            # make sure to save page to allow resuming

            for item in jd["results"]:
                try:
                    dates = re.findall(dates_pat, item["sakusha"]) if item["sakusha"] else None
                    dates = dates[0] if dates else None

                    if dates:
                        death = dates.split("-")[-1] if len(dates.split("-")) > 1 else None
                    else:
                        death = None

                    data = {
                        "institution_name": mus_info["institution_name"],
                        "institution_city": mus_info["institution_city"],
                        "institution_state": mus_info["institution_state"],
                        "institution_country": mus_info["institution_country"],
                        "institution_latitude": mus_info["institution_latitude"],
                        "institution_longitude": mus_info["institution_longitude"],
                        "object_number": item["organization_item_key"],
                        "category": item["bunrui"],
                        "culture": item["bunkazai"],
                        "title": item["title"],
                        "maker_full_name": "|".join(re.findall(re.compile(r"( and |, |;)")), re.sub(by_pat, "", re.sub(names_only, "", item["sakusha"])).replace("Compiled by", "").replace("illustrated by", "").replace("Illustrated by", "") if item["sakusha"] else None,
                        "maker_birth_year": dates.split("-")[0] if dates else None,
                        "maker_death_year": death,
                        "materials": "|".join(item["hinshitu_keijo"].split(" and ")) if item["hinshitu_keijo"] else None,
                        "from_location": item["seisakuchi"],
                        "credit_line": item["kizousha"],
                        "source_1": url,
                        "source_2": f"https://colbase.nich.go.jp/collection_items/tnm/{item['organization_item_key']}" if item["organization_item_key"] else None,
                        "image_url": item["thumbnail_url"],
                        "description": item.get("descriptions", [])[0].get("text").replace("\n", "") if item.get("descriptions") else None,
                        "date_description": item["jidai_seiki"],
                        "drop_me": page,
                    }

                    writer.writerow(data)

                except Exception:
                    print("\n",id)
                    print(json.dumps(jd))
                    # send_mail("script crashed", "")
                    raise

# if __name__ == "__main__":
#         arguments = []
#         end_id = 9180 #45899
#         # start_num is supplemental for first run and is only used if the files don't exist
#         for i in range(10):
#             if i == 0:
#                 start_num = 0
#             else:
#                 # Use end_id before it is added to
#                 start_num = end_id - 9180
#             print("Startnum: " + str(start_num))
#             arguments.append([f"./files/extracted_data{i}.csv", start_num, end_id])
#             end_id = end_id + 9180
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
            # sys.exit(1)

mus_info = {
    "institution_name": "Tokyo National Museum",
    "institution_city": "Taito",
    "institution_state": "Tokyo",
    "institution_country": "Japan",
    "institution_latitude": 35.71887280999633,
    "institution_longitude": 139.77652834061385
}
scraper("tnm_extracted_data.csv", mus_info, 1)
