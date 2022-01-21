import csv
from dateutil import parser
import re

# ,DEED_DATE,DEED_BOOK,DEED_PAGE,PKG_SALE_D,PKG_SALE_P,LAND_SALE_,LAND_SALE1,
columns = ["property_id", "physical_address", "city", "county", "state", "zip5", "sale_date", "sale_price", "book", "page", "property_type", "source_url"]

with open("PARCEL.csv", "r", encoding="utf-8") as input_csv:
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in reader:
            land_info = {
                "property_id": row["PIN"],
                "physical_address": " ".join(str(row["LOCATION_A"]).upper.strip().split()),
                "city": " ".join(row["PHYADDR_CI"].upper().split()),
                "county": "Burken",
                "state": "NC",
                "zip5": re.match('[0-9]{5}', row["PHYADDR_CI"]),
            }

            # If neither pkg_sale_date nor land_sale, try deed_date

            if not row["PKG_SALE_D"] and not row["LAND_SALE_"] and row["DEED_DATE"]:
                land_info["sale_date"] = parser.parse(row["DEED_DATE"])

            if row["LAND_SALE_"] and not row["PKG_SALE_D"]:
                land_info["sale_date"] = parser.parse(row["LAND_SALE_"])
                land_info["sale_price"] = row["LAND_SALE1"]

            elif not row["LAND_SALE_"] and row["PKG_SALE_D"]:
                land_info["sale_date"] = parser.parse(row["PKG_SALE_D"])
                land_info["sale_price"] = row["PKG_SALE_P"]
