import csv
from tqdm import tqdm
from dateutil import parser

#PID,PropertyHouseNo,PropertyAddress,,,,,,,,YearBuilt,LastSaleDate,LastSalePrice,,PropertyCity,PropertyZip,
columns = ["property_id", "physical_address", "property_type", "year_built", "sale_date", "sale_price", "zip5", "city", "county", "state", "source_url"]
with open("Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["PID"],
                    "physical_address": " ".join(str(row["PropertyAddress"]).upper().split()),
                    "sale_date": str(parser.parse(row["LastSaleDate"])),
                    "sale_price": row["LastSalePrice"],
                    "city": " ".join(str(row["PropertyCity"]).upper().split()),
                    "zip5": row["PropertyZip"],
                    "county": "SCOTT",
                    "state": "MN",
                    "source_url": "https://opendata.gis.co.scott.mn.us/datasets/ScottCounty::parcels",
                }

                # If address is in separate fields
                property_type = [str(row["Classification"]).strip(), str(row["ModelDesc"]).strip(), str(row["ArchitectureDesc"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["property_type"] = ' '.join(filter(None, property_type)).upper()

                # Delete if no year_built
                try:
                    if int(row["YearBuilt"]) != 0 and int(row["YearBuilt"]) <= 2022:
                        land_info["year_built"] = row["YearBuilt"]

                except ValueError:
                    pass

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
