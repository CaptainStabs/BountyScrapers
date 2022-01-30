import csv
from tqdm import tqdm
from dateutil import parser
# ,,,,,,,,mdeedVolum,
#﻿PIN,mdeedPage,DeededOwne,SaleDate,SaleAmount,
columns = ["property_id", "physical_address", "book", "page", "buyer_name", "seller_name", "sale_date", "sale_price", "county", "state", "source_url"]
with open("Parcels.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["\ufeffPIN"].strip(),
                    "seller_name": " ".join(str(row["DeededOwne"]).split()),
                    "buyer_name": "",
                    "sale_date": str(parser.parse(row["SaleDate"])),
                    "sale_price": row["SaleAmount"],
                    "county": "LAKE",
                    "state": "OH",
                    "source_url": "https://www.lakecountyohio.gov/gis/"
                }

                # If address is in separate fields
                street_list = [str(row["mlocStrDir"]).strip(), str(row["mlocStrNo"]).strip(), str(row["mlocStrNo2"]).strip(), str(row["mlocStrNam"]).strip(), str(row["mlocStrSuf"]).strip(), str(row["mlocStrS_1"]).strip(), str(row["msecondary"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                # Delete if no book
                # Update field
                book = str(row["mdeedVolum"]).strip()
                page = str(row["mdeedPage"]).strip()

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
