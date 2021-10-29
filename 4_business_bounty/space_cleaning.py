import csv
from tqdm import tqdm
import os
import pandas as pd


column_name = "street_physical" # city_registered or city_physical
filename = f"F:\\us-businesses\\{column_name}.csv"
output_filename = f"F:\\us-businesses\\us-businesses\\{column_name}_cleaned.csv"

columns = ["name", "business_type", "state_registered", column_name]
#
with open(filename, "r",  encoding="utf-8") as f:
    lines = f.readlines()
    total = 0
    for line in tqdm(lines):
        total += 1
    fieldnames = ["name",	"business_type",	"state_registered", column_name]
    f.seek(0)
    with open(output_filename, "a", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)
        reader = csv.DictReader(f, fieldnames=fieldnames)
        if os.stat(output_filename).st_size == 0:
            writer.writeheader()

        for row in tqdm(reader, total=total):
            old_street = row[column_name]
            street = " ".join(str(old_street).split())
            # print(street)
            # print(f"\n{old_city_registered} -> {city_registered}")
            data = {
                "name": row["name"],
                "business_type": row["business_type"],
                "state_registered": row["state_registered"],
                column_name: str(street).strip(),
            }

            writer.writerow(data)
