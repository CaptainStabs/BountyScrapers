import csv
import json
import os
import re
import signal
import sys
import traceback as tb
from multiprocessing import Pool
from html import unescape


# import _istarmap
import pandas as pd
import requests
from tqdm import tqdm

import logging; logging.basicConfig(level=logging.INFO)

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

def get_last_id(filename):
    if os.path.exists(filename) and os.stat(filename).st_size > 250:
        df = pd.read_csv(filename)
        df_columns = list(df.columns)
        data_columns = ",".join(map(str, df_columns))

        # Get the last row from df
        last_row = df.tail(1)
        # Access the corp_id
        last_id = last_row["drop_me"].values[0]
        last_id += 1
        return last_id
    else:
        last_id = 1
        return

html_remover = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

def scraper(filename, start_num=False, end_num=False):
    # filename, start_num, end_num = filename[0], filename[1], filename[2]
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    print(start_num, end_num, filename)
    if os.path.exists(filename) and os.stat(filename).st_size > 377:
        start_id = get_last_id(filename)
    else:
        start_id = start_num

    columns = [
        "object_number",
        "institution_name",
        "institution_city",
        "institution_state",
        "institution_country",
        "institution_latitude",
        "institution_longitude",
        "title", # displaytitle
        "department",
        "category", # classification
        "year_start", # datebegin
        "year_end", # dateend
        "date_description", #daterange
        "materials", #medium
        "dimensions", #dimensions
        "credit_line", #creditline
        "inscription", # markings or inscribed
        "accession_year",  # accessionyear,
        "image_url",  # primaryimage?
        "from_location", # geography -> [displaygeography]
        "culture", # displayculture
        "description", #caption
        "maker_full_name", # makers
        "maker_role", # makers -> role
        "maker_birth_year", # datebegin
        "maker_death_year", # dateend
        "source_1",
        "drop_me"
        ]

    remove_escaped = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    with open(filename, "a", encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        s = requests.Session()
        for id in tqdm(range(start_id, end_num)):
            try:
                url = f"https://data.artmuseum.princeton.edu/objects/{id}"
                jd = url_get(url, s)
                if not jd: continue

                data = {
                    "object_number": jd["objectnumber"],
                    "institution_name": "Princeton University Art Museum",
                    "institution_city": "Princeton",
                    "institution_state": "New Jersey",
                    "institution_country": "United Stated",
                    "institution_latitude": 40.34771360812758,
                    "institution_longitude": -74.65811190186194,
                    "title": jd["displaytitle"],
                    "department": jd["department"],
                    "category": jd["classification"],
                    "year_start": jd["datebegin"],
                    "year_end": jd["dateend"],
                    "date_description": jd["daterange"],
                    "materials": jd["medium"],
                    "dimensions": jd["dimensions"],
                    "credit_line": jd["creditline"],
                    "source_1": url,
                    "drop_me": id

                }

                if not data["year_start"]:
                    data["year_start"] = None
                if not data["year_end"]:
                    data["year_end"] = None

                if jd["inscribed"]:
                    data["inscription"] = jd["inscribed"]
                elif jd["markings"]:
                    data["inscription"] = jd["markings"]

                if len(jd["primaryimage"]):
                    data["image_url"] = jd["primaryimage"][0]
                elif len(jd["media"]):
                    print("Not primaryimage, using media")
                    data["image_url"] = jd["media"][0]["uri"]

                if len(jd["geography"]):
                    data["from_location"] = jd["geography"][0]["displaygeography"]

                if len(jd["cultures"]):
                    data["culture"] = "|".join([x["displayculture"] for x in jd["cultures"]])

                texts = [x["textpurpose"] for x in jd["texts"]]
                if len(jd["texts"]) and "Description" in texts:
                    index = texts.index("Description")
                    data["description"] = unescape(re.sub(html_remover, '', jd["texts"][index]["textentryhtml"])).replace("\n", "")[:10000]
                elif jd["caption"]:
                    data["description"] = jd["caption"]

                makers = jd["makers"]
                if len(makers):
                    data["maker_full_name"] = "|".join([x["displayname"] for x in makers])
                    data["maker_role"] = "|".join([x["role"] for x in makers])
                    data["maker_birth_year"] = "|".join([str(x["datebegin"]) for x in makers])
                    data["maker_death_year"] = "|".join([str(x["dateend"])  for x in makers])

                try:
                    data["accession_year"] =  jd["accessionyear"].split("-")[0]
                except AttributeError:
                    pass

                writer.writerow(data)

            except Exception as e:
                print("\n",id)
                print(json.dumps(jd, indent=4))
                print(e)
                raise(e)

if __name__ == "__main__":
    arguments = []
    end_id = 10307
    # start_num is supplemental for first run and is only used if the files don't exist
    for i in range(10):
        if i == 0:
            start_num = 0
        else:
            # Use end_id before it is added to
            start_num = end_id - 10307
        print("Startnum: " + str(start_num))
        arguments.append([f"./files/extracted_data{i}.csv", start_num, end_id])
        end_id = end_id + 10307
    print(arguments)

    # scraper("test.csv", 2496, 2510)
    try:
        pool = Pool(processes=len(arguments))
        pool.starmap(scraper, arguments)
        # for _ in tqdm(pool.istarmap(scraper, arguments), total=len(arguments)):
        #     pass
        pool.close()
        # pool.starmap(scraper, arguments), total=len(arguments)
    except KeyboardInterrupt:
        print("Quitting")
        pool.terminate()
        sys.exit()
    except Exception as e:
        raise(e)
        print(e)
        tb.print_exc()
        pool.terminate()
    finally:
        print("   [*] Joining pool...")
        pool.join()
        sys.exit()
        print("   [*] Finished joining...")
        sys.exit(1)
# # # 2496
