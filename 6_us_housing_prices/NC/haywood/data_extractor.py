import csv
from tqdm import tqdm
from dateutil import parser

# ﻿ALPHA, Prop_Addr,Sale_Date_,Sale_Price,,Yr_Built,Land_Desc,
columns = ["property_id", "physical_address", "sale_date", "sale_price", "year_built", "property_type", "county", "state", "source_url"]

with open("Parcels.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="", encoding="utf-8") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["﻿ALPHA"],
                    "physical_address": " ".join(str(row["Prop_Addr"]).upper().strip().split()),
                    "sale_date": str(parser.parse(row["Sale_Date"])),
                    "sale_price": str(row["Sale_Price"]).split(".")[0],
                    "property_type": " ".join(str(row["Land_Desc"]).upper().strip().split()),
                    "county": "Haywood",
                    "state": "NC",
                    "source_url": "http://maps.haywoodcountync.gov/downloads/Parcels.zip"
                }


                # Delete if no year_built
                try:
                    if int(row["Yr_Built"]) != 0 and int(row["Yr_Built"]) <= 2022:
                        land_info["year_built"] = row["Yr_Built"]

                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
