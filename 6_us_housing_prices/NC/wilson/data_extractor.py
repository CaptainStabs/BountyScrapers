import csv
from tqdm import tqdm
from dateutil import parser

# PIN,,DeedBook,DeedPage,,SalesAmount,,YearActuallyBuilt1Imp,,,Description1,,PhysicalStreetAddress,CityCodeDesc,,GrantorName1,GrantorName2,,,SaleDate, MultipleImprovements,
columns = ["property_id", "book", "page", "sale_price", "year_built", "property_type", "physical_address", "city", "seller_name", "sale_date", "num_units", "county", "state", "source_url"]
with open("Tax_Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": str(row["PIN"]).strip().replace(".000", ""),
                    "sale_price":str(row["SalesAmount"]).strip(),
                    "property_type": str(row["Description1"]).strip(),
                    "physical_address": " ".join(str(row["PhysicalStreetAddress"]).upper().split()),
                    "city": str(row["CityCodeDesc"]).strip(),
                    "seller_name": ", ".join([" ".join(row[f"GrantorName{i}"].split()) for i in range(1,3) if row[f"GrantorName{i}"]]),
                    # "seller_name": " ".join(" ".join([row[f"GrantorName{i}"] for i in range(1,3) if row[f"GrantorName{i}"]]).split()),
                    "sale_date": str(parser.parse(str(row["SaleDate"]).strip())).replace("+00:00", ""),
                    "county": "Wilson",
                    "state": "NC",
                    "source_url": "https://county-data-wilsoncounty.opendata.arcgis.com/datasets/tax-parcels"
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

                # Delete if no year_built
                try:
                    if int(row["YearActuallyBuilt1Imp"]) != 0 and int(row["YearActuallyBuilt1Imp"]) <= 2022:
                        land_info["year_built"] = row["YearActuallyBuilt1Imp"]

                except ValueError:
                    pass

                try:
                    # Delete if no unit count
                    if int(row["MultipleImprovements"]) != 0:
                        land_info["num_units"] = row["MultipleImprovements"]
                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
