import csv
from tqdm import tqdm
from dateutil import parser
from pathlib import Path
import sys

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))

from _sale_type.sale_type import sale_type

#DEEDBOOK,DEEDPAGE,DEEDYEAR,SALE_AMT,TOWNSHIP,PROP_ADDRESS,,DATESOLD,PIN,BALDUE
columns = ["book", "page", "sale_price", "city", "physical_address", "sale_date", "property_id", "sale_type", "county", "state", "source_url"]
with open("Tax_Parcels.csv", "r", newline="", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "sale_price": row["SALE_AMT"],
                    "sale_date": str(parser.parse(str(row["DATESOLD"]).replace("+00", "").strip())),
                    "city": " ".join(str(row["CITY"]).upper().split()),
                    "physical_address": " ".join(str(row["PROP_ADDRESS"]).upper().split()),
                    "property_id": row["PIN"],
                    "county": "Rowan",
                    "state": "NC",
                    "source_url": "https://gisdata-rowancountync.opendata.arcgis.com/datasets/RowanCountyNC::tax-parcels-"
                }

                try:
                    land_info["sale_type"] = sale_type[row["SALEINST"].upper().replace("_", "").strip()]

                except KeyError:
                    land_info["sale_type"] = str(row["SALEINST"]).upper().strip()


                book = str(row["DEEDBOOK"]).strip()
                page = str(row["DEEDPAGE"]).strip()

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = int(book)
                        land_info["page"] = int(page)

                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError as e:
                print(e)
                pass
