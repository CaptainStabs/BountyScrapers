import pandas as pd
import csv
import os


columns = ["name", "city", "state", "county", "district_id"]


df = pd.read_csv("HIFLD_Schools.csv")
df_columns = list(df.columns)
data_columns = ",".join(map(str, df_columns))


with open("HIFLD_less_fields.csv", "a", encoding="utf-8") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)
    if os.stat("HIFLD_less_fields.csv").st_size == 0:
        writer.writeheader()

    for index, row in df.iterrows():
        csv_dict = {}
        csv_dict["name"] = row["name"]
        csv_dict["city"] = row["city"]
        csv_dict["state"] = row["state"]
        csv_dict["county"] = row["COUNTY"]
        csv_dict["district_id"] = row["DISTRICTID"]
        writer.writerow(csv_dict)
