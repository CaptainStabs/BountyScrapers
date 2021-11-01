import csv
import pandas as pd
import os
from tqdm import tqdm

columns = ["name", "city", "state", "address", "zip", "district", "lat", "lon", "public_private"]

with open("Public_School_Characteristics_2017-181.csv", "r", encoding="utf-8") as input_source:
    df = pd.read_csv(input_source)
    df_columns = list(df.columns)
    data_columns = ",".join(map(str, df_columns))
    line_count = 0
    for line in input_source.readlines():
        line_count += 1

with open("reimport.csv", "a", encoding="utf-8") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)
    if os.stat("reimport.csv").st_size == 0:
        writer.writeheader()

    for index, row in tqdm(df.iterrows(), total=line_count):
        school_info = {}
        school_info["name"] = row["name"].upper()
        school_info["city"] = row["city"].upper()
        school_info["state"] = row["state"].upper()
        school_info["address"] = str(row["address"]).upper()
        school_info["district"] = str(row["district"]).upper()
        school_info["zip"] = row["zip"]
        school_info["lat"] = row["lat"]
        school_info["lon"] = row["lom"]
        # school_info["district"] = row["district"].upper()
        school_info["public_private"] = row["public_private"]
        writer.writerow(school_info)
