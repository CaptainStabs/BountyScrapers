import csv
from tqdm import tqdm
import os
import pandas as pd


filename = "F:\\us-businesses\\city_registered.csv"
output_filename = "F:\\us-businesses\\us-businesses\\city_registered_cleaned.csv"
column_name = "city_registered" # city_registered or city_physical

columns = ["name", "business_type", "state_registered", column_name]

with open(filename, "r", encoding="utf-8") as f:
    lines = f.readlines()
    total = 0
    for line in lines:
        total += 1

df = pd.read_csv(filename)
# df_columns = list(df.columns)
# data_columns = ",".join(map(str, df_columns))

with open(output_filename, "a", encoding="utf-8", newline="") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat(output_filename).st_size == 0:
        writer.writeheader()



    for index, row in tqdm(df.iterrows(), total=total):
        old_city = row[column_name]
        city = str(old_city).split(",")[0]
        # print(f"\n{old_city_registered} -> {city_registered}")
        data = {
            "name": row["name"],
            "business_type": row["business_type"],
            "state_registered": row["state_registered"],
            column_name: str(city).strip(),
        }

        writer.writerow(data)
