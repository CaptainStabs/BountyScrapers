import csv
from tqdm import tqdm
from dateutil import parser

# DEED_BOOK,DEED_PAGE,,DATE_SOLD,SALES_PRICE,PHYSICAL_ADDRESS,,PARCELID,PIN,
columns = ["book", "page", "sale_date", "sale_price", "physical_address", "property_id", "county", "state", "source_url"]
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
                    "sale_date": str(parser.parse(row["DATE_SOLD"])),
                    "sale_price": row["SALES_PRICE"],
                    "physical_address": " ".join(str(row["PHYSICAL_ADDRESS"]).upper().split()),
                    "property_id": row["PARCELID"],
                    "county": "ALEXANDER",
                    "state": "NC",
                    "source_url": "https://maps.alexandercountync.gov/arcgis1/rest/services/Parcels/MapServer/0",
                }

                # Delete if no book
                # Update field
                book = str(row["DEED_BOOK"]).strip()
                page = str(row["DEED_PAGE"]).strip()

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = int(book)
                        land_info["page"] = int(page)

                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
