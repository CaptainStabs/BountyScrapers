import csv
from tqdm import tqdm
from dateutil import parser

# PARCEL_ID,LOCATION,,YRBLT,PROPERTY USE,SALE_DATE,SALE_PRICE,BOOK,PAGE,,GRANTOR,GRANTEE
columns = ["property_id", "physical_address", "year_built", "property_type", "sale_date", "sale_price", "book", "page", "seller_name", "buyer_name", "county", "state", "source_url"]
with open("SalesData_2020.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": str(row["PARCEL_ID"]).replace('="', "").strip('"'),
                    "physical_address": " ".join(str(row["LOCATION"]).upper().split()),
                    "property_type": " ".join(str(row["PROPERTY_USE"]).upper().split()),
                    "sale_date": str(parser.parse(str(row["SALE_DATE"]).strip())),
                    "sale_price": str(row["SALE_PRICE"]).strip(),
                    "seller_name": " ".join(str(row["GRANTOR"]).upper().split()),
                    "buyer_name": " ".join(str(row["GRANTEE"]).upper().split()),
                    "county": "LEON",
                    "state": "FL",
                    "source_url": "ftp://ftp.leonpa.org/SalesData_2020.csv"
                }

                # Delete if no book
                # Update field
                book = str(row["BOOK"]).strip()
                page = str(row["PAGE"]).strip()

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = int(book)
                        land_info["page"] = int(page)

                except ValueError:
                    pass

                # Delete if no year_built
                try:
                    if int(row["YRBLT"]) != 0 and int(row["YRBLT"]) <= 2022:
                        land_info["year_built"] = row["YRBLT"]

                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
