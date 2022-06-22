import csv
import json
import os
import re
import signal
import sys
import traceback as tb
from multiprocessing import Pool

import _istarmap
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

def dimensions(dim):
    if len(list(set(list(dim.values())))) != 1:
        dimension = " x ".join([str(dim["height"]), str(dim["width"]), str(dim["depth"]), str(dim["diameter"])])
        dimension = " ".join([dimension, str(dim["unitLength"])])
        if not isinstance(dim["weight"], type(None)):
            dimension = " ".join([dimension, str(dim["weight"]), dim["unitWeight"]])
        return dimension
    else:
        return ""

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

def scraper(filename, start_num=False, end_num=False):
    # filename, start_num, end_num = filename[0], filename[1], filename[2]
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    print(start_num, end_num, filename)
    if os.path.exists(filename) and os.stat(filename).st_size > 283:
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
        "category",
        "title",
        "description",
        "dimensions", #
        "accession_year",
        "credit_line",
        "source_1",
        "date_description",
        "from_location",
        "maker_full_name",
        "maker_role",
        "year_start",
        "year_end",
        "accession_number",
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
                url = f"https://api.maas.museum/v2/objects/{id}"
                jd = url_get(url, s)
                if not jd: continue
                try:
                    temp = jd["_id"]
                except TypeError:
                    jd = jd[0]
                data = {
                    "object_number": jd["_id"],
                    "accession_number": jd["registrationNumber"],
                    "institution_name": "Museum of Applied Arts & Sciences",
                    "institution_city": "Ultimo",
                    "institution_state": "New South Wales",
                    "institution_country": "Australia",
                    "institution_latitude": -33.87848680715133,
                    "institution_longitude": 151.19954179528983,
                    "category": "|".join([x for x in jd["category"] if not isinstance(x, type(None))]),
                    "dimensions": dimensions(jd['dimensions']),
                    "source_1": url,
                    "drop_me": id,
                }

                events = jd["events"]
                years = jd["years"]
                history = jd["history"]

                if len(events):
                    data["date_description"] = "|".join([x['date'] for x in events if not isinstance(x['date'], type(None))])
                    data["from_location"] = "|".join([str(x['place']) for x in events if not isinstance(x['place'], type(None))])[:4000]
                    data["maker_full_name"] = "|".join([str(x['creator']) for x in events])
                    data["maker_role"] = "|".join([str(x['role']) for x in events])

                if len(history) and not len(events):
                    logging.info("Using history not events")
                    data["date_description"] = "|".join([x['date'] for x in history if not isinstance(x['date'], type(None))])
                    data["from_location"] = "|".join([x['place'] for x in history if not isinstance(x['place'], type(None))])[:4000]
                    data["maker_full_name"] = "|".join([str(x['creator']) for x in history])
                    data["maker_role"] = "|".join([x['role'] for x in history])

                if len(jd["production"]) and not len(events) and not len(history):
                    prod = jd["production"]
                    logging.info("Using production not events or history")
                    data["date_description"] = "|".join([x['date'] for x in prod if not isinstance(x['date'], type(None))])
                    data["from_location"] = "|".join([x['place'] for x in prod if not isinstance(x['place'], type(None))])[:4000]
                    data["maker_full_name"] = "|".join([str(x['creator']) for x in prod])
                    data["maker_role"] = "|".join([x['role'] for x in prod])


                if len(years) and "date_description" not in data.keys():
                    logging.info("Adding date_description from years")
                    data["date_description"] = "-".join([years[0], years[-1]])

                if len(years):
                    data["year_start"] = years[0]
                    data["year_end"] = years[-1]

                if "acquisitionCreditLine" in jd.keys():
                    data["credit_line"] = jd["acquisitionCreditLine"]

                if "accessionedYear" in jd.keys():
                    data["accession_year"] = jd["accessionedYear"]

                if "title" in jd.keys():
                    data["title"] = jd["title"]
                else:
                    if "summary" in jd.keys():
                        data["title"] = jd["summary"]

                if "description" in jd.keys():
                    data["description"] = remove_escaped.sub('', jd["description"][:10000]).replace("\n", "")
                elif "significanceStatement" in jd.keys():
                    if jd["significanceStatement"]:
                        data["description"] =  remove_escaped.sub('', jd["significanceStatement"][:10000]).replace("\n", "")

                writer.writerow(data)

            except Exception as e:
                print("\n",id)
                print(json.dumps(jd, indent=4))
                print(e)
                raise(e)

if __name__ == "__main__":
        arguments = []
        end_id = 99999
        # start_num is supplemental for first run and is only used if the files don't exist
        for i in range(10):
            if i == 0:
                start_num = 0
            else:
                # Use end_id before it is added to
                start_num = end_id - 99999
            print("Startnum: " + str(start_num))
            arguments.append([f"./files/extracted_data{i}.csv", start_num, end_id])
            end_id = end_id + 99999
        print(arguments)

        try:
            pool = Pool(processes=len(arguments))
            for _ in tqdm(pool.istarmap(scraper, arguments), total=len(arguments)):
                pass
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
            # sys.exit(1)
