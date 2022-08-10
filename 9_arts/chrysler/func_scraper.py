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
        # except KeyboardInterrupt:
        #     print("Ctrl-c detected, exiting")
        #     import sys; sys.exit()
        #     raise KeyboardInterrupt
        except Exception as e:
            raise(e)
            x+=1
            continue

        if r.status_code == 404:
            return

        r = r.text
        x=10
        return r            # if x == 4:
            #     raise(e)
        x += 1

def scraper(filename, start_num, end_num, position, lock):
    with lock:
        bar = tqdm(
            desc=f'Position {position}',
            total=end_num,
            position=position,
            leave=False
        )
    # filename, start_num, end_num = filename[0], filename[1], filename[2]
    # signal.signal(signal.SIGINT, signal.SIG_IGN)
    print(start_num, end_num, filename)
    if os.path.exists(filename) and os.stat(filename).st_size > 515:
        start_id = get_last_id(filename, 515)
    else:
        start_id = start_num
    print(start_id)
    columns = ['institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', 'title', 'maker_full_name', 'maker_role', 'maker_birth_year', 'maker_death_year', 'date_description', 'culture', 'materials', 'dimensions', 'category', 'credit_line', 'object_number', 'inscription', 'image_url', 'current_location', 'description', 'provenance', 'source_1', 'drop_me']

    remove_escaped = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        s = requests.Session()
        for id in tqdm(range(start_id, end_num)):
            try:
                url = f"https://chrysler.emuseum.com/objects/{id}"
                jd = url_get(url, s)
                if not jd: continue

                parser = fromstring(jd)

                roles = parser.xpath("//div[@class='detailField peopleField']/*/text()")
                roles = [x.replace(": ", "") for x in roles]
                names = [x.replace("\n", "").strip() for x in parser.xpath("//div[@class='detailField peopleField']/span[2]/span[@property='name']/text()")]
                dates = [x.replace("\n", "").strip() for x in parser.xpath("//div[@class='detailField peopleField']/span[2]/span[last()]/text()")]

                birth, death = None, None
                if len(dates):
                    birth, death = get_dates(dates)

                date_desc = parser.xpath("//*[@class='detailField displayDateField']/span[@property='dateCreated']/text()")
                img = parser.xpath('//*[@id="mediaZone"]/div/img/@src')
                dimens = parser.xpath("//*[@class='detailField dimensionsField']/span[@class='detailFieldValue']/div/text()")
                insc = parser.xpath("//*[@class='detailField inscribedField']/span[@class='detailFieldValue']/text()")
                cult = parser.xpath("//*[@class='detailField cultureField']/span[@class='detailFieldValue']/text()")
                cate = parser.xpath("//*[@class='detailField multiItemField classificationsField']/div/text()")
                cur_loc = parser.xpath("//*[@class='detailField onviewField']/div/text()")
                desc = parser.xpath("//*[@class='detailField toggleField descriptionField']/span[@property='description']/text()")
                mat = parser.xpath("//*[@class='detailField mediumField']/span[@class='detailFieldValue']/text()")
                cred_line = parser.xpath("//*[@class='detailField creditlineField']/span[@class='detailFieldValue']/text()")

                desc_stuff = parser.xpath('//*[@class="detailField toggleField descriptionField"]/span[@class="toggleLabel detailFieldLabel"]/text()')
                prov = None
                if "Provenance" in desc_stuff:
                    prov_ind = desc_stuff.index("Provenance")
                    prov = parser.xpath(f'//*[@class="detailField toggleField descriptionField"][{prov_ind+1}]/span[@class="toggleContent"]/text()')


                data = {
                    "institution_name": "The Chrysler Museum of Art",
                    "institution_city": "Norfolk",
                    "institution_state": "Virginia",
                    "institution_country": "United States",
                    "institution_latitude": 36.85638887993706,
                    "institution_longitude": -76.29305291999475,
                    "title": parser.xpath('//*[@class="detailField titleField"]/h1/text()')[0],
                    "maker_full_name": "|".join(names) if names else None,
                    "maker_role": "|".join(roles) if roles else None,
                    "maker_birth_year": birth,
                    "maker_death_year": death,
                    "date_description": date_desc[0] if date_desc else None,
                    "culture": cult[0] if cult else None,
                    "materials": mat[0] if mat else None,
                    "dimensions": " ".join(dimens) if dimens else None,
                    "category": "|".join(cate) if cate else None,
                    "credit_line": cred_line[0] if cred_line else None,
                    "object_number": parser.xpath("//*[@class='detailField invnoField']/span[@class='detailFieldValue']/text()")[0],
                    "inscription": insc[0] if insc else None,
                    "image_url": "https://chrysler.emuseum.com/" + str(img[0]) if img else None,
                    "current_location": " ".join([x.replace("\n", "").strip() for x in cur_loc]) if cur_loc else None,
                    "description": " ".join(desc).replace("n", "").strip() if desc else None,
                    "provenance": prov,
                    "source_1": url,
                    "drop_me": id
                }

                writer.writerow(data)

                with lock:
                    bar.update(1)

            except KeyboardInterrupt:
                return

            except Exception:
                print("\nCRASHED ID:",url)
                tb.print_exc()
                # send_mail("script crashed", "")
                raise

        with lock:
            bar.close()


# scraper("extracted_data.csv", 0, 60600)
