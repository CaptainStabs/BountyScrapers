# property_id,physical_address,sale_date,sale_price,property_type,book,page,zip5,state,county,city,source_url,seller_name
import csv
from tqdm import tqdm

columns = ["property_id", "physical_address", "sale_date", "sale_price", "property_type", "book", "page", "zip5", "state", "county", "city", "source_url", "seller_name"]
with open("extracted_data.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("cleaned_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in reader:
            land_info = {
                "property_id": row["property_id"].strip(),
                "physical_address": row["physical_address"].strip(),
                "sale_date": str(row["sale_date"]).strip(),
                "sale_price": row["LAST_SALE_PRICE"].strip(),
                "property_type": row["property_type"].strip(),
                "book": row["book"],
                "page": row["page"],
                "zip5": str(row["zip5"]).strip(),
                "county": row["county"].upper(),
                "state": row["state"],
                "source_url": row["source_url"],
                "seller_name": row["seller_name"]
            }

            writer.writerow(land_info)
