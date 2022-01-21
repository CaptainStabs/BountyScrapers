import csv
from dateutil import parser
import re
from tqdm import tqdm

columns = ["property_id", "physical_address", "city", "county", "state", "zip5", "sale_date", "sale_price", "book", "page", "property_type", "source_url"]

with open("PARCEL.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    # Seek back to 0 to allow csv to read full file
    input_csv.seek(0)

    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["PIN"],
                    "physical_address": " ".join(str(row["LOCATION_A"]).upper().strip().split()).strip(),
                    "city": " ".join(row["PHYADDR_CI"].upper().split()).strip(),
                    "county": "Burken",
                    "state": "NC",
                    "zip5": row["PHYADDR_ZI"],
                    "source_url": "https://www.burkenc.org/2495/Data-Sets",
                    "property_type": " ".join(str(row["LAND_CLASS"]).split()).strip()
                }

                # If neither pkg_sale_date nor land_sale, try deed_date
                land_info["sale_date"] = parser.parse(row["DEED_DATE"])
                land_info["sale_price"] = row["REVENUE_ST"]

                book = row["DEED_BOOK"]
                page = row["DEED_PAGE"]

                if book != "0" and page != "0" and book is not None and page is not None:
                    land_info["book"] = book
                    land_info["page"] = page

                if land_info["zip5"] = "00000":
                    land_info["zip5"] = ""

                if land_info["physical_address"] and land_info["sale_date"]:
                    writer.writerow(land_info)
            except parser._parser.ParserError:
                continue
