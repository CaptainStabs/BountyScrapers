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
    writer = csv.DictWriter(f, fieldnames=columns)

    # if os.path.exists(filename) and os.stat(filename).st_size > 3:
    #     df = pd.read_csv(filename)
    #     df_columns = list(df.columns)
    #     data_columns = ",".join(map(str, df_columns))
    #
    #     # Get the last row from df
    #     last_row = df.tail(1)
    #     # Access the corp_id
    #     last_id = int(str(last_row["id"].values[0]).lstrip("P"))
    #     last_id += 1
    # else:
    #     last_id = 0
    #     writer.writeheader()

    # Believe it ends at 99992, but I'll just end at 999999 just in case
    last_id = 19666
    for id in tqdm(range(last_id, 135909)):
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

            with open("test.html", "w") as f:
                f.write(response.text)

        if request_success:
            parser = fromstring(response.text)

            try:
                parser.xpath('//*[@id="content_pdata"]/div[2]/text()')[0]
                has_data = False

            except IndexError:
                has_data = True
            try:
                if has_data:
                    land_info = {
                        "state": "WA",
                        "county": " ".join(str(parser.xpath('//*[@id="jurisdiction"]/text()')[0]).split()).upper().strip(),
                        "property_id": id,
                        "property_type": " ".join(str(parser.xpath('/html/body/div/div[7]/table/tr/td[2]/div/div/form/div[2]/table[7]/tr[6]/td[2]/text()')[0]).split()).upper().strip(),
                        "source_url": url,
                        "id": id
                    }

                    sale_price = str(parser.xpath('//*[@id="content_pdata"]/table[5]/tr[2]/td[2]/table/tr[3]/td[2]/text()')[0]).strip().replace("$", "").replace(",", "").split(".")[0]

                    if sale_price:
                        land_info["sale_price"] = sale_price


                    do_save = True
                    try:
                        land_info["year_built"] = str(parser.xpath('//*[@id="content_pdata"]/table[7]/tr[7]/td[2]/text()')).strip()

                    except IndexError:
                        pass

                    try:
                        land_info["physical_address"] =  " ".join(str(parser.xpath('//*[@id="content_pdata"]/table[3]/tr/td[2]/table/tr[2]/td/text()')[0]).split()).upper().strip()

                    except IndexError:
                        do_save = False

                    try:
                        land_info["sale_date"] = dateparser.parse(str(parser.xpath('//*[@id="content_pdata"]/table[5]/tr[2]/td[2]/table/tr[2]/td[2]/text()')[0]).strip())

                    except IndexError:
                        do_save = False




                    writer.writerow(land_info)

            except IndexError as e:
                print("\n", e)
                print("ID:", id)
