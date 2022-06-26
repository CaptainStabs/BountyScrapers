import csv
import json
import os
import re
import signal
import sys
import traceback as tb
from multiprocessing import Pool
import time



# import _istarmap
import pandas as pd
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tqdm import tqdm

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import sys
from pathlib import Path

p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))
from _common import get_last_id

import logging; logging.basicConfig(level=logging.INFO)

def sleep_counter(seconds, filename):
    for remaining in range(seconds, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{} Too many requests, waiting for {:2d} seconds.".format(filename[22:-4], remaining))
        sys.stdout.flush()
        time.sleep(1)

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

def url_get(id, key, s):
    print("\n", id, key[:5])
    url = f"https://hackathon.philamuseum.org/api/v0/collection/object?query={id}&api_token={key}"
    return s.get(url, verify=False)

def scraper(filename, key, start_num=None, end_num=None):
    print(start_num, end_num, filename)
    # filename, start_num, end_num = filename[0], filename[1], filename[2]
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    columns = [
        "object_number",
        "category",
        "date_description",
        "year_start",
        "year_end",
        "materials",
        "dimensions",
        "credit_line",
        "provenance",
        "title",
        "technique",
        "from_location",
        "maker_full_name",
        "maker_role",
        "maker_birth_year",
        "maker_death_year",
        "current_location",
        "image_url",
        "source_1",
        "drop_me"
        ]

    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.path.exists(filename) and os.stat(filename).st_size > 283:
            start_id = get_last_id(filename)
        else:
            start_id = 0

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        s = requests.Session()
        for i in tqdm(range(start_id, 298920), desc=filename[22:-4]):
            url = f"https://hackathon.philamuseum.org/api/v0/collection/object?query={i}"
            r = url_get(i, key, s)
            ratelimit_remaining = int(r.headers['X-RateLimit-Remaining'])
            # print(ratelimit_remaining)
            if ratelimit_remaining < 20:
                print("\n", ratelimit_remaining)

            if ratelimit_remaining == 10:
                # print("Sleeping for 60")
                sleep_counter(60, filename)
                r = url_get(i, key, s)
                print("ratelimit remaining under 10:", r.headers["X-RateLimit-Remaining"])
                if int(r.headers["x-RateLimit-Remaining"]) < 10: # don't use var here because we need to check current r headers
                    print("Has not reset, exiting.")
                    os.exit(1)

            if r.status_code == 429:
                retry_after = int(r.headers["retry-after"]) + 1
                sleep_counter(retry_after, filename)
                r = url_get(i, key, s)

                if not r.headers["x-RateLimit-Remaining"]: # don't use var here because we need to check current r headers
                    print("Has not reset, exiting.")
                    os.exit(1)

            if r.status_code != 500 and r.status_code != 429:
                jd = r.json()

                data = {
                    "object_number": jd["ObjectNumber"],
                    "category": jd["Classification"],
                    "date_description": jd["Dated"],
                    "year_start": jd["DateBegin"],
                    "year_end": jd["DateEnd"],
                    "materials": jd["Medium"],
                    "credit_line": jd["CreditLine"],
                    "provenance": jd["Provenance"],
                    "title": jd["Title"],
                    "technique": jd["Style"],
                    "maker_full_name": "|".join([x["Artist"] for x in jd["Artists"]]),
                    "maker_role": "|".join([x["Role"] for x in jd["Artists"]]),
                    "current_location": jd["Location"],
                    "image_url": jd["Image"],
                    "source_1": url,
                    "drop_me": i
                }

                if len(jd["Artists"]) > 1:
                    try:
                        data["maker_birth_year"] = "|".join([x["Artist_Info"].split(",")[-1].split("-")[0].strip() if x["Artist_Info"] else "" for x in jd["Artists"]])
                        data["maker_death_year"] = "|".join([x["Artist_Info"].split(",")[-1].split("-")[-1].strip() if x["Artist_Info"] else "" for x in jd["Artists"] if x["Artist_Info"]])
                    except AttributeError:
                        print("Artist info is null")
                        print(jd["Artists"])

                elif len(jd["Artists"]) == 1:
                    if "unknown" in jd["Artists"][0]["Artist"]:
                        data["maker_role"] = ""
                        print("Nulling maker_role for", jd["Artists"])

                if jd["Dimensions"]:
                    data["dimensions"] = jd["Dimensions"].replace("\r\n", "")

                if jd["Geography"]:
                    data["from_location"] = jd["Geography"].replace("\\u", "\\u")

                writer.writerow(data)

if __name__ == "__main__":
    arguments = []
    keys = ["jnFV09XMKDJ0yVYrcQd3si72VFN4EUeM15B479G6RkMfiu4BstY2GuaR19kI", "wfXOpPLeYwgissXKDoT5MzygR4ApP8Ev14HIR83LtHNMFY4JdHRuVyk3qJK7", "T3UWvnmQdtMSeZUZcjqi75gu7PTpjWJItRYdcicMtWx0xXEri1dBhW6RpfPd", "d3INVaCoZxa1PbuLmm3RhghHcdSJQzF0XHhXqxVWQez0VCBREn8cgGtajOK5", "ARun27s8a8VImueDBUwipkICRZI30eWAuFxjBFhsjLGKIHpacZhsm418VRXu"]
    end_id = 59784
    sub_id = end_id
    # start_num is supplemental for first run and is only used if the files don't exist
    for i in range(5):
        if i == 0:
            start_num = 0
        else:
            # Use end_id before it is added to
            start_num = end_id - sub_id
        print("Startnum: " + str(start_num))
        arguments.append([f"./files/extracted_data{i}.csv", keys[i], start_num, end_id])
        end_id = end_id + sub_id
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
