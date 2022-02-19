import csv
from tqdm import tqdm
from dateutil import parser

# PARCEL_ID,BK,PG,PROPLOCAT,,LANDTYPE,YRBUILT1,SALEPRICE,SALETYPE,SALEDATE,ORTHO
columns = ["property_id", "book", "page", "physical_address", "year_built", "sale_price", "sale_date", "state", "county", "source_url"]

with open("Parcels2021Download.csv", "r") as input_csv:
    line_count = 0
    # Count lines in file
    for line in input_csv.readlines():
        line_count += 1

    # Seek back to 0 to allow csv to read full file
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            land_info = {
                "property_id": row["PARCEL_ID"],
                "book": row["BK"],
                "page": row["PG"],
                "physical_address": " ".join(str(row["PROPLOCAT"]).upper().strip().split()),
                "year_built": row["YRBUILT1"],
                "sale_price": row["SALEPRICE"],
                "sale_date": parser.parse(str(row["SALEDATE"]).replace("+00", "")),
                "state": "NC",
                "county": "WILKES",
                "source_url": "https://data3-wilkescountygis.opendata.arcgis.com/datasets/wilkescountygis::parcels2021download/about"
            }

            if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"]:
                writer.writerow(land_info)
