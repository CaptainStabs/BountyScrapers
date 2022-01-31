import csv
from tqdm import tqdm

columns = ["state", "property_id", "physical_address", "property_type", "num_units", "sale_price", "sale_date", "book", "page", "county", "city", "zip5", "source_url", "year_built"]

def date_cleaner(date):
    date = date.split("T")
    year = date[0]
    time = date[1].split("-")[0]
    date = year + " " + time
    return date

with open("property.csv", "r") as f:
    line_count = 0
    # Count lines in file
    for line in f.readlines():
        line_count += 1

    # Seek back to 0 to allow csv to read full file
    f.seek(0)

    reader = csv.DictReader(f, delimiter=";")

    with open("extracted_data.csv", "a", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            land_info = {
                "state": "NC",
                "property_id": row["Realid"],
                "physical_address": " ".join(row["Location"].upper().strip().split()),
                "property_type": " ".join(row["LandClass"].upper().strip().split()),
                "book": row["DeedBook"],
                "page": row["DeedPage"],
                "county": row["County"],
                "city": row["PhyCity"],
                "zip5": row["PhyZip"],
                "source_url": row["Real Estate Info"],
                "year_built": row["Year Built"]
            }

            #DeedBook;DeedPage;County;PhyCity;PhyZip;Real Estate Info;Deed Info;Year Built
            if row["TotalUnits"]:
                land_info["num_units"] = row["TotalUnits"]

            if row["LandSaleDate"] and row["TotalSaleDate"]:
                land_info["sale_date"] = date_cleaner(row["TotalSaleDate"])
                land_info["sale_price"] = str(row["TotalSaleValue"]).replace(",", "")

            elif row["LandSaleDate"] and not row["TotalSaleDate"]:
                land_info['sale_date'] = date_cleaner(row["LandSaleDate"])
                land_info["sale_price"] = str(row["LandSaleValue"]).replace(",", "")

            elif row["TotalSaleDate"] and not row["LandSaleDate"]:
                land_info['sale_date'] = date_cleaner(row["TotalSaleDate"])
                land_info["sale_price"] = str(row["TotalSaleValue"]).replace(",", "")


            writer.writerow(land_info)
