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
from lxml.html import fromstring
from pathlib import Path
p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))
from _common import get_last_id
from _common.send_mail import send_mail

dates_pat = re.compile(r"(\d{4}|\d{3} \d{4}|\d{3})")
pat1 = re.compile(r"(?:(?:(\d{4}|\d{3})\/)|(:?|\d{4}|\d{3}))(?:(\d{4}|\d{3})|(\d{4}|\d{3})(?:\)))")
pat2 = re.compile(r"((\d{4}|\d{3}) - (\d{4}|\d{3})-(\d{4}|\d{3}))|((?!\d)(\d{4}|\d{3}) - |(\d{4}|\d{3})-(\d{4}|\d{3}) - (\d{4}|\d{3}))")
born_pat = re.compile(r"(?: born )(\d{4})(?:\))")

def get_dates(dates):
    bio = "|".join(dates)
    if re.findall(pat2, bio):
        print("\nAAAA")
        years = bio.split(" - ")
        years = [y.replace("-", "/").strip("(").strip(")") for y in years]
        years[0] = years[0].split(",")[1].strip() if len(years[0].split(",")) > 1 else years[0]

    elif re.findall(born_pat, bio):
        years = re.findall(born_pat, bio)

    elif "/" not in bio:
        years = re.findall(dates_pat, bio)
    elif "/" in bio:
        years = re.findall(pat1, bio)
        years = [tuple(y for y in tup if y != '') for tup in years]
        years = ["/".join(y) for y in years]


    birth_years = "|".join([years[i] for i in range(0, len(years), 2)])
    death_years = "|".join([years[i] for i in range(1, len(years), 2)])
    if len(birth_years):
        birth = birth_years
    else:
        birth = None
    if len(death_years):
        death = death_years
    else:
        death = None

    return birth, death

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
            r = r.text
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
    columns = ['institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', 'title', 'maker_full_name', 'maker_role', 'maker_birth_year', 'maker_death_year', 'date_description', 'culture', 'materials', 'dimensions', 'category', 'credit_line', 'object_number', 'image_url', 'source_1', 'inscription', 'drop_me']

    remove_escaped = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        s = requests.Session()
        for id in tqdm(range(start_id, end_num)):
            try:
                url = f"https://zimmerli.emuseum.com/objects/{id}"
                jd = url_get(url, s)
                if not jd: continue

                parser = fromstring(jd)

                roles = parser.xpath("//div[@class='detailField peopleField']/*/text()")
                names = [x.replace("\n", "").strip() for x in parser.xpath("//div[@class='detailField peopleField']/span[2]/span[@property='name']/text()")]
                dates = [x.replace("\n", "").strip() for x in parser.xpath("//div[@class='detailField peopleField']/span[2]/span[last()]/text()")]

                birth, death = None, None
                if len(dates):
                    birth, death = get_dates(dates)

                date_desc = parser.xpath("//*[@class='detailField displayDateField']/span[@property='dateCreated']/text()")
                img = parser.xpath('//*[@id="mediaZone"]/div/img/@src')
                dimens = parser.xpath("//*[@class='detailField dimensionsField']/span[@class='detailFieldValue']/text()")
                insc = parser.xpath("//*[@class='detailField inscribedField']/span[@class='detailFieldValue']/text()")

                data = {
                    "institution_name": "Zimmerli Art Museum, Rutgers University",
                    "institution_city": "New Brunswick",
                    "institution_state": "New Jersey",
                    "institution_country": "United States",
                    "institution_latitude": 40.49975929808084,
                    "institution_longitude": -74.44583970209675,
                    "title": parser.xpath('//*[@id="detailView"]/div/div[2]/div/div/div[1]/h1/text()')[0],
                    "maker_full_name": "|".join(names) if names else None,
                    "maker_role": "|".join(roles) if roles else None,
                    "maker_birth_year": birth,
                    "maker_death_year": death,
                    "date_description": date_desc[0] if date_desc else None,
                    "culture": parser.xpath("//*[@class='detailField cultureField']/span[@class='detailFieldValue']/a/text()")[0],
                    "materials": parser.xpath("//*[@class='detailField mediumField']/span[@class='detailFieldValue']/text()")[0],
                    "dimensions": dimens[0] if dimens else None,
                    "category": parser.xpath("//*[@class='detailField classificationField']/span[@class='detailFieldValue']/text()")[0],
                    "credit_line": parser.xpath("//*[@class='detailField creditlineField']/span[@class='detailFieldValue']/text()")[0],
                    "object_number": parser.xpath("//*[@class='detailField invnoField']/span[@class='detailFieldValue']/text()")[0],
                    "inscription": insc[0] if insc else None,
                    "image_url": "https://zimmerli.emuseum.com/" + str(img[0]) if img else None,
                    "source_1": url,
                    "drop_me": id
                }

                writer.writerow(data)

            except Exception:
                print("\n",id)
                tb.print_exc()
                # send_mail("script crashed", "")
                raise

# scraper("extracted_data.csv", 0, 60600)
