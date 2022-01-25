import csv
from tqdm import tqdm
from dateutil import parser

#pin83,,phys_zip,prop_addre,cur_deed_b,cur_deed_p,sale_date,sale_price,PRC
columns = ["property_id", "physical_address", "book", "page", "sale_date", "sale_price", "county", "state", "source_url", "zip5"]
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
                    "property_id": row["pin83"],
                    "physical_address": " ".join(str(row["prop_addre"]).upper().strip().split()),
                    "sale_date": str(parser.parse(row["sale_date"])),
                    "sale_price": str(row["sale_price"]).split(".")[0],
                    "county": "Jones",
                    "state": "NC",
                    "source_url": str(row["PRC"]).strip(),
                    "zip5": row["phys_zip"]
                }

                # Delete if no book
                # Update field
                book = row["cur_deed_b"]
                page = row["cur_deed_p"]

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = book
                        land_info["page"] = page

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
