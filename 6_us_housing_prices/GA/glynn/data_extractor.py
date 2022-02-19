import csv
from tqdm import tqdm
from dateutil import parser

# "PARCEL_ID","FULL_ADDRESS","DEED_BOOK","DEED_PAGE","SALE_DATE","SALE_PRICE"
columns = ["property_id", "physical_address", "book", "page", "sale_date", "sale_price", "county", "state", "source_url"]
with open("Parcels_Extract.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["PARCEL_ID"].strip(),
                    "physical_address": " ".join(str(row["FULL_ADDRESS"]).upper().split()),
                    "sale_date": str(parser.parse(row["SALE_DATE"])),
                    "sale_price": row["SALE_PRICE"],
                    "county": "GLYNN",
                    "state": "GA",
                    "source_url": "https://glynncounty.org/DocumentCenter/View/42975"

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
