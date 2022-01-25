import csv
from tqdm import tqdm
from dateutil import parser

#﻿PARCEL_ID,PROPERTY_L,,SALE_DATE,SALE_PRICE,
columns = ["property_id", "physical_address", "sale_date", "sale_price", "county", "state", "source_url"]
with open("Parcels.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                if row["SALE_DATE"] != "0.00000000000":
                    try:
                        land_info = {
                            "property_id": row["﻿PARCEL_ID"],
                            "physical_address": " ".join(str(row["PROPERTY_L"]).upper().strip().split()),
                            "sale_price": str(row["SALE_PRICE"]).split(".")[0],
                            "sale_date": str(parser.parse(str(row["SALE_DATE"]).split(".")[0])),
                            "county": "Martin",
                            "state": "NC",
                            "source_url": "https://gis.martincountyncgov.com/DataDownloads/"
                        }



                        year = land_info["sale_date"].split("-")[0]

                        if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                            writer.writerow(land_info)

                    except KeyError as e:
                        print(e)
                        pass


            except parser._parser.ParserError:
                print("PARSER")
                pass
