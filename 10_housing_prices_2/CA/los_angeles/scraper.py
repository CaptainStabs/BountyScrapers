import requests
import json
from tqdm import tqdm
import csv
import datetime
import traceback as tb
import os
import random


import sys
from pathlib import Path

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))
from _common import date_parse
from _common.send_mail import send_mail
from _common import get_last_id

def url_get(url, s):
    x = 0
    while x < 10:
        try:
            r = s.get(url)
        # except KeyboardInterrupt:
        #     print("Ctrl-c detected, exiting")
        #     # import sys; sys.exit()
        #     raise KeyboardInterrupt

        except requests.exceptions.ConnectionError:
            x+=1
            continue

        except Exception as e:
            raise(e)
            x+=1
            continue

        if r.status_code == 404:
            return

        try:
            r = r.json()
            x=20
            return r
        except json.decoder.JSONDecodeError:

            if r.status_code == 200:
                return None

            print(r)
            # if x == 4:
            #     raise(e)
        x += 1

def get_user_agent():
    user_agents = user_agents = [
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
     'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
     'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
     'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
     'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
     ]

    user_agent = random.choice(user_agents)
    headers = {
      'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'DNT': '1',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': user_agent,
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-User': '?1',
      'Sec-Fetch-Dest': 'document'
    }
    return headers

def scraper(filename, start_num=False, end_num=False):
    # filename, start_num, end_num = filename[0], filename[1], filename[2]
    # signal.signal(signal.SIGINT, signal.SIG_IGN)
    print(start_num, end_num, filename)
    if os.path.exists(filename) and os.stat(filename).st_size > 515:
        start_id = get_last_id(filename, 515)
    else:
        start_id = start_num

    columns = ['state', 'property_zip5', 'property_street_address', 'property_city', 'property_county', 'property_id', 'property_type', 'property_lat', 'property_lon', 'building_num_units', 'building_year_built', 'building_area_sqft', 'land_area_sqft', 'building_num_beds', 'building_num_baths', 'land_area_acres', 'land_assessed_value', 'land_assessed_date', 'building_assessed_value', 'building_assessed_date', 'sale_datetime', 'sale_price', 'total_assessed_value', 'transfer_deed_type']
    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        s = requests.Session()

        for id in tqdm(range(start_id, end_num)):
            s.headers.update(get_user_agent())
            try:
                # id = 20040010s04
                url = f"https://portal.assessor.lacounty.gov/api/parceldetail?ain={id}"

                r = url_get(url, s)
                if not r: continue
                r = r["Parcel"]
                if not r: continue

                if r:
                    print("IS R")

                assessed_date = str(date_parse("-".join([r["CurrentRoll_BaseYear"], "01", "01"])))
                data = {
                    "state": "CA",
                    "property_zip5": r["SitusZipCode"][:5],
                    "property_street_address": " ".join(r["SitusStreet"].upper().split()),
                    "property_city": r["SitusCity"].strip(" CA").strip(),
                    "property_county": "LOS ANGELES",
                    "property_id": r["AIN"],
                    "property_type": r["UseType"],
                    "property_lat": r["Latitude"],
                    "property_lon": r["Longitude"],
                    "building_num_units": r["NumOfUnits"],
                    "building_year_built": r["YearBuilt"],
                    "building_area_sqft": r["SqftMain"],
                    "land_area_sqft": r["SqftLot"],
                    "building_num_beds": r["NumOfBeds"],
                    "building_num_baths": r["NumOfBaths"],
                    "land_area_acres": r["LandAcres"],
                    "land_assessed_value": r["CurrentRoll_LandValue"],
                    "land_assessed_date": assessed_date,
                    "building_assessed_value": r["CurrentRoll_ImpValue"],
                    "building_assessed_date": assessed_date,
                }

                sale_request = s.get(f"https://portal.assessor.lacounty.gov/api/parcel_ownershiphistory?ain={id}").json()

                sr = sale_request["Parcel_OwnershipHistory"]

                for sale in sr:
                    if sale["DTTSalePrice"] is not None:
                        data["sale_datetime"] = str(date_parse(sale["RecordingDate"]))
                        data["sale_price"] = sale["DTTSalePrice"]
                        data["total_assessed_value"] = sale["AssessedValue"]
                        data["transfer_deed_type"] = sale["DocumentReasonCodeDesc"]
                        writer.writerow(data)


            except KeyboardInterrupt:
                return

            except Exception:
                print("\n",r)
                print(json.dumps(r, indent=4))
                send_mail("script crashed", tb.print_exc())
                raise


# scraper(r"./files/a.csv", 4328022016, 4328022018)
