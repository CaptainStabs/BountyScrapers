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


def url_get(url, p,  s):
    x = 0
    while x < 5:
        try:
            r = s.post(url, data=p)
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
# "|".join([",".join([x.get("RecordType", ""), x.get("Role", "")]) if x["RecordType"] or x["Role"] else "" for x in artists]),
def get_roles(artists):
    r_list = []
    for info in artists:
        rec_type = info["RecordType"]
        role = info["Role"]
        if rec_type and role:
            r_list.append(",".join([rec_type, role]))
        elif rec_type and not role:
            r_list.append(str(rec_type) + ",")
        elif role and not rec_type:
            r_list.append("," + str(role))

        return "|".join(r_list)

def scraper(filename, start_num=False, end_num=False):
    # filename, start_num, end_num = filename[0], filename[1], filename[2]
    # signal.signal(signal.SIGINT, signal.SIG_IGN)
    print(start_num, end_num, filename)
    if os.path.exists(filename) and os.stat(filename).st_size > 515:
        start_id = get_last_id(filename, 515)
    else:
        start_id = start_num
    print(start_id)
    columns = ["object_number","institution_name","institution_city","institution_state","institution_country","institution_latitude","institution_longitude","category","title","description","dimensions", "current_location","materials","from_location","date_description","maker_full_name","maker_first_name","maker_last_name","maker_birth_year","maker_death_year","maker_role","accession_number", "credit_line", "image_url","source_1","source_2", "drop_me"]

    remove_escaped = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()
        headers = {
            'host': 'smaapi.unit.ku.edu',
        }
        s = requests.Session()
        s.headers.update(headers)
        url = "https://smaapi.unit.ku.edu/sma/fetch-object"
        for id in tqdm(range(start_id, end_num)):
            try:

                pay =  "\r\n{\"objectID\":\"REP\"}".replace("REP", str(id))
                jd = url_get(url, pay, s)
                if not jd: continue

                obj_info = jd.get("objectInformation", [])
                if len(jd.get("objectInformation", [])) > 1:
                    print(json.dumps(obj_info, indent=2))
                    print(" [???] objectInformation greater than 1")

                if len(obj_info):
                    obj_info = obj_info[0]
                else: continue

                artists = jd.get("multipleArtists", [])

                t = [x["Role"] for x in artists if x["Role"]]
                if t:
                    print("Role is not null", t)
                    print([x["RecordType"] for x in artists if x["RecordType"]])
                data = {
                    "institution_name": "Spencer Museum of Art",
                    "institution_city": "Lawrence",
                    "institution_state": "Kansas",
                    "institution_country": "United States",
                    "institution_latitude": 38.959665913773726,
                    "institution_longitude": -95.24450747806205,
                    "object_number": obj_info.get("ObjID") if obj_info else None,
                    "title": obj_info.get("Title"),
                    "category": obj_info.get("ObjectType"),
                    "materials": "|".join([x for x in obj_info.get("MaterialTechnique").split(", ") if x]),
                    "from_location": obj_info.get("GeogAssoc"),
                    "credit_line": obj_info.get("CreditLine"),
                    "description": obj_info.get("Description")[:10000] if jd.get("Description") else None,
                    "accession_number": obj_info.get("AccessionNum"),
                    "current_location": obj_info.get("CurrentLocation"),
                    "date_description": obj_info.get("Date"),
                    "maker_full_name": "|".join([x["FirstSortConcat"] if x["FirstSortConcat"] else "" for x in artists]),
                    "maker_first_name": "|".join([x["FirstName"] if x["FirstName"] else "" for x in artists]),
                    "maker_last_name": "|".join([x["SortName"] if x["SortName"] else "" for x in artists]),
                    "maker_birth_year": "|".join([x["Date"].split("–")[0] if x["Date"] else "" for x in artists]),
                    "maker_death_year": "|".join([x["Date"].split("–")[-1] if x["Date"] and "–" in x["Date"] else "" for x in artists]),
                    # "maker_role": "|".join([",".join([x.get("RecordType", ""), x.get("Role", "")]) if x["RecordType"] or x["Role"] else "" for x in artists]),
                    "maker_role": get_roles(artists),
                    "dimensions": "|".join(x["Dimensions"] for x in jd.get("objectDimensions", {}) if x["Dimensions"]),
                    "image_url": "https://smaapi.app.ku.edu/api/media/{}/full".format(obj_info.get("MulID")) if obj_info.get("MulID") else None,
                    "source_1": "https://smaapi.unit.ku.edu/sma/fetch-object",
                    "source_2": f"https://spencerartapps.ku.edu/collection-search#/object/{id}",
                    "drop_me": id,
                }

                writer.writerow(data)

            except Exception as e:
                print("\n",id)
                # send_mail("script crashed", "")
                print(json.dumps(jd, indent=4))
                print(e)
                raise(e)

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

scraper("extracted_data.csv", 3, 99999)
