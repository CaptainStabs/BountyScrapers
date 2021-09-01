import os
import pandas as pd
import csv
from bs4 import BeautifulSoup
from utils.interrupt_handler import GracefulInterruptHandler
from tqdm import tqdm
import requests
import traceback
import urllib
from lxml import html
import time

columns = ["name", "city", "state", "district", "DISTRICTID"]
headers = {
    "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    "sec-ch-ua-mobile": "?0",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
}

input_file = "HIFLD_less_fields.csv"

df = pd.read_csv(input_file)
df_columns = list(df.columns)
data_columns = ",".join(map(str, df_columns))

with GracefulInterruptHandler() as h:
    with open("districts2.csv", "a", encoding="utf-8") as output_source:
        writer = csv.DictWriter(output_source, fieldnames=columns)

        if os.stat("districts2.csv").st_size == 0:
            writer.writeheader()

        file_length = 0
        file_length = len(open(input_file, encoding='utf8').readlines())

        for index, row in tqdm(df.iterrows(), total=file_length):
            if h.interrupted:
                print("   [!] Interrupted, exiting")
                break

            name = urllib.parse.quote_plus(str(row["name"]))
            city = urllib.parse.quote_plus(str(row["city"]))
            county = urllib.parse.quote_plus(str(row["county"]))

            try:
                search_query = f"https://nces.ed.gov/ccd/schoolsearch/school_list.asp?Search=1&InstName={name}&City={city}&County={county}"
                response = requests.request("GET", search_query, headers=headers)
                html_page = response.text

            except TimeoutError as e:
                traceback.print_exc()
                time.sleep(1)
                pass

            soup = BeautifulSoup(html_page, "html.parser")

            for link in soup.findAll("a"):
                if link.get("href") is None:
                    continue

                if not link["href"].startswith("school_detail.asp"):
                    continue

                school_path = link["href"].lstrip("..")
                school_url = "https://nces.ed.gov/ccd/schoolsearch/" + school_path
                print(school_url)
                break

            try:
                school_response = requests.request("GET", school_url, headers=headers)
                school_page = response.text

            except TimeoutError:
                time.sleep(1)
                pass

            school_soup = BeautifulSoup(school_page, "html.parser")
            with open("t.txt", "w") as f:
                f.write(school_page)
                os.exit()
                if link.get("href") is None:
                    continue

                if "../districtsearch/district_detail.asp?" not in link["href"]:
                    continue

                print(link)
                district_path = link["href"].lstrip("..")
                print(district_path)
                district_link = "https://nces.ed.gov/ccd/" + str(district_path)
                print(district_link)
                print
                district_page = requests.request("GET", district_link, headers=headers)

                tree = html.fromstring(district_page.content)
                district = tree.xpath("/html/body/div[1]/div[3]/table/tbody/tr[4]/td/table/tbody/tr[1]/td[1]/font[1]/text()")
                print("District: " + str(district))
