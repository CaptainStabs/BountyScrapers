import csv
from tqdm import tqdm
from dateutil import parser

# PIN,SITUS_ADDR,DEEDBOOK,DEEDPAGE,SALEDATE,SALE_AMT,,PRC,
columns = ["property_id", "physical_address", "book", "page", "sale_date", "sale_price", "county", "state", "source_url"]
with open("tax2.csv", "r") as input_csv:
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
                    "physical_address": " ".join(str(row["SITUS_ADDR"]).upper().split()),
                    "sale_date": str(parser.parse(row["SALEDATE"])),
                    "sale_price": row["SALE_AMT"],
                    "county": "Pamlico",
                    "state": "NC",
                    "source_url": row["PRC"]
                }

                # Delete if no book
                # Update field
                book = str(row["DEEDBOOK"]).strip()
                page = str(row["DEEDPAGE"]).strip()

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
