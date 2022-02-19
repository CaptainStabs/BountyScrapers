import csv
from tqdm import tqdm

def validate_year():
    with open("C:\\Users\\adria\\Downloads\\added_counties.csv", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()])
        input_csv.seek(0)
        reader = csv.DictReader(input_csv)


        with open("fixed_dates.csv", "a") as output_csv:
            writer = csv.DictWriter(output_csv, fieldnames=reader.fieldnames)
            writer.writeheader()

            for row in tqdm(reader, total=line_count):
                if "https://data-sagis.opendata.arcgis.com/datasets" not in row["source_url"]:
                    land_info = {
                        "state": row["state"],
                        "zip5": row["zip5"],
                        "physical_address": row["physical_address"],
                        "city": " ".join(str(row["city"]).split()).strip(),
                        "county": " ".join(str(row["county"]).split()).strip(),
                        "property_id": row["property_id"].strip(),
                        "sale_date": row["sale_date"],
                        "property_type": row["property_type"].strip(),
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

                    year = int(land_info["sale_date"].split("-")[0])

                    if year >= 1690 and year <= 2022:
                        writer.writerow(row)

validate_year()
