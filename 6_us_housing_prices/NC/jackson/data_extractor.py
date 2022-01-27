import csv
from tqdm import tqdm
from dateutil import parser

#PIN,PropAddr,SaleDate_UTC,SalePrice,Prc_Url,
columns = ["property_id", "physical_address", "sale_date", "sale_price", "county", "state", "source_url"]
with open("Jackson_County_Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["PIN"],
                    "physical_address": " ".join(str(row["PropAddr"]).upper().strip().split()),
                    "sale_date": str(parser.parse(str(row["SaleDate_UTC"]).replace("+00", ""))),
                    "county": "Jackson",
                    "state": "NC",
                    "source_url": row["Prc_Url"]
                }

                if row["SalePrice"] == "":
                    land_info["sale_price"] = 0

                else:
                    land_info["sale_price"] = row["SalePrice"]

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
