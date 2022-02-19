import csv
from dateutil import parser
from tqdm import tqdm

columns = ["property_id", "sale_date", "sale_price", "book", "page", "physical_address", "sale_type", "city", "state", "zip5", "source_url"]
with open("extracted_data.csv", "r") as input_csv:
    line_count = 0
    # Count lines in file
    for line in input_csv.readlines():
        line_count += 1

    # Seek back to 0 to allow csv to read full file
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("cleaned_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            land_info = {
                "property_id": row["property_id"],
                "sale_date": parser.parse(row["sale_date"]),
                "sale_price": row["sale_price"],
                "book": row["book"],
                "page": row["page"],
                "physical_address": row["physical_address"],
                "sale_type": " ".join(row["sale_type"].strip('][').split(', ')),
                "city": row["city"],
                "state": row["state"],
                "zip5": row["zip5"],
                "source_url": "https://data-fairfaxcountygis.opendata.arcgis.com/datasets/Fairfaxcountygis::tax-administrations-real-estate-sales-data/about"
            }

            writer.writerow(land_info)
