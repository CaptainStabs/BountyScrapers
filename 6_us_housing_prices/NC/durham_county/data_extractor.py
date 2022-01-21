import csv
from tqdm import tqdm
from dateutil import parser

# ,DEED_BOOK,DEED_PAGE,
columns = ["property_id", "property_type", "book", "page", "sale_date", "sale_price", "physical_address", "county", "state", "source_url"]
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
                    "property_id": row["PIN"],
                    "property_type": row["LANDUSE_DESC"].strip(),
                    "sale_date": str(parser.parse(row["DATE_SOLD"])),
                    "sale_price": row["SALE_PRICE"],
                    "physical_address": " ".join(str(row["SITE_ADDRE"]).upper().strip().split()),
                    "county": "Durham",
                    "state": "NC",
                    "source_url": "https://live-durhamnc.opendata.arcgis.com/datasets/DurhamNC::parcels-1/about"
                }

                book = row["DEED_BOOK"]
                page = row["DEED_PAGE"]

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = book
                        land_info["page"] = page

                except ValueError:
                    continue

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                continue
