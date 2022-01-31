import csv
from tqdm import tqdm
from dateutil import parser
import usaddress
import json

# ﻿PARCEL_ID,,Situs_Addr,Situs_City,Classifica,,Sale_Date,Price,
columns = ["property_id", "physical_address", "city", "zip5", "property_type", "sale_date", "sale_price", "county", "state", "source_url"]
with open("AssessorParcels_WGS.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["﻿PARCEL_ID"].strip(),
                    "physical_address": " ".join(str(row["Situs_Addr"]).upper().split()),
                    # "city": " ".join(str(row["Situs_City"]).upper().split()),
                    "property_type": " ".join(str(row["Classifica"]).upper().split()),
                    "sale_date": str(parser.parse(row["Sale_Date"])),
                    "sale_price": str(row["Price"]).split(".")[0],
                    "county": "ARAPAHOE",
                    "state": "CO",
                    "source_url": "https://www.arapahoegov.com/1151/GIS-Data-Download"

                }

                city = " ".join(str(row["Situs_City"]).upper().split())
                try:
                    parsed_address = usaddress.tag(city)
                    parse_success = True

                except usaddress.RepeatedLabelError as e:
                    print(e)
                    parse_success = False

                if parse_success:
                    try:
                        parsed_city = str(parsed_address[0]["PlaceName"]).strip()
                        if parsed_city != "CO":
                            if parsed_city == "ENGELWOOD":
                                land_info["city"] = "ENGLEWOOD"
                            else:
                                land_info["city"] = str(parsed_address[0]["PlaceName"]).strip()
                    except KeyError:
                        # print(city)
                        pass

                    try:
                        land_info["zip5"] = parsed_address[0]["ZipCode"].split("-")[0]
                        if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                            land_info["zip5"] = ""
                    except KeyError:
                        # print(city)
                        pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
