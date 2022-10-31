import csv
from tqdm import tqdm
from dateutil import parser

# PARCEL_ID,LOCATION,,YRBLT,PROPERTY USE,SALE_DATE,SALE_PRICE,BOOK,PAGE,,GRANTOR,GRANTEE
columns = ["property_id", "property_street_address", "building_year_built", "property_type", "sale_datetime", "sale_price", "book", "page", "seller_name", "buyer_name", "sale_type", "property_county", "state", "source_url", "total_assessed_value", "building_area_sqft"]
with open("SalesData_2020.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data_2020.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": str(row["PARCEL_ID"]).replace('="', "").strip('"'),
                    "property_street_address": " ".join(str(row["LOCATION"]).upper().split()),
                    "property_type": " ".join(str(row["PROPERTY_USE"]).upper().split()),
                    "sale_datetime": str(parser.parse(str(row["SALE_DATE"]).strip())),
                    "sale_price": str(row["SALE_PRICE"]).strip(),
                    "seller_name": " ".join(str(row["GRANTOR"]).upper().split()),
                    "buyer_name": " ".join(str(row["GRANTEE"]).upper().split()),
                    "sale_type": str(row["INSTRUMENT_DESC"]).upper().strip(),
                    "property_county": "LEON",
                    "state": "FL",
                    "total_assessed_value": row["ASSESSED_VALUE"],
                    "source_url": "ftp://ftp.leonpa.org/SalesData_2020.csv"
                }

                base = int(row["BASE_SQ_FT"]) if row["BASE_SQ_FT"] else 0
                aux = int(row["AUX_SQ_FT"]) if row["AUX_SQ_FT"] else 0
                sq_ft = aux + base
                if sq_ft:
                    land_info["building_area_sqft"] = sq_ft
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
                        land_info["building_year_built"] = row["YRBLT"]

                except ValueError:
                    pass

                year = land_info["sale_datetime"].split("-")[0]

                if land_info["property_street_address"] and land_info["sale_datetime"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
