import csv
from tqdm import tqdm
import os
import pandas as pd

columns = ["name", "business_type", "state_registered", "city_physical"]

filename = "rhode_island_physical.csv"
output_filename = "cleaned_physical_commas.csv"
column_name = "city_registered" # city_registered or city_physical

with open(filename, "r") as f:
    lines = f.readlines()
    total = 0
    for line in lines:
        total += 1

df = pd.read_csv(filename)
df_columns = list(df.columns)
data_columns = ",".join(map(str, df_columns))

with open(output_filename, "a", encoding="utf-8") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat(output_filename).st_size == 0:
        writer.writeheader()



    for index, row in tqdm(df.iterrows(), total=total):
        old_city = row[column_name]
        city = old_city.split(",")[0]
        # print(f"\n{old_city_registered} -> {city_registered}")
        data = {
            "name": row["name"],
            "business_type": row["business_type"],
            "state_registered": row["state_registered"],
            colunmn_name: str(city).strip(),
        }

        writer.writerow(data)
