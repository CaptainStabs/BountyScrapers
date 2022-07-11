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

def scraper(filename, start_num=False, end_num=False):
    # filename, start_num, end_num = filename[0], filename[1], filename[2]
    # signal.signal(signal.SIGINT, signal.SIG_IGN)
    print(start_num, end_num, filename)
    if os.path.exists(filename) and os.stat(filename).st_size > 515:
        start_id = get_last_id(filename, 515)
    else:
        start_id = start_num
    print(start_id)
    columns = ["object_number","institution_name","institution_city","institution_state","institution_country","institution_latitude","institution_longitude","category","title","description","dimensions","inscription","provenance","materials","technique","from_location","date_description","year_start","year_end","maker_full_name","maker_first_name","maker_last_name","maker_birth_year","maker_death_year","maker_role","maker_gender","accession_number","image_url","source_1","source_2", "drop_me"]

    remove_escaped = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        s = requests.Session()
        for id in tqdm(range(start_id, end_num)):
            try:
                url = f"https://www.warmuseum.ca/_api/en/collections/artifact/{id}"
                jd = url_get(url, s)
                if not jd: continue
                if jd["type"] != "artifact": continue

                meta = jd["_meta_"]
                data = {
                    "institution_name": "Canadian War Museum",
                    "institution_city": "Ottawa",
                    "institution_state": "Ontario",
                    "institution_country": "Canada",
                    "institution_latitude": 45.4171028137207,
                    "institution_longitude": 75.7169418334961,
                    "object_number": jd["object_number"],
                    "maker_full_name": "|".join([x for x in jd["artist_maker"]]),
                    "category": "|".join(["|".join([x for x in jd["category"]]), "|".join([x for x in jd["classification"]])]),
                    "date_description": jd["date_made"],
                    "department": "|".join([x for x in jd["department"]]),
                    "year_start": jd["earliest"].split("/")[0] if len(jd["earliest"].split("/")) else None,
                    "inscription": jd["inscription"],
                    "year_end": jd["latest"].split("/")[0] if len(jd["latest"].split("/")) else None,
                    "material": "|".join([x for x in jd["material"]]),
                    "dimensions": jd["dimensions"],
                    "image_url": jd.get("media", [])[0].get("url") if len(media) else None,
                    "title": jd["title"],
                    "from_location": "|".join([x["country"] for x in jd["places"]["origins"]]) if len(jd["places"]["origins"]) else None,
                    "image_url": jd["media"][0]["url"] if len(jd["media"]) else None,
                    "description": jd["model"],
                    "source_1": f"https://www.warmuseum.ca/_api/en/collections/artifact/{id}",
                    "source_2": f"https://www.warmuseum.ca/_api/en/collections/artifact/{id}",
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

scraper("extracted_data.csv", 0, 2220758)
