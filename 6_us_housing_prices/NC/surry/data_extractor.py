import csv
from tqdm import tqdm
from dateutil import parser

#HouseNumber,StreetDirection,StreetName,StreetType,StreetSuffix,,DeedBook,DeedPage,PARCEL_ID,SaleMonth,SaleYear,SalePrice,Township,
columns = ["physical_address", "book", "page", "property_id", "sale_date", "sale_price", "city", "county", "state", "source_url"]
with open("surry.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["PARCEL_ID"],
                    "sale_date": str(parser.parse(str(row["SaleMonth"]) + "/01/" + str(row["SaleYear"]))),
                    "sale_price": row["SalePrice"],
                    "city": " ".join(str(row["Township"]).upper().split()),
                    "county": "Surry",
                    "state": "NC",
                    "source_url": "https://www.co.surry.nc.us/departments/(k_through_z)/tax/downloadable_data.php"
                }

                # If address is in separate fields
                street_list = [str(row["HouseNumber"]).strip(), str(row["StreetDirection"]).strip(), str(row["StreetName"]).strip(), str(row["StreetType"]).strip(), str(row["StreetSuffix"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

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

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
