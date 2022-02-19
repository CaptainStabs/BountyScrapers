import csv
from tqdm import tqdm
from dateutil import parser

# NEWPIN,HouseNumbe,StreetDire,StreetName,StreetType,DeedBook,DeedPage,SaleMonth,SaleYear,,SalePrice,
columns = ["property_id", "physical_address", "book", "page", "sale_date", "sale_price", "county", "state", "source_url"]
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
                    "property_id": row["NEWPIN"],
                    "sale_date": str(parser.parse((str(row["SaleMonth"]) + "/01/" + str(row["SaleYear"])))),
                    "sale_price": row["SalePrice"],
                    "source_url": row["TaxCard"],
                    "county": "Cherokee",
                    "state": "NC"

                }

                # If address is in separate fields
                street_list = [ str(row["HouseNumbe"]).strip(), str(row["StreetDire"]).strip(), str(row["StreetName"]).strip(), str(row["StreetType"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                # Delete if no book
                # Update field
                book = row["DeedBook"]
                page = row["DeedPage"]

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = book
                        land_info["page"] = page

                except ValueError:
                    pass


                year = row["SaleYear"]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
