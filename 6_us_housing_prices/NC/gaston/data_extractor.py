import csv
from tqdm import tqdm
from dateutil import parser
from pathlib import Path
import sys

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))

from _sale_type.sale_type import sale_type
unknown_type = []

# PIN,DEED_BOOK,DEED_PAGE,DESC1_DESC,DIST_TWN,PHYSSTRADD,,,SALEDATE,SALESAMT,YEARBLT,
columns = ["property_id", "book", "page", "property_type", "city", "physical_address", "sale_date", "sale_price", "year_built", "sale_type", "county", "state", "source_url"]
with open("DevNetCAMA.csv", "r") as input_csv:
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
                    "property_type": " ".join(str(row["DESC1_DESC"]).upper().strip().split()),
                    "city": " ".join(str(row["DIST_TWN"]).upper().strip().split()),
                    "physical_address": " ".join(str(row["PHYSSTRADD"]).upper().strip().split()),
                    "sale_date": str(parser.parse(row["SALEDATE"])),
                    "sale_price": row["SALESAMT"].split(".")[0],
                    "county": "GASTON",
                    "state": "NC",
                    "source_url": "https://cloud.gastongov.com/owncloud/public.php?service=files&t=d546a0e44c38b7ecbbb5c25d768fa8cc",
                }

                try:
                    land_info["sale_type"] = sale_type[row["DEEDTYPE"].upper().replace("_", "").strip()]

                except KeyError:
                    land_info["sale_type"] = str(row["DEEDTYPE"]).upper().strip()

                book = row["DEED_BOOK"]
                page = row["DEED_PAGE"]

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = book
                        land_info["page"] = page

                except ValueError:
                    pass

                if int(row["YEARBLT"]) != 0 and int(row["YEARBLT"]) <= 2022:
                    land_info["year_built"] = row["YEARBLT"]

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)


            except parser._parser.ParserError:
                continue
