import requests
import os
import pandas as pd
import csv
import time
import sys
from utils.interrupt_handler import GracefulInterruptHandler
from bs4 import BeautifulSoup
from _secrets import notify_url

columns = ["name", "city", "state", "district"]

headers = {
  'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
  'sec-ch-ua-mobile': '?0',
  'Upgrade-Insecure-Requests': '1',
  'DNT': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-User': '?1',
  'Sec-Fetch-Dest': 'document',
}

print("   [*] Opening Source File...")
with GracefulInterruptHandler() as h:
    with open("HIFLD_Schools.csv","r", encoding="utf-8") as input_source:
        df = pd.read_csv(input_source)
        df_columns = list(df.columns)
        data_columns = ",".join(map(str, df_columns))

        print("      [*] Opening output...")
        with open("districts_added.csv", "a", encoding="utf-8") as output_source:
            writer = csv.DictWriter(output_source, fieldnames=columns)
            if os.stat("districts_added.csv").st_size == 0:
                writer.writeheader()

            for index, row in df.iterrows():
                if h.interrupted:
                    print("      [!] Interrupted, exiting")
                    break

                try:
                    district_id = row["DISTRICTID"]
                    no_error = True
                except KeyError:
                    print(f"            [!] Error on index: {index}")
                    no_error = False
                    pass

                if no_error:
                    search_query = f"https://nces.ed.gov/ccd/districtsearch/district_list.asp?Search=1&details=1&InstName=&DistrictID={district_id}"
                    response = requests.request("GET", search_query, headers=headers)
                    html_page = response.text

                    soup = BeautifulSoup(html_page, "html.parser")

                    for link in soup.findAll("a"):
                        if link.get("href") is None:
                            continue
                        if not link["href"].startswith("district_detail.asp?"):
                            continue

                        district = link.string
                        print(f"         [*] District Name: {district}")

                    school_info = {}
                    school_info["name"] = row["name"].upper()
                    school_info["city"] = row["city"].upper()
                    school_info["state"] = row["state"].upper()
                    school_info["district"] = district.upper()
                    writer.writerow(school_info)
