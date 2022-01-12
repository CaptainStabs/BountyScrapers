import requests
import csv
from tqdm import tqdm
from lxml.html import fromstring
from dateutil import parser as dateparser
import pandas as pd
import os
import time


filename = "records.csv"
payload={}
headers = {
  'Cookie': 'ASP.NET_SessionId=4oh40r3srgv5iqvksyzdf00h'
}

columns = ["state", "physical_address", "county", "property_id", "sale_date", "property_type", "sale_price", "year_built", "source_url", "id"]
with open(filename, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, fieldnames=columns)

    if os.path.exists(filename) and os.stat(filename).st_size >= 1:
        df = pd.read_csv(file_name)
        df_columns = list(df.columns)
        data_columns = ",".join(map(str, df_columns))

        # Get the last row from df
        last_row = df.tail(1)
        # Access the corp_id
        last_id = last_row["corp_id"].values[0]
        last_id += 1
    else:
        last_id = 0
        writer.writeheader()

    # Believe it ends at 99992, but I'll just end at 999999 just in case
    for id in tqdm(range(last_id, 99999)):
        id = "P" + str(id)
        url = f"https://skagitcounty.net/Search/Property/?id={id}"

        request_success = False
        request_tries = 0
        while not request_success or request_tries > 10:
            try:
                response = requests.request("GET", url, headers=headers, data=payload)
                request_success = True
            except requests.exceptions.ConnectionError:
                print("  [!] Connection Closed! Retrying in 1...")
                time.sleep(1)
                # response = requests.request("GET", url, headers=get_user_agent(), data=payload)
                request_success = False

        if request_success:
            parser = fromstring(response.text)

            try:
                parser.xpath('//*[@id="content_pdata"]/div[2]/text()')[0]
                has_data = True
            except IndexError:
                has_data = False

            if has_data:
                land_info = {
                    "state": "WA"
                    "physical_address": " ".join(str(parser.xpath('//*[@id="content_pdata"]/table[3]/tbody/tr/td[2]/table/tbody/tr[2]/td/text()')[0]).split()).upper().strip(),
                    "county": " ".join(str(parser.xpath('//*[@id="jurisdiction"]/text()')[0]).split()).upper().strip(),
                    "property_id": str(parser.xpath('//*[@id="content_pdata"]/table[2]/tbody/tr[2]/td[1]/b/text()')[0]).strip(),
                    "sale_date": dateparser.parse(str(parser.xpath('//*[@id="content_pdata"]/table[5]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]/text()')[0]).strip()),
                    "property_type": " ".join(str(parser.xpath('//*[@id="content_pdata"]/table[7]/tbody/tr[6]/td[2]/text()')[0]).split()).upper().strip(),
                    "year_built": str(parser.xpath('//*[@id="content_pdata"]/table[7]/tbody/tr[7]/td[2]/text()')).strip(),
                    "source_url": url,
                    "deed_type": str(parser.xpath('//*[@id="content_pdata"]/table[5]/tbody/tr[2]/td[2]/table/tbody/tr[1]/td[2]/text()')[0]),
                    "id": id
                }

                sale_price = "sale_price": str(parser.xpath('//*[@id="content_pdata"]/table[5]/tbody/tr[2]/td[2]/table/tbody/tr[3]/td[2]/text()')[0]).strip().replace("$", "").replace(",", "").split(".")[0],

                if sale_price:
                    land_info["sale_price"] = sale_price

                writer.writerow(land_info)
