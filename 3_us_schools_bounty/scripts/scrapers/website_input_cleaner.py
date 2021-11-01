import csv
import os
import pandas as pd

columns = ["name", "city", "state", "address", "website"]

with open("websites_HIFLD_Schools.csv", "r", encoding="utf-8") as input_source:
    df = pd.read_csv(input_source)
    df_columns = list(df.columns)
    data_columns = ",".join(map(str, df_columns))

    with open("Smaller_HIFLD_Schools.csv", "a", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=columns)

        if os.stat("Smaller_HIFLD_Schools.csv").st_size == 0:
            writer.writeheader()

        for index, row in df.iterrows():
            if pd.isnull(row["website"]):
                output_dict = {}
                output_dict["name"] = row["name"]
                output_dict["city"] = row["city"]
                output_dict["state"] = row["state"]
                output_dict["address"] = row["address"]
                # output_dict["website"] = row["website"]

                writer.writerow(output_dict)
