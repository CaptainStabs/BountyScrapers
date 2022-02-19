import csv
from tqdm import tqdm
from dateutil import parser

# PIN,,Site_Address,,Property_Description,Township, Sale_Price,Sale_Date,,DeedBook,DeedPage,,
columns = ["property_id", "physical_address", "property_type", "city", "sale_price", "sale_date", "book", "page", "county", "state", "source_url"]
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
                    "physical_address": " ".join(str(row["Site_Address"]).upper().split()),
                    "property_type": " ".join(str(row["Property_Description"]).upper().split()),
                    "city": " ".join(str(row["Township"]).upper().split()),
                    "sale_price": row["Sale_Price"],
                    "sale_date": str(parser.parse(row["Sale_Date"])),
                    "county": "PERSON",
                    "state": "NC",
                    "source_url": "https://gis.personcountync.gov/arcgis/rest/services/Tax/BitekParcelInfo/MapServer/1",
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

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
