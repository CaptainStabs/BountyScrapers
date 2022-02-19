import csv
from tqdm import tqdm
from dateutil import parser

# "mapblolot","saledate1","saleprice","deedbook","deedpage","validitycode",,"PropStreet","City","Zip","YearBuilt","UseCode","HouseStyle"
columns = ["property_id", "sale_date", "sale_price", "book", "page", "sale_type", "physical_address", "city", "zip5", "year_built", "property_type", "county", "state", "source_url"]
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
                    "property_id": row["mapblolot"],
                    "sale_date": str(parser.parse(str(row["saledate1"]))),
                    "sale_price": row["saleprice"],
                    "sale_type": " ".join(str(row["validitycode"]).upper().split()),
                    "physical_address": " ".join(str(row["PropStreet"]).upper().split()),
                    "city": " ".join(str(row["City"]).upper().split()),
                    "zip5": row["Zip"],
                    "county": "ALBEMARLE",
                    "state": "VA",
                    "source_url": "https://gisweb.albemarle.org/gisdata/CAMA/GIS_View_Redacted_VisionSales_TXT.zip",
                }

                if "STORY" in str(row["HouseStyle"]).upper():
                    land_info["property_type"] = str(row["UseCode"]).upper().strip() + " " + str(row["HouseStyle"]).upper().strip()
                else:
                    land_info["property_type"] = str(row["UseCode"]).upper().strip()

                # Delete if no book
                # Update field
                book = str(row["deedbook"]).strip()
                page = str(row["deedpage"]).strip()

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = int(book)
                        land_info["page"] = int(page)

                except ValueError:
                    pass

                # Delete if no year_built
                try:
                    if int(row["YearBuilt"]) != 0 and int(row["YearBuilt"]) <= 2022:
                        land_info["year_built"] = row["YearBuilt"]

                except ValueError:
                    pass

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] != "NULL" and land_info["sale_date"] != "NULL" and land_info["sale_price"] != "NULL" and int(year) <= 2022 and land_info["sale_date"] != "1754-01-01 00:00:00":
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
