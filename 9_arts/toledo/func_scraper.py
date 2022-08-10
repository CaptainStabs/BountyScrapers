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

dates_pat = re.compile(r"(\d{3,4}\-\d{3,4})|(\d{3,4})")
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
    columns = ['institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', 'title', 'maker_full_name', 'maker_role', 'maker_birth_year', 'maker_death_year', 'date_description', 'title', 'date_description', 'dimensions', 'materials', 'category', 'credit_line', 'object_number', 'description', 'from_location', 'image_url', 'source_1', 'culture', 'current_location', 'drop_me']

    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        s = requests.Session()
        for id in tqdm(range(start_id, end_num)):
            try:
                url = f"http://emuseum.toledomuseum.org/objects/{id}"
                jd = url_get(url, s)
                if not jd: continue

                parser = fromstring(jd)

                roles = parser.xpath("//div[@class='detailField peopleField']/*/text()")
                names = [x.replace("\n", "") for x in parser.xpath("//div[@class='detailField peopleField']/span[2]/span[1]/text()")]
                dates = [x.replace("\n", "").strip() for x in parser.xpath("//div[@class='detailField peopleField']/span[2]/span[last()]/text()")]

                birth, death = None, None
                if len(dates):
                    birth, death = get_dates(dates)

                date_desc = parser.xpath("//*[@class='detailField displayDateField']/span[@class='detailFieldValue']/text()")
                dimens = parser.xpath("//*[@class='detailField dimensionsField']/span[@class='detailFieldValue']/div/text()")
                mats = parser.xpath("//*[@class='detailField mediumField']/span[@class='detailFieldValue']/text()")
                cred_line = parser.xpath("//*[@class='detailField creditlineField']/span[@class='detailFieldValue']/text()")
                desc = parser.xpath("//*[@class='detailField labelTextField']/span[@class='detailFieldValue']/text()")
                from_loc = parser.xpath('//*[@class="detailField periodField"]/span[@class="detailFieldValue"]/text()')
                img = parser.xpath('//*[@id="mediaZone"]/div/img/@src')
                data = {
                    "institution_name": "The Toledo Museum of Art",
                    "institution_city": "Toledo",
                    "institution_state": "Ohio",
                    "institution_country": "United States",
                    "institution_latitude": 41.658397959482,
                    "institution_longitude": -83.55939586197056,
                    "title": parser.xpath('//*[@class="detailField titleField"]/h1/text()')[0],
                    "maker_full_name": "|".join(names) if names else None,
                    "maker_role": "|".join(roles) if roles else None,
                    "maker_birth_year": birth,
                    "maker_death_year": death,
                    "date_description": date_desc[0] if date_desc else None,
                    "title": parser.xpath('//*[@class="detailField titleField"]/h1/text()')[0],
                    "date_description": date_desc[0] if date_desc else None,
                    "dimensions": dimens[0] if dimens else None,
                    "materials": mats[0] if mats else None,
                    "category": parser.xpath("//*[@class='detailField classificationField']/span[@class='detailFieldValue']/text()")[0],
                    "credit_line": cred_line[0] if cred_line else None,
                    "object_number": parser.xpath("//*[@class='detailField invnoField']/span[@class='detailFieldValue']/text()")[0],
                    "description": desc[0] if desc else None,
                    "from_location": from_loc[0] if from_loc else None,
                    "image_url": "http://emuseum.toledomuseum.org/" + img[0] if img else None,
                    "source_1": url,
                    "drop_me": id
                }

                desc_stuff = parser.xpath('//*[@class="detailField toggleField descriptionField"]/span[@class="toggleLabel detailFieldLabel"]/text()')
                if "Description" in desc_stuff:
                    desc_ind = desc_stuff.index("Description")
                    desc = parser.xpath(f'//*[@class="detailField toggleField descriptionField"][{desc_ind+1}]/span[@class="toggleContent"]/text()')[0]

                    desc = desc.replace("\n", "").strip()
                    if not data["description"]:
                        data["description"] = desc
                    else:
                        data["description"] = "|".join([data["description"], desc])


                if "Culture" in desc_stuff:
                    cult_ind = desc_stuff.index("Culture")
                    cult = parser.xpath(f'//*[@class="emuseum-detail-category detailField thesconceptsField"][{cult_ind+1}]/ul/li/span/text()')
                    data["culture"] = cult[0]

                not_view = parser.xpath("//*[@class='detailField currentLocationField']/text()")

                if len(not_view):
                    data["current_location"] = not_view[0].replace("\n", "").strip()
                else:
                    view = ": ".join([parser.xpath("//*[@class='detailField currentLocationField']/span[@class='detailFieldLabel']/text()")[0], parser.xpath("//*[@class='detailField currentLocationField']/span[@class='detailFieldValue']/text()")[0].replace("\n", "").strip()])
                    data["current_location"] = view


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

# scraper("extracted_data.csv", 55000, 60600, 1, "")
