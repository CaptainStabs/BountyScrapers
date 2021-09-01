import csv
import os
import pandas as pd
from _ignored_domains import ignored_domains
from tqdm import tqdm

columns = ["name", "city", "state", "website"]


with open("check.csv", "r", encoding="utf-8") as input_source:
    df = pd.read_csv(input_source)
    df_columns = list(df.columns)
    data_columns = ",".join(map(str, df_columns))

with open("dirty_websites2.csv", "a", encoding="utf-8") as output2:
    writer2 = csv.DictWriter(output2, fieldnames=columns)
    if os.stat("dirty_websites2.csv").st_size == 0:
        writer2.writeheader()

    for index, row in tqdm(df.iterrows()):
        for ignored_domain in ignored_domains:
            if ignored_domain in str(row["website"]):
                website = str(row["website"])
                print(f"\nignored_domain: {ignored_domain}\n      website: {website}")
                output_dict = {}
                output_dict["name"] = row["name"]
                output_dict["city"] = row["city"]
                output_dict["state"] = row["state"]
                output_dict["website"] = ""
                writer2.writerow(output_dict)
