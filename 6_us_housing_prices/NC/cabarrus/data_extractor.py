import csv
from tqdm import tqdm
from dateutil import parser
# InstrumentType
# PIN14, SaleYear, SaleMonth, SalePrice, DeedBook, DeedPage, ,con_cat, City, State, Zip,
columns = ["property_id", "sale_date", "sale_price", "book", "page", "physical_address", "city", "zip5", "county", "state", "source_url"]
with open("Parcels.csv", "r") as input_csv:
    # line_count = len([line for line in input_csv.readlines()])
    # input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=163561):
            try:
                land_info = {
                    "property_id": row["PIN14"],
                    "sale_date": str(parser.parse(str(row["SaleMonth"] + "/01/" + row["SaleYear"]))),
                    "sale_price": row["SalePrice"],
                    "physical_address": " ".join(str(row["con_cat"]).upper().split()),
                    "city": " ".join(str(row["City"]).upper().split()),
                    "zip5": row["Zip"],
                    "county": "CABARRUS",
                    "state": "NC",
                    "source_url": "https://location.cabarruscounty.us/arcgishost/rest/services/Website/MapCabarrusPropertyData/MapServer/0/",
                }

                # Delete if no book
                # Update field
                book = str(row["DeedBook"]).strip()
                page = str(row["DeedPage"]).strip()

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = int(book)
                        land_info["page"] = int(page)

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
