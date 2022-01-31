import csv
from tqdm import tqdm
from dateutil import parser
# import json
# import heartrate; heartrate.trace(browser=True, daemon=True)

# PARCELNB,,PHYSADDRESS,PHYSCITY,PHYSZIP,,SALEDATE,SALEPRICE,
columns = ["property_id", "physical_address", "city", "zip5", "sale_date", "sale_price", "county", "state", "source_url"]
with open("Parcels.csv", "r") as input_csv:
    # line_count = len([line for line in input_csv.readlines()])
    # input_csv.seek(0)
    line_count = 53275
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["PARCELNB"].strip(),
                    "physical_address": " ".join(str(row["PHYSADDRESS"]).upper().split()),
                    "city": " ".join(str(row["PHYSCITY"]).upper().split()),
                    "zip5": str(row["PHYSZIP"]).strip(),
                    "sale_date": str(parser.parse(row["SALEDATE"].strip())).replace("+00:00", ""),
                    "sale_price": str(row["SALEPRICE"]).strip(),
                    "county": "GARFIELD",
                    "state": "CO",
                    "source_url": "https://data-garfieldcolorado.opendata.arcgis.com/datasets/garfieldcolorado::garfield-county-parcels/"

                }


                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                # print(json.dumps(row, indent=2))
                pass
