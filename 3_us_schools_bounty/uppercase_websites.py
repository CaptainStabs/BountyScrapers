import pandas as pd
import csv
import os
from tqdm import tqdm

df = pd.read_csv("schools.csv")
df_columns = list(df.columns)
data_colmns = ",".join(map(str, df_columns))

columns = ["name", "city", "state", "website"]

with open("uppercased.csv", "a", encoding="utf-8") as output:
    writer = csv.DictWriter(output, fieldnames=columns)

    if os.stat("uppercased.csv").st_size == 0:
        writer.writeheader()

    for index, row in tqdm(df.iterrows()):
        output_dict = {}
        output_dict["name"] = row["name"]
        output_dict["city"] = row["city"]
        output_dict["state"] = row["state"]
        output_dict["website"] = str(row["website"]).upper()
        writer.writerow(output_dict)

# num_upper = 0
# num_lower = 0
# for index, row in tqdm(df.iterrows()):
#     if str(row["website"]).isupper():
#         num_upper += 1
#     if str(row["website"]).islower():
#         num_lower += 1
#
# print("Upper: " + str(num_upper))
# print("Lower: " + str(num_lower))
