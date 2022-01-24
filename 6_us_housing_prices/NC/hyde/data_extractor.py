import csv
from tqdm import tqdm
from dateutil import parser

#PIN,SITUSADDR,SITUSROAD,DEEDBOOK,DEEDPAGE,GRANTOR,SaleDate,SaleAmount
columns = ["property_id", "physical_address", "book", "page", "seller_name", "sale_date", "sale_price", "county", "state", "source_url"]
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
                    "seller_name": " ".join(str(row["GRANTOR"]).strip().split()),
                    "county": "Hyde",
                    "state": "NC",
                    "source_url": "https://dl.agd.cc/hyde/"
                }

                # If address is in separate fields
                street_list = [str(row["SITUSADDR"]).strip(), str(row["SITUSROAD"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                # Delete if no book
                # Update field
                book = row["DEEDBOOK"]
                page = row["DEEDPAGE"]

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = book
                        land_info["page"] = page

                except ValueError:
                    pass

                if row["SaleDate"] != "NULL":
                    land_info["sale_date"] = str(parser.parse(str(row["SaleDate"])))

                if row["SaleAmount"] != "NULL":
                    land_info["sale_price"] = row["SaleAmount"]

                try:
                    if land_info["sale_date"]:
                        year = land_info["sale_date"].split("-")[0]

                        if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                            writer.writerow(land_info)
                except KeyError:
                    pass

            except parser._parser.ParserError:
                pass
