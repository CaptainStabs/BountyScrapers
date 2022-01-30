import csv
from tqdm import tqdm
from dateutil import parser
import sqlite3
import pandas as pd
import json

# Property file
# Property ID,Situs_Address,PropertySubType

# Transfer file
# Property ID,OR Book #,OR Page #,Sale Date,Buyer,Seller,Sale Price
columns = ["property_id", "physical_address", "property_type", "book", "page", "sale_date", "buyer_name", "seller_name", "sale_price", "county", "state", "source_url"]

conn = sqlite3.connect(':memory:')

csv_data = pd.read_csv("Sales.csv")
csv_data.to_sql('sales', conn, if_exists="replace", index=False)
cur = conn.cursor()

with open("Property.csv", "r", encoding='utf-8') as input_csv:
    line_count = 0
    # Count lines in file
    for line in input_csv.readlines():
        line_count += 1

    # Seek back to 0 to allow csv to read full file
    input_csv.seek(0)

    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": str(row["Property_ID"]).strip(),
                    "physical_address": " ".join(str(row["Situs_Address"]).upper().split()),
                    "county": "INDIAN RIVER",
                    "state": "FL",
                    "source_url": "https://www.ircpa.org/site-links/pro-tools-page/"
                }

                prop_type = str(row["PropertySubType"]).strip()

                if prop_type == "RES":
                    land_info["property_type"] = "RESIDENTIAL"
                elif prop_type == "CONDO":
                    land_info["property_type"] = "CONDO"
                elif prop_type == "COMM":
                    land_info["property_type"] = "COMMERCIAL"]
                else:
                    land_info["property_type"] = prop_type.upper()

                    # Property ID,OR_Book_#,OR_Page_#,Sale_Date,Buyer,Seller,Sale_Price
                for results in cur.execute(f"SELECT OR_Book_#, OR_Page_#, Sale_Date, Buyer, Seller, Sale_Price FROM sales WHERE  Property_ID = '{row['Property_ID']}';"):
                    # Delete if no book
                    # Update field
                    book = str(results[0]).strip()
                    page = str(results[1]).strip()

                    try:
                        if int(book) != 0 and int(page) != 0:
                            land_info["book"] = int(book)
                            land_info["page"] = int(page)

                    except ValueError:
                        pass

                    # print(results)
                    land_info["sale_date"] =  str(parser.parse(str(results[2]).strip()))

                    land_info["buyer_name"] = " ".join(str(results[3]).split())
                    land_info["seller_name"] = " ".join(str(results[4]).split())
                    land_info["sale_price"] = int(results[5])


                    year = land_info["sale_date"].split("-")[0]

                    if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                        writer.writerow(land_info)

            except Exception as e:
                print(e)
