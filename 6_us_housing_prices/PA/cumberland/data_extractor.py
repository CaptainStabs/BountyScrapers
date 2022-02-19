import csv
from tqdm import tqdm
from dateutil import parser

# ,PIN,,SITUS,DB_PG,DEED_VERFY,SALEPRICE,SALEDATE,YEAR_BLT,
columns = ["property_id", "physical_address", "book", "page", "sale_type", "sale_price", "sale_date", "year_built", "county", "state", "source_url"]
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
                    "physical_address": " ".join(str(row["SITUS"]).upper().split()),
                    "sale_price": row["SALEPRICE"].split(".")[0],
                    "sale_date": str(parser.parse(row["SALEDATE"])),
                    "county": "CUMBERLAND",
                    "state": "PA",
                    "source_url": "https://www.pasda.psu.edu/uci/DataSummary.aspx?dataset=2026",
                }

                if row["DEED_VERFY"] == "Y":
                    land_info["sale_type"] = "VERIFIED DEED"
                elif row["DEED_VERFY"] == "N":
                    land_info["sale_type"] = "UNVERIFIED DEED"
                elif row["DEED_VERFY"] != "`" and row["DEED_VERFY"] != "0":
                    land_info["sale_type"] = row["DEED_VERFY"]

                book_page = row["DB_PG"].split("-")
                try:
                    # Delete if no book
                    # Update field
                    book = str(book_page[0]).strip()
                    page = str(book_page[1]).strip()

                    try:
                        if int(book) != 0 and int(page) != 0:
                            land_info["book"] = int(book)
                            land_info["page"] = int(page)

                    except ValueError:
                        pass
                except IndexError:
                    pass
                # Delete if no year_built
                try:
                    if int(row["YEAR_BLT"]) != 0 and int(row["YEAR_BLT"]) <= 2022:
                        land_info["year_built"] = row["YEAR_BLT"]

                except ValueError:
                    pass


                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
