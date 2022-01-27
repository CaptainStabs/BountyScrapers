import csv
from tqdm import tqdm
from dateutil import parser as dateparser
import requests
import time
from lxml.html import fromstring


headers = {
  'Cookie': 'CFGLOBALS=urltoken%3DCFID%23%3D8270217%26CFTOKEN%23%3D4c12c414b5486fbd%2D1C0152A9%2DC5EE%2D0D6F%2D56B2C06400CE4843%23lastvisit%3D%7Bts%20%272022%2D01%2D27%2011%3A42%3A55%27%7D%23hitcount%3D7%23timecreated%3D%7Bts%20%272022%2D01%2D27%2011%3A39%3A26%27%7D%23cftoken%3D4c12c414b5486fbd%2D1C0152A9%2DC5EE%2D0D6F%2D56B2C06400CE4843%23cfid%3D8270217%23; CFID=8270217; CFTOKEN=4c12c414b5486fbd-1C0152A9-C5EE-0D6F-56B2C06400CE4843'
}

# PIN,DEED_BOOK,DEED_PAGE,,STREET_ADD,SALES_AMT,YEAR_BUILT,DESCRIPTIO,,DEEDLINK,
columns = ["pin", "book", "page", "physical_address", "sale_price", "sale_date", "seller_name", "county", "state", "source_url"]
with open("tax_parcels.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": str(row["﻿PIN"]).strip(),
                    "physical_address": " ".join(str(row["STREET_ADD"]).upper().split()),
                    "sale_price": row["SALES_AMT"],
                    "property_type": row["DESCRIPTIO"].strip(),
                    "source_url": row["TAXCARD"]
                }

                # Delete if no book
                # Update field
                book = str(row["DEED_BOOK"]).strip()
                page = str(row["DEED_PAGE"]).strip()

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = int(book)
                        land_info["page"] = int(page)

                except ValueError:
                    pass

                # Delete if no year_built
                try:
                    if int(row["YEAR_BUILT"]) != 0 and int(row["YEAR_BUILT"]) <= 2022:
                        land_info["year_built"] = row["YEAR_BUILT"]

                except ValueError:
                    pass

                request_success = False
                request_tries = 0

                while not request_success and request_tries < 10:
                    try:
                        response = requests.request("GET", "https://" + str(land_info["source_url"]), headers=headers)
                        request_success = True
                    except requests.exceptions.ConnectionError:
                        print("  [!] Connection Closed! Retrying in 1...")
                        time.sleep(1)
                        # response = requests.request("GET", url, headers=get_user_agent(), data=payload)
                        request_success = False
                        request_tries += 1

                parser = fromstring(response.text)

                land_info["sale_date"] = str(dateparser.parse(parser.xpath('/html/body/form/table[2]/tbody/tr/td/table[3]/tbody/tr/td[2]/table[2]/tbody/tr[13]/td[2]/div/font/font/strong/text()')))
                land_info["seller_name"] = " ".join(str(parser.xpath('/html/body/form/table[2]/tbody/tr/td/table[3]/tbody/tr/td[2]/table[2]/tbody/tr[11]/td[2]/div/font/strong/text()')).split())

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
