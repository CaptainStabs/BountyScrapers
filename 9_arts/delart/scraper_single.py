import csv
import json
import os
import re
import signal
import sys
import traceback as tb
from multiprocessing import Pool
from urllib3 import exceptions as urllib3_exceptions

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

dates_pat = re.compile(r"(\d{3,4}(?:\-|\–)\d{3,4})")
pat1 = re.compile(r"(?:(?:(\d{4}|\d{3})\/)|(:?|\d{4}|\d{3}))(?:(\d{4}|\d{3})|(\d{4}|\d{3})(?:\)))")
pat2 = re.compile(r"((\d{4}|\d{3}) - (\d{4}|\d{3})-(\d{4}|\d{3}))|((?!\d)(\d{4}|\d{3}) - |(\d{4}|\d{3})-(\d{4}|\d{3}) - (\d{4}|\d{3}))")
born_pat = re.compile(r"(?: born )(\d{4})(?:\))")

# print(re.findall(pat, string))

def get_dates(dates: list) -> tuple:
    year_list = []
    for bio in dates:
        if not any(x.isdigit() for x in bio):
            year_list.append("")
            continue

        # print("Bio:",bio)
        if re.findall(pat2, bio):
            print("\nAAAA")
            years = bio.split(" - ")
            years = [y.replace("-", "/").strip("(").strip(")") for y in years]
            years[0] = years[0].split(",")[1].strip() if len(years[0].split(",")) > 1 else years[0]
            year_list.append([x for x in years])

        elif re.findall(born_pat, bio):
            years = re.findall(born_pat, bio)
            # print("years:", years)
            year_list.extend(years)

        elif "/" not in bio:
            years = re.search(dates_pat, bio)
            if years:
                year_list.append(years.group(0))

        elif "/" in bio:
            years = re.findall(pat1, bio)
            years = [tuple(y for y in tup if y != '') for tup in years]
            years = ["/".join(y) for y in years]

    b_list = []
    d_list = []
    for year in year_list:
        if "-" in year:
            b, d = year.split("-")
            b_list.append(b)
            d_list.append(d)
        else:
            b_list.append(year)
            d_list.append("")

    birth_years = "|".join(b_list)
    death_years = "|".join(d_list)
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

        except urllib3_exceptions.MaxRetryError:
            if x < 4:
                x+=1
            else:
                raise
            return
            continue

        except Exception as e:
            raise(e)
            x+=1
            continue


        if r.status_code == 404:
            return

        if r.status_code == 401:
            return

        r = r.text
        x=10
        return r            # if x == 4:
            #     raise(e)
        x += 1

def scraper(filename, start_num, end_num, position, lock):
    # filename, start_num, end_num = filename[0], filename[1], filename[2]
    # signal.signal(signal.SIGINT, signal.SIG_IGN)
    print(start_num, end_num, filename)
    if os.path.exists(filename) and os.stat(filename).st_size > 515:
        start_id = get_last_id(filename, 515)
    else:
        start_id = start_num

    with lock:
        bar = tqdm(
            desc=f'Position {position}',
            total=end_num-start_id,
            position=position+1,
            leave=False
        )

    print(start_id)
    columns = ['institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', 'title', 'maker_full_name', 'maker_role', 'maker_birth_year', 'maker_death_year', 'date_description', 'dimensions', 'materials', 'category', 'credit_line', 'object_number', 'description', 'image_url', 'current_location', 'source_1', 'drop_me']

    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        s = requests.Session()
        for id in tqdm(range(start_id, end_num)):
            try:
                url = f"https://emuseum.delart.org/objects/{id}"
                jd = url_get(url, s)
                if not jd: continue

                parser = fromstring(jd)

                roles = parser.xpath("//div[@class='detailField peopleField']/*/text()")
                names = [x.replace("\n", "") for x in parser.xpath('//*[@class="detailField peopleField"]/span[@class="detailFieldValue"]/a/span[@property="name"]/text()')]
                dates = [x.replace("\n", "").strip() for x in parser.xpath("//div[@class='detailField peopleField']/span[2]/span[last()]/text()")]

                birth, death = None, None
                if len(dates):
                    birth, death = get_dates(dates)

                date_desc = parser.xpath("//*[@class='detailField displayDateField']/span[@class='detailFieldValue']/text()")
                dimens = parser.xpath("//*[@class='detailField dimensionsField']/span[@class='detailFieldValue']/text()")
                mats = parser.xpath("//*[@class='detailField mediumField']/span[@class='detailFieldValue']/text()")
                cred_line = parser.xpath("//*[@class='detailField creditlineField']/span[@class='detailFieldValue']/text()")
                desc = parser.xpath('//*[@id="detailView"]/div/div[2]/div/div/span/span[2]/text()')
                img = parser.xpath('//*[@id="mediaZone"]/div/img/@src')

                data = {
                    "institution_name": "Delaware Art Museum",
                    "institution_city": "Wilmington",
                    "institution_state": "Delaware",
                    "institution_country": "United States",
                    "institution_latitude": 39.76544340487763,
                    "institution_longitude": -75.56469599738497,
                    "title": parser.xpath('//*[@class="detailField titleField"]/h1/text()')[0],
                    "maker_full_name": "|".join(names) if names else None,
                    "maker_role": "|".join(roles) if roles else None,
                    "maker_birth_year": birth,
                    "maker_death_year": death,
                    "date_description": date_desc[0] if date_desc else None,
                    "dimensions": dimens[0] if dimens else None,
                    "materials": "|".join(mats) if mats else None,
                    "category": parser.xpath('//*[@class="detailField classificationField"]/span[@property="artForm"]/text()')[0],
                    "credit_line": cred_line[0] if cred_line else None,
                    "object_number": parser.xpath("//*[@class='detailField invnoField']/span[@class='detailFieldValue']/text()")[0],
                    "description": desc[0] if desc else None,
                    "image_url": "https://emuseum.delart.org/" + img[0] if img else None,
                    "current_location": parser.xpath('''//*[@class="detailField onviewField"]/span[@class="detailFieldValue {eognl:detailed.onview == 1 ? 'on-view' : 'not-on-view'}"]/text()''')[0],
                    "source_1": url,
                    "drop_me": id
                }

                desc_stuff = parser.xpath('//*[@class="detailField toggleField descriptionField"]/span[@class="toggleLabel detailFieldLabel"]/text()')

                if "Culture" in desc_stuff:
                    cult_ind = desc_stuff.index("Culture")
                    cult = parser.xpath(f'//*[@class="emuseum-detail-category detailField thesconceptsField"][{cult_ind+1}]/ul/li/span/text()')
                    data["culture"] = cult[0]


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

        # with lock:
        #     bar.close()

# scraper("extracted_data.csv", 0, 60600, 1, "")
