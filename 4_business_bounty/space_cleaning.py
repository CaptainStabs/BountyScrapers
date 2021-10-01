import csv
from tqdm import tqdm
import os
import pandas as pd

columns = ["name", "business_type", "state_registered", "street_physical"]

filename = "E:\\us-businesses\\fix_commas.csv"
output_filename = "E:\\us-businesses\\cleaned_spaces.csv"
column_name = "street_physical" # city_registered or city_physical
#
with open(filename, "r",  encoding="utf-8") as f:
    lines = f.readlines()
    total = 0
    for line in tqdm(lines):
        total += 1
fieldnames = ["name",	"business_type",	"state_registered",	"street_registered",	"city_registered",	"zip5_registered",	"state_physical",	"street_physical",	"city_physical",	"zip5_physical",	"filing_number",	"public",	"naics_2017",	"ein",	"sic4",	"parent",	"website", "duns"]
with open(filename, "r",  encoding="utf-8") as f:
    with open(output_filename, "a", encoding="utf-8") as output_file:
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
