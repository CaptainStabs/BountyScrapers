import csv
from tqdm import tqdm
from dateutil import parser
prop_types = {
    "C": "COMMERCIAL",
    "R": "RESIDENTIAL",
}
    # PIN_COMMON,LOC_ADDRES,,BOOK,PAGE,DEED_REC_D,CLASS,,LAST_SALE_,
columns = ["property_id", "physical_address", "book", "page", "sale_date", "property_type", "sale_price", "county", "state", "source_url"]
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
                    "property_id": row["PIN_COMMON"],
                    "physical_address": " ".join(str(row["LOC_ADDRES"]).upper().split()),
                    "sale_date": str(parser.parse(row["DEED_REC_D"])),
                    "sale_price": row["LAST_SALE_"],
                    "county": "CHESTER",
                    "state": "PA",
                    "source_url": "https://www.pasda.psu.edu/uci/DataSummary.aspx?dataset=1694",
                }

                try:
                    land_info["property_type"] = prop_types[row["CLASS"]]
                except KeyError:
                    land_info["property_type"] = row["CLASS"].strip()


                # Delete if no book
                # Update field
                book = str(row["BOOK"]).strip()
                page = str(row["PAGE"]).strip()

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
