import requests
import jmespath
import json
from dateutil import parser
from tqdm import tqdm
import csv
import pandas as pd
import os
import time
# from deed_scraper import get_deed

url = "https://property.spatialest.com/nc/durham/data/propertycard"


headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
#  'Cookie': 'XSRF-TOKEN=eyJpdiI6IjA4cHFaaytiT1kxWVNPN1VPcWhRQ1E9PSIsInZhbHVlIjoiN1VIK0hlc1BabXpIbkFMVVpKRENlUzBmaThSZHFFUzF6ZTJZdUMwTWwwK3E1anUrakV2UkhqZEdXbFhtMEoraCIsIm1hYyI6ImZjODQ1M2YxYTdkZmJkYjU1YzZjMTYzOTBlYmI1ZTBjZDJhYWJlOTlkZDM4ZmQ1NDAzODExYzZiZWZiMGQ3YmMifQ%3D%3D; laravel_session=eyJpdiI6Iis0XC8xTTFmVWw4V2hUS0ZvbURDREVBPT0iLCJ2YWx1ZSI6IjRGODhVN1FFZmRJbkdXRFVHR0NCQlRPZGtsOHpYXC9tZlB6cHNFOUtST0ZVMjNJcUFNK3B1b2pLN1RMQm1qVEVmIiwibWFjIjoiZWExZmIxNTFkM2RjM2QwNWViNmZmNDI4N2JiOTJlM2M2MDcwYzcyNGNhZDY3NGE2MDNiMTM4MGRhMjgyMTk0ZiJ9'
}

columns = ["state", "county", "physical_address", "property_type", "book", "page", "sale_price", "sale_date", "property_id", "source_url", "year_built"]
filename = "land_info.csv"

with open(filename, "a", newline="", encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    if os.path.exists(filename) and os.stat(filename).st_size > 3:
        df = pd.read_csv(filename)
        df_columns = list(df.columns)
        data_columns = ",".join(map(str, df_columns))

        # Get the last row from df
        last_row = df.tail(1)
        # Access the corp_id
        last_id = last_row["property_id"].values[0]
        last_id += 1
    else:
        last_id = 100000
        writer.writeheader()

    for parcel_id in tqdm(range(last_id, 293000)):
        payload=f'card=&parcelid={parcel_id}&year='

        request_success = False
        request_tries = 0

        while not request_success or request_tries > 10:
            try:
                response = requests.request("POST", url, headers=headers, data=payload)
                request_success = True
            except requests.exceptions.ConnectionError:
                print("  [!] Connection Closed! Retrying in 1...")
                time.sleep(1)
                # response = requests.request("GET", url, headers=get_user_agent(), data=payload)
                request_success = False

        cleaned_response = str(response.text).replace("\\", "").strip('"')
        json_data = json.loads(cleaned_response)
        # print(cleaned_response)

        if json_data['found']:
            parcel = json_data['parcel']
            sale_date = parcel["keyinfo"][10]["value"]
            sale_price =  parcel["keyinfo"][11]["value"]
            if sale_date != "-" and sale_price != "-":
                book = parcel["keyinfo"][8]["value"].split(" / ")[0]
                page =  parcel["keyinfo"][8]["value"].split(" / ")[1]

                # deed_info = get_deed(book, page)

                land_info = {
                    "state":"NC",
                    "county":"DURHAM",
                    "physical_address": str(parcel["header"]["location"]["value"]).upper().strip(),
                    "property_type": " ".join(parcel["keyinfo"][5]["value"].split()).strip().upper(),
                    "book": book,
                    "page": page,
                    "sale_price": sale_price.lstrip("$").replace(",", ""),
                    "sale_date": parser.parse(sale_date),
                    "property_id": json_data["id"],
                    "source_url": f"https://property.spatialest.com/nc/durham/#/property/{parcel_id}"
                }

                try:
                    year_built = parcel["buildings"]["residential"][0]["display"][0]["value"]

                except KeyError:
                    print(parcel["buildings"])
                    break

                writer.writerow(land_info)




        # break
        # expression = jmespath.compile('data.menusV3.menus[][name, groups[].[name, items[*][name,price,calories]]]')
        # #expression = jmespath.compile('length(data)')
        # data = json.loads(menu_response.text)
        # searched = expression.search(data)
