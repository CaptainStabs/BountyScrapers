import csv
from tqdm import tqdm
from dateutil import parser

# PARCELKEY,MUNI,,LOCADDR,LOCZIP,BOOK,PAGE,DESCRIPTIO,,SALE_DATE,SALE_PRICE,,YR_BUILT,STORIES,
columns = ["property_id", "city", "physical_address", "zip5", "book", "page", "property_type", "sale_date", "sale_price", "year_built", "county", "state", "source_url"]
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
                    "property_id": row["PARCELKEY"],
                    "city": " ".join(str(row["MUNI"]).upper().split()),
                    "physical_address": " ".join(str(row["LOCADDR"]).upper().split()),
                    "zip5": row["LOCZIP"],
                    "sale_date": str(parser.parse(row["SALE_DATE"])),
                    "sale_price": row["SALE_PRICE"],
                    "county": "TOMPKINS",
                    "state": "NY",
                    "source_url": "https://tcdata-tompkinscounty.opendata.arcgis.com/datasets/tompkinscounty::parcels-public/about",
                }

                try:
                    if int(row["STORIES"]):
                        land_info["property_type"] = " ".join(str(row["DESCRIPTIO"]).upper().split()) + ", " + str(row["STORIES"]) + " STORIES"
                    else:
                        land_info["property_type"] = " ".join(str(row["DESCRIPTIO"]).upper().split())

                except ValueError:
                    print("A")
                    land_info["property_type"] = " ".join(str(land_info["DESCRIPTIO"]).upper().split())

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
                    if int(row["YR_BUILT"]) != 0 and int(row["YR_BUILT"]) <= 2022:
                        land_info["year_built"] = row["YR_BUILT"]

                except ValueError:
                    pass

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""


                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
