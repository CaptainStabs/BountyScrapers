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

        if r.status_code == 403:
            return

        r = r.text
        x=10
        return r            # if x == 4:
            #     raise(e)
        x += 1

def scraper(filename, start_num, end_num, position, lock):
    # with lock:
    #     bar = tqdm(
    #         desc=f'Position {position}',
    #         total=end_num,
    #         position=position,
    #         leave=False
    #     )
    # filename, start_num, end_num = filename[0], filename[1], filename[2]
    # signal.signal(signal.SIGINT, signal.SIG_IGN)
    print(start_num, end_num, filename)
    if os.path.exists(filename) and os.stat(filename).st_size > 515:
        start_id = get_last_id(filename, 515)
    else:
        start_id = start_num
    print(start_id)
    columns = ['institution_name', 'institution_city', 'institution_state', 'institution_country', 'institution_latitude', 'institution_longitude', 'title', 'maker_full_name', 'maker_role', 'maker_birth_year', 'maker_death_year', 'date_description', 'culture', 'materials', 'category', 'object_number', 'inscription', 'image_url', 'description', 'department', 'maker_full_name', 'provenance', 'from_location', 'dimensions', 'source_1', 'drop_me']

    remove_escaped = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        s = requests.Session()
        for id in tqdm(range(start_id, end_num)):
            try:
                url = f"https://collections.peabody.harvard.edu/objects/details/{id}"
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
                dimens = parser.xpath("//*[@class='detailField dimensionsField']/span[@class='detailFieldValue']/text()")
                insc = parser.xpath("//*[@class='detailField inscribedField']/span[@class='detailFieldValue']/text()")
                cult = parser.xpath("//*[@class='detailField cultureField']/span[@class='detailFieldValue']/text()")

                cur_loc = parser.xpath("//*[@class='detailField onviewField']/div/text()")
                desc = parser.xpath('//*[@class="detailField titleField paragraph2"]/span[2]/text()')
                mat = parser.xpath("//*[@class='detailField mediumField']/span[@class='detailFieldValue']/a/text()")
                cred_line = parser.xpath("//*[@class='detailField creditlineField']/span[@class='detailFieldValue']/text()")
                dep = parser.xpath("//*[@class='detailField departmentField']/span[@class='detailFieldValue']/a/text()")
                maker = parser.xpath("//*[@class='detailField peopleField']/span[@class='detailFieldValue']/span/text()")
                from_loc = parser.xpath("//*[@class='thes-path-flat']/div/div/span/text()")


                desc_stuff = [x.replace("\n", "").strip() for x in parser.xpath('//*[@class="emuseum-detail-category detailField thesconceptsField"]/span[@class="detailFieldLabel"]/text()')]

                culture, cate = None, None
                if "Culture" in desc_stuff:
                    cult_ind = desc_stuff.index("Culture")
                    cult = parser.xpath(f'//*[@class="emuseum-detail-category detailField thesconceptsField"][{cult_ind+1}]/ul/li/span/text()')

                if "Classification" in desc_stuff:
                    cate_ind = desc_stuff.index("Classification")
                    cate = parser.xpath(f'//*[@class="emuseum-detail-category detailField thesconceptsField"][{cate_ind+1}]/ul/li/span/text()')


                prov_stuff = parser.xpath("//*[@class='detailField peopleField paragraph2']/span/span[@property='name']/text()")
                prov_role = parser.xpath("//*[@class='detailField peopleField paragraph2']/span[@class='detailFieldLabel']/text()")
                prov = None
                if prov_stuff:
                    prov_stuff = [x.replace("\n", "").strip() for x in prov_stuff]
                    prov = [f'{prov_role[i]}: {prov_stuff[i]}' for i in range(len(prov_role))]

                data = {
                    "institution_name": "Peabody Museum of Archaeology and Ethnology",
                    "institution_city": "Cambridge",
                    "institution_state": "Massachusetts",
                    "institution_country": "United States",
                    "institution_latitude": 42.37825443020888,
                    "institution_longitude": -71.11467238420505,
                    "title": parser.xpath('//*[@class="detailField titleField"]/span[@class="detailFieldValue"]/text()')[0].replace("\n", "").strip(),
                    "maker_full_name": "|".join(names) if names else None,
                    "maker_role": "|".join(roles) if roles else None,
                    "maker_birth_year": birth,
                    "maker_death_year": death,
                    "date_description": date_desc[0].replace("\n", "").strip() if date_desc else None,
                    "culture": "|".join(cult) if cult else None,
                    "materials": mat[0].replace("\n", "").strip() if mat else None,
                    "category": "|".join(cate) if cate else None,
                    "object_number": parser.xpath("//*[@class='detailField invnoField']/span[@class='detailFieldValue']/text()")[0].replace("\n", "").strip(),
                    "inscription": insc[0] if insc else None,
                    "image_url": "https://collections.peabody.harvard.edu/" + str(img[0]) if img else None,
                    "description": " ".join(desc).replace("\n", "").strip() if desc else None,
                    "department": dep[0].replace("n", "").strip() if dep else None,
                    "maker_full_name": "|".join([x.replace("n", "").strip() for x in maker]) if maker else None,
                    "provenance": "; ".join(prov) if prov else None,
                    "from_location": " / ".join(from_loc) if from_loc else None,
                    "dimensions": dimens[0].replace("\n", "").strip() if dimens else None,
                    "source_1": url,
                    "drop_me": id
                }

                writer.writerow(data)

                # with lock:
                #     bar.update(1)

            except KeyboardInterrupt:
                return

            except Exception:
                print("\nCRASHED ID:",url)
                tb.print_exc()
                # send_mail("script crashed", "")
                raise

        # with lock:
        #     bar.close()


# scraper("extracted_data.csv", 0, 400, 1, "")
