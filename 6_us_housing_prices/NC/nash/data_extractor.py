import csv
from tqdm import tqdm
from dateutil import parser

# TAX_PIN,PHYS_ADDR,,DEEDBOOK,DEEDPAGE,SALEDATE,,SALEPRICE,BLDG_TYPE,R_YR_BUILT,TOTALCARDS
columns = ["property_id", "physical_address", "book", "page", "sale_date", "sale_price", "property_type", "year_built", "num_units", "county", "state", "source_url"]
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
                    "property_id": row["TAX_PIN"],
                    "physical_address": " ".join(str(row["PHYS_ADDR"]).upper().strip().split()),
                    "sale_date": str(parser.parse(row["SALEDATE"])),
                    "sale_price": row["SALEPRICE"],
                    "property_type": " ".join(str(row["BLDG_TYPE"]).strip().split()),
                    "county": "Nash",
                    "state": "NC",
                    "source_url": "http://nc-nashcounty.civicplus.com/195/GIS-Downloads"
                }

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

                # Delete if no year_built
                try:
                    if int(row["R_YR_BUILT"]) != 0 and int(row["R_YR_BUILT"]) <= 2022:
                        land_info["year_built"] = row["R_YR_BUILT"]

                except ValueError:
                    pass


                try:
                    # Delete if no unit count
                    if int(row["TOTALCARDS"]) != 0:
                        land_info["num_units"] = row["TOTALCARDS"]
                except ValueError:
                    pass


                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
