import csv
from tqdm import tqdm
from dateutil import parser

from pathlib import Path
import sys

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))

from _sale_type.sale_type import sale_type

#,PIN,,PhyAddress,,DeedBook,DeedPage,TransDate,SalesAmt,Impr1Desc,YearBuilt,MutipleImp
columns = ["property_id", "physical_address", "book", "page", "sale_date", "sale_price", "property_type", "year_built", "num_units", "sale_type", "county", "state", "source_url"]
with open("Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                if row["TransDate"] != "0":
                    land_info = {
                        "property_id": row["PIN"],
                        "physical_address": " ".join(str(row["PhyAddress"]).upper().strip().split()),
                        "sale_date": str(parser.parse(row["TransDate"])),
                        "sale_price": row["SalesAmt"],
                        "property_type": " ".join(str(row["Impr1Desc"]).strip().split()),
                        "county": "MONTGOMERY",
                        "state": "NC",
                        "source_url": "https://montnc.maps.arcgis.com/home/item.html?id=c4e8961b34394c61bcd253ced1480693"
                    }

                    try:
                        land_info["sale_type"] = sale_type[row["SalesInstr"].upper().replace("_", "").strip()]

                    except KeyError:
                        land_info["sale_type"] = str(row["SalesInstr"])

                    # Delete if no book
                    # Update field
                    book = row["DeedBook"]
                    page = row["DeedPage"]

                    try:
                        if int(book) != 0 and int(page) != 0:
                            land_info["book"] = book
                            land_info["page"] = page

                    except ValueError:
                        pass

                    # Delete if no year_built
                    try:
                        if int(row["YearBuilt"]) != 0 and int(row["YearBuilt"]) <= 2022:
                            land_info["year_built"] = row["YearBuilt"]

                    except ValueError:
                        pass


                    # Delete if no unit count
                    if int(row["MutipleImp"]) != 0:
                        land_info["num_units"] = row["MutipleImp"]


                    year = land_info["sale_date"].split("-")[0]

                    if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                        writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
