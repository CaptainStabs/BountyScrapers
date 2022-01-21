import csv
from dateutil import parser
from tqdm import tqdm

# MultipleImprovements,,PropertyType,
columns = ["property_id", "physical_address", "book", "page", "sale_date", "sale_price", "seller_name", "city", "property_type", "num_units", "county", "state", "source_url"]

with open("Chatham_County.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["Full_AKPAR"].strip().strip(),
                    "physical_address": " ".join(str(row["PhysicalAddress"]).upper().strip().split()),
                    "sale_date": str(parser.parse(str(row["DateSold"]).strip())),
                    "sale_price": str(row["SaleAmount"]).strip(),
                    "city": " ".join(str(row["CityCodeDescription"]).strip().upper().replace(" ETJ", "").split()),
                    "property_type": str(row["PropertyUseType"]).strip(),
                    "county": "Chatham",
                    "state": "NC",
                    "source_url": "https://opendata-chathamncgis.opendata.arcgis.com/datasets/ChathamncGIS::chatham-county-parcels-tax-data/about"
                }

                seller_name = [" ".join(str(row["GrantorName1"]).strip().split()), " ".join(str(row["GrantorName2"]).strip().split())]
                seller_name = ', '.join(filter(None, seller_name)).upper()
                land_info["seller_name"] = seller_name

                try:
                    if int(row["DeedBook"]) != 0 and int(row["DeedPage"]) != 0:
                        land_info["book"] = str(row["DeedBook"]).strip()
                        land_info["page"] = str(row["DeedPage"]).strip()
                except ValueError:
                    continue

                try:
                    if int(row["MultipleImprovements"]) != 0:
                        land_info["num_units"] = row["MultipleImprovements"]

                except ValueError:
                    continue

                if land_info["sale_date"] and land_info["physical_address"]:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                continue
