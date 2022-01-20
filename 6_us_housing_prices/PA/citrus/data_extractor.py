import csv
from tqdm import tqdm
from dateutil import parser
import sqlite3
import pandas as pd
import json

#,LASTSALEDT,LASTSALEPRICE,,,RES_YRBUILT,COMM_YRBUILT,SITE_ZIP

columns = ["property_id", "num_units", "physical_address", "sale_date", "sale_price", "book", "page", "year_built", "zip5", "state", "county", "city", "source_url"]

conn = sqlite3.connect(':memory:')

csv_data = pd.read_csv("VD_SALES.dat")
csv_data.to_sql('sales', conn, if_exists="replace", index=False)
cur = conn.cursor()


with open("VD_PARCELDATA.dat", "r") as input_csv:
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
                    "state": "PA",
                    "county": "Citrus",
                    "source_url": "https://www.citruspa.org/_dnn/Downloads",
                    "property_id": row["PARCELID"],
                    "city": row["SITE_ADRCITY"],
                    "zip5": row["SITE_ZIP"]
                }

                if int(row["NUMBLDG"]):
                    land_info["num_units"] = int(row["NUMBLDG"])

                if row["RES_YRBUILT"]:
                    land_info["year_built"] = row["RES_YRBUILT"]
                elif row["COMM_YRBUILT"]:
                    land_info["year_built"] = row["COMM_YRBUILT"]

                street_list = [str(row["SITE_ADRNO"]).strip(), str(row["SITE_ADRDIR"]).strip(), str(row["SITE_ADRSTR"]).strip(), str(row["SITE_ADRSUF"]).strip(), str(row["SITE_ADRSUF2"]).strip(), str(row["SITE_UNITNO"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                for results in cur.execute(f'SELECT * FROM sales WHERE ALTKEY = {row["ALTKEY"]};'):
                    sale_date = str(parser.parse(results[1]))
                    year = sale_date.split("-")[0]

                    if int(year) > 2022:
                        year = sale_date.split("-")[0]
                        sale_date = "19" + str(year)[2:] + sale_date.replace(year, "")
                    land_info["sale_date"] = str(parser.parse(results[1]))
                    land_info["sale_price"] = int(results[2])
                    land_info["book"] = results[3]
                    land_info["page"] = results[4]

                    if land_info["physical_address"] and land_info["sale_date"]:
                        writer.writerow(land_info)
            except Exception as e:
                print(e)
