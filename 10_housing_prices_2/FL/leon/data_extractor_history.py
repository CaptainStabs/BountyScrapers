import csv
from tqdm import tqdm
from dateutil import parser

# PARID,LOCATION,ZIP,NUMBER_OF_BLDGS,YRBLT,PROPERTY_USE_DESC,SALE_DATE,SALE_PRICE,BOOK,PAGE,GRANTOR,GRANTEE
columns = ["property_id", "property_street_address", "property_zip5", "building_year_built", "property_type", "sale_datetime", "sale_price", "book", "page", "seller_name", "buyer_name", "building_num_units", "sale_type", "property_county", "state", "source_url"]
with open("./historical/Combined.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data_history.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": str(row["PARID"]).replace('="', "").strip('"'),
                    "property_street_address": " ".join(str(row["LOCATION"]).upper().split()),
                    "property_zip5": row["ZIP"],
                    "property_type": " ".join(str(row["PROPERTY_USE_DESC"]).upper().replace('"', "").split()),
                    "sale_datetime": str(parser.parse(str(row["SALE_DATE"]).strip())),
                    "sale_price": str(row["SALE_PRICE"]).strip(),
                    "seller_name": " ".join(str(row["GRANTOR"]).upper().replace('"', "'").split()),
                    "buyer_name": " ".join(str(row["GRANTEE"]).upper().replace('"', "'").split()),
                    "sale_type": str(row["INSTRUMENT_DESC"]).upper().strip(),
                    "property_county": "LEON",
                    "state": "FL",
                    "source_url": "ftp://ftp.leonpa.org/SalesHistory.csv"
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
                        land_info["building_year_built"] = row["YRBLT"]

                except ValueError:
                    pass


                # Delete if no zip5
                if land_info["property_zip5"] == "00000" or land_info["property_zip5"] == "0" or len(land_info["property_zip5"]) != 5:
                    land_info["property_zip5"] = ""

                try:
                    # Delete if no unit count
                    if int(row["NUMBER_OF_BLDGS"]) != 0:
                        land_info["building_num_units"] = row["NUMBER_OF_BLDGS"]
                except ValueError:
                    pass


                year = land_info["sale_datetime"].split("-")[0]

                if land_info["property_street_address"] and land_info["sale_datetime"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
