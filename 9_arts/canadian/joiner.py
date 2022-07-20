import pandas as pd
import os

path = './files/'
f_list = [os.path.join(path, files) for files in os.listdir(path)]

df_from_each_file = (pd.read_csv(f) for f in f_list)
concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)

df = concatenated_df
df["inscription"] = df["inscription"][:4000]
df["institution_longitude"] = -75.7169418334961
df["materials"] = df["material"].str.replace("|", ",")
df["from_location"] =  df["from_location"].str.strip(", ")
df["category"] = df["category"].str.replace("|", ",")
df.to_csv("combined.csv", index=False)
