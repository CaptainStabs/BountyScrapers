import csv
from tqdm import tqdm
from dateutil import parser
import sqlite3
import pandas as pd
import json

# Master file
# ParcelID|YearBuilt|Situs Address|Situs City|SalePrice|SaleDate|Grantee|Grantor|

# Transfer file
# ParcelID|SaleDate|RecordedDate|SalePrice|Book|Page||GrantorName|GranteeName
columns = ["property_id", "property_type", "physical_address", "city", "sale_date", "sale_price", "book", "page", "seller_name", "buyer_name"]

conn = sqlite3.connect(':memory:')

csv_data = pd.read_csv("tax_transfers.csv")
csv_data.to_sql('sales', conn, if_exists="replace", index=False)
cur = conn.cursor()


with open("real_master.csv", "r", encoding='utf-8') as input_csv:
    line_count = 0
    # Count lines in file
    for line in input_csv.readlines():
        line_count += 1

    # Seek back to 0 to allow csv to read full file
    input_csv.seek(0)

    reader = csv.DictReader(input_csv, delimiter="|")

    with open("C:\\Users\\adria\\github\\BountyScrapers\\6_us_housing_prices\\GA\\atlanta\\extracted_data.csv", "a") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": str(row["ParcelID"]).strip(),
                    "property_type": str(row["LandUseCodeDescription"].replace(str(row["LandUseCode"]), "")).strip(),
                    "physical_address": " ".join(str(row["Situs Address"]).upper().split()),
                    "city": row["Situs City"].strip(),
                }


                # Delete if no year_built
                try:
                    if int(row["YearBuilt"]) != 0 and int(row["YearBuilt"]) <= 2022:
                        land_info["year_built"] = row["YearBuilt"]

                except ValueError:
                    pass

                for results in cur.execute(f"SELECT SaleDate, SalePrice, Book, Page, GrantorName, GranteeName FROM sales WHERE ParcelID = '{row['ParcelID']}';"):
                    # print(results)
                    land_info["sale_date"] =  str(parser.parse(str(results[0]).strip()))
                    land_info["sale_price"] = int(results[1])

                    # Delete if no book
                    # Update field
                    book = str(results[2]).strip()
                    page = str(results[3]).strip()

                    try:
                        if int(book) != 0 and int(page) != 0:
                            land_info["book"] = int(book)
                            land_info["page"] = int(page)

                    except ValueError:
                        pass


                    try:
                        land_info["seller_name"] = " ".join(str(results[4]).split())
                    except:
                        pass

                    try:
                        land_info["buyer_name"] = " ".join(str(results[5]).split())
                    except:
                        pass


                    year = land_info["sale_date"].split("-")[0]

                    if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                        writer.writerow(land_info)

            except Exception as e:
                print(e)
