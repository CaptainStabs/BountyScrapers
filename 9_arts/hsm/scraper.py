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
from _common import get_last_id, send_mail


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

def dimensions(dim):
    if not dim: return
    hgt = str(dim["height"][0]) if len(dim["height"]) else None
    wid =  str(dim["width"][0]) if len(dim["width"]) else None
    dia = str(dim["diameter"][0]) if len(dim["diameter"]) else None
    dep = str(dim["depth"][0]) if len(dim["depth"]) else None
    uni = str(dim["unitLength"][0]) if len(dim["unitLength"]) else None

    d_list = [hgt, wid, dia, dep]
    dimension = " x ".join([x for x in d_list if x])

    if dimension and uni:
        dimension = " ".join([dimension, uni])

    wgt = str(dim["weight"][0]) if len(dim["weight"]) else None
    if not isinstance(wgt, type(None)):
        dimension = " ".join([dimension, str(dim["weight"][0]), dim["unitWeight"][0]])
    return dimension


def get_location(jd):
    try:
        loc = jd["origins"][0]
    except KeyError:
        loc = None
    if loc:
        place_list = []
        for i in range(0, 5, -1):
            place_list.append(",".join([x for x in loc[f"placeCreated{i}"]]))
        return ",".join(place_list)
    else:
        return

def get_image(jd):
    try:
        media = jd["multimedia"][0]
    except IndexError:
        media = None
    if media:
        img_path = media["path"]
        name = media["MulIdentifier"]
        url = "https://hsm-online-collections-assets-prod.s3.eu-west-1.amazonaws.com/emu/emumultimedia/multimedia/"
        return "".join([url, img_path, name])
    else: return


def scraper(filename, start_num=False, end_num=False):
    # filename, start_num, end_num = filename[0], filename[1], filename[2]
    signal.signal(signal.SIGINT, signal.SIG_IGN)
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
        headers = {
      'Content-Type': 'application/json',
      'x-api-key': 'yuFn5KEdcU2KVtUFol2Ft24wonNthuDBaovxyN8h', # api was hardcoded into website
      'host': 'prod-online.glamdigital.io'
        }
        s = requests.Session()
        s.headers.update(headers)
        for id in tqdm(range(start_id, end_num)):
            try:
                url = f"https://prod-online.glamdigital.io/item/hsm-catalogue-{id}/full"
                jd = url_get(url, s)
                if not jd: continue

                ident = jd["identifier"]
                phys = jd["physical"]
                insc = jd["inscriptions"]
                data = {
                    "institution_name": "History of Science Museum",
                    "institution_city": "Oxford",
                    "institution_state": "Oxfordshire ",
                    "institution_country": "United Kingdom",
                    "institution_latitude": 51.75431763807817,
                    "institution_longitude": -1.2554219667123852,
                    "object_number": ident.get("inventoryNo"),
                    "accession_number": ident.get("accessionNumber"),
                    "category": "|".join([x for x in jd["subject"]]),
                    "title": jd.get("recordTitle"),
                    "description": jd.get("recordDescription")[:10000] if jd.get("recordDescription")  else None,
                    "dimensions": dimensions(jd.get("dimensions")),
                    "inscription": "|".join([x for x in [insc["primaryInscriptions"], insc["otherInscriptions"]] if x]),
                    "materials": "|".join([x for x in phys["material"]]),
                    "technique": "|".join([x for x in phys["technique"]]),
                    "from_location": get_location(jd),
                    "date_description": jd["dateCreated"],
                    "year_start": str(jd["dateCreatedEarliest"]).split("-")[0] if jd["dateCreatedEarliest"] else "",
                    "year_end": str(jd["dateCreatedLatest"]).split("-")[0] if jd["dateCreatedLatest"] else "",
                    "maker_full_name": "|".join([x["fullName"] for x in jd["persons"] if x["fullName"] else ""]),
                    "maker_first_name": "|".join([x["firstName"] for x in jd["persons"] if x["firstName"] else ""]),
                    "maker_last_name": "|".join([x["lastName"] for x in jd["persons"] if x["lastName"] else ""]),
                    "maker_birth_year": "|".join([x["birthDate"].split("-")[0] for x in jd["persons"] if x["birthDate"] else ""]),
                    "maker_death_year": "|".join([x["birthDate"].split("-")[-1] for x in jd["persons"] if x["birthDate"] else ""]),
                    "maker_role": "|".join([x["partyType"] for x in jd["persons"] if x["partyType"] else ""]),
                    "maker_gender": "|".join([x["sex"] for x in jd["persons"] if x["sex"] else ""]),
                    "image_url": get_image(jd),
                    "provenance": jd["owner"]["provenance"],
                    "source_1": url,
                    "source_2": f"https://www.hsm.ox.ac.uk/collections-online#/item/hsm-catalogue-{id}",
                    "drop_me": id,
                }

                writer.writerow(data)

            except Exception as e:
                print("\n",id)
                print(json.dumps(jd, indent=4))
                print(e)
                raise(e)

if __name__ == "__main__":
        arguments = []
        end_id = 9180 #45899
        # start_num is supplemental for first run and is only used if the files don't exist
        for i in range(10):
            if i == 0:
                start_num = 0
            else:
                # Use end_id before it is added to
                start_num = end_id - 9180
            print("Startnum: " + str(start_num))
            arguments.append([f"./files/extracted_data{i}.csv", start_num, end_id])
            end_id = end_id + 9180
        print(arguments)

        try:
            pool = Pool(processes=len(arguments))
            pool.starmap(scraper, arguments)
            # for _ in tqdm(pool.istarmap(scraper, arguments), total=len(arguments)):
            #     pass
            pool.close()
            send_mail("Finished", "")
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
            send_mail("Scraper crashed", "")
            sys.exit()
            print("   [*] Finished joining...")
            # sys.exit(1)

# scraper("test.csv", 0, 20)
