import csv
from tqdm import tqdm
from dateutil import parser
import sqlite3
import pandas as pd
import json

#	ParcelID	Situs	LandUse	City	ZipCode

columns = ["property_id", "property_street_address", "sale_datetime", "sale_price", "property_type", "book", "page", "property_zip5", "state", "property_county", "property_city", "source_url", "seller_name", "appraisal_total", "land_appraisal_total", "building_appraisal_total", "assessed_total", "land_area_acres"]

conn = sqlite3.connect(':memory:')

csv_data = pd.read_csv("tax_sales.csv")
csv_data.to_sql('sales', conn, if_exists="replace", index=False)
cur = conn.cursor()


with open("PropertyProfile.csv", "r", encoding='utf-8') as input_csv:
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
                    "state": "GA",
                    "property_county": "Fulton",
                    "source_url": "https://gisdata.fultoncountyga.gov/datasets/tax-parcels-2021",
                    "property_id": row["ParcelID"],
                    "property_city": row["City"],
                    "property_zip5": row["ZipCode"],
                    "property_type": row["LandUse"],
                    "property_street_address": " ".join(str(row["Situs"]).upper().split()),
                    "appraisal_total": row["ApprValue"],
                    "land_appraisal_total": row["ApprLand"],
                    "building_appraisal_total": row["ApprImpr"],
                    "assessed_total": row["Assessed"],
                    "land_area_acres": row["LandArea"],
                }

                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""


                for results in cur.execute(f"SELECT * FROM sales WHERE ParcelID = '{row['ParcelID']}';"):
                    # print(results)
                    sale_date = str(results[5]).split(" ")[0]
                    year = sale_date.split("-")[0]
                    #
                    # if int(year) > 2022:
                    #     year = sale_date.split("-")[0]
                    #     sale_date = "19" + str(year)[2:] + sale_date.replace(year, "")
                    land_info["sale_datetime"] = str(parser.parse(sale_date))
                    land_info["sale_price"] = int(results[6])

                    # Delete if no book
                    # Update field
                    book = str(results[3]).strip()
                    page = str(results[4]).strip()

                    try:
                        if int(book) != 0 and int(page) != 0:
                            land_info["book"] = int(book)
                            land_info["page"] = int(page)

                    except ValueError:
                        pass

                    # land_info["book"] = results[3]
                    # land_info["page"] = results[4]
                    try:
                        land_info["seller_name"] = " ".join(results[7].split())
                    except:
                        pass

                    year = land_info["sale_date"].split("-")[0]

                    if land_info["property_street_address"] and land_info["sale_datetime"] and land_info["sale_price"] != "" and int(year) <= 2022:
                        writer.writerow(land_info)

            except Exception as e:
                print(e)
