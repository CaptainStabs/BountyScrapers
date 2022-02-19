import csv
from tqdm import tqdm
from dateutil import parser
from pathlib import Path
import sys

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))

from _sale_type.sale_type import sale_type


# ,LU_Desc,Prop_ID,,Situs_Addr,Situs_City,Situs_Zip,Sale_Deed,Sale_Price,Sale_Date,
columns = ["property_type", "property_id", "physical_address", "city", "zip5", "sale_type", "sale_price", "sale_date", "county", "state", "source_url"]
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
                    "property_type": " ".join(str(row["LU_Desc"]).upper().split()).strip(),
                    "property_id": row["Prop_ID"].strip(),
                    "physical_address": " ".join(str(row["Situs_Addr"]).upper().split()).strip(),
                    "city": " ".join(str(row["Situs_City"]).upper().split()).strip(),
                    "zip5": row["Situs_Zip"][:5],
                    "sale_price": row["Sale_Price"],
                    "sale_date": str(parser.parse(row["Sale_Date"].strip())),
                    "county": "JEFFERSON",
                    "state": "WA",
                    "source_url": "https://gisdata-jeffcowa.opendata.arcgis.com/datasets/public-parcels/",
                }

                try:
                    land_info["sale_type"] = sale_type[row["Sale_Deed"].upper().replace("_", "").strip()]
                except KeyError:
                    land_info["sale_type"] = row["Sale_Deed"].upper().strip()

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""


                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
