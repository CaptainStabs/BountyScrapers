import yaml
import csv
from tqdm import tqdm


columns = ["state", "zip5", "physical_address", "city", "county", "property_id", "sale_date", "property_type", "sale_price", "seller_name", "buyer_name", "num_units", "year_built", "source_url", "book", "page", "sale_type"]
with open("geo-data.yaml", "r") as f:
    zip_cty_cnty = yaml.safe_load(f)

with open("F:\\us-housing-prices-2\\null_counties.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("F:\\us-housing-prices-2\\added_counties.csv", "a") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        
        for row in tqdm(reader, total=line_count):
            if row["zip5"] and row["city"]:
                try:
                    county = zip_cty_cnty["zip5"]["county"]
                    land_info = {
                        "state": row["state"],
                        "zip5": row["zip5"],
                        "physical_address": row["physical_address"],
                        "city": row["city"],
                        "county": str(county).upper().strip(),
                        "property_id": row["property_id"],
                        "sale_date": row["sale_date"],
                        "sale_price": row["sale_price"],
                        "seller_name": row["seller_name"],
                        "buyer_name": row["buyer_name"],
                        "num_units": row["num_units"],
                        "year_built": row["year_built"],
                        "source_url": row["source_url"],
                        "book": row["book"],
                        "page": row["page"],
                        "sale_type": row["sale_type"]
                    }

                except KeyError:
                    pass
            elif row["zip5"] and not row["city"]:
                county = zip_cty_cnty["zip5"]["county"]
                city = zip_cty_cnty["zip5"]["city"]
                land_info = {
                    "state": row["state"],
                    "zip5": row["zip5"],
                    "physical_address": row["physical_address"],
                    "city": str(city).upper().strip(),
                    "county": str(county).upper().strip(),
                    "property_id": row["property_id"],
                    "sale_date": row["sale_date"],
                    "sale_price": row["sale_price"],
                    "seller_name": row["seller_name"],
                    "buyer_name": row["buyer_name"],
                    "num_units": row["num_units"],
                    "year_built": row["year_built"],
                    "source_url": row["source_url"],
                    "book": row["book"],
                    "page": row["page"],
                    "sale_type": row["sale_type"]
                }

                try:
                    writer.writerow(land_info)

                except Exception as e:
                    print("E")
