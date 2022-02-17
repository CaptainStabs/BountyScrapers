import csv
from tqdm import tqdm

columns = ["state", "zip5", "physical_address", "city", "county", "property_id", "sale_date", "property_type", "sale_price", "seller_name", "buyer_name", "num_units", "year_built", "source_url", "book", "page", "sale_type"]

with open("C:\\Users\\adria\\Downloads\\added_counties.csv", "r") as input_csv:
    line_count = 3489716 #len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("C:\\Users\\adria\\Downloads\\cleaned_added_counties.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            land_info = {
                "state": row["state"],
                "zip5": row["zip5"],
                "physical_address": row["physical_address"], # Don't fix bad addresses
                "city": " ".join(str(row["city"]).upper().split()).strip(),
                "property_id": row["property_id"].strip(),
                "sale_date": row["sale_date"],
                "property_type": " ".join(str(row["property_type"]).upper().split()),
                "sale_price": row["sale_price"],
                "seller_name": " ".join(str(row["seller_name"]).split()).strip().strip(),
                "buyer_name": " ".join(str(row["buyer_name"]).split()).strip().strip(),
                "num_units": row["num_units"],
                "year_built": row["year_built"],
                "source_url": row["source_url"].strip(),
                "book": row["book"],
                "page": row["page"],
                "sale_type": row["sale_type"].strip(),
            }

            if not land_info["book"] or not land_info["page"]:
                land_info["book"] = ""
                land_info["page"] = ""

            elif not land_info["book"] and land_info["page"]:
                land_info["book"] = ""
                land_info["page"] = ""

            elif land_info["book"] and not land_info["page"]:
                land_info["book"] = ""
                land_info["page"] = ""


            writer.writerow(land_info)
