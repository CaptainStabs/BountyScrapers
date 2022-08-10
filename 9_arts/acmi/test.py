import json
import os

import pandas as pd
from tqdm import tqdm

def desc_checker(desc, brief):
    if desc[0] == brief:
        print("Yes")
    else:
        print("No")

with open("download.json", "r") as f:
    j = json.load(f)
    j = j['results']

df = pd.DataFrame.from_dict(j)
print(df.columns)
df.apply(lambda x: desc_checker(x["description_for_label"], x["brief_description"]), axis=1)

print(df["description_for_label"])
# print(df["description"].loc[0].strip("<p>").strip("</p>"))
# print(df["headline_credit"])
