import pandas as pd
import os


f_list = ["cleaned_first1.csv", "cleaned.csv"]

df_from_each_file = (pd.read_csv(f) for f in f_list)
df = pd.concat(df_from_each_file, ignore_index=True)

df["description"] = df["description"][:10000]
df["object_number"] = df["object_number"].apply(lambda x: x[:50] if not pd.isnull(x) else x)
df = df.drop_duplicates(subset=["object_number"])
df = df.dropna(subset=["object_number"])

# df.loc[df['maker_death_year'] == '|', 'maker_death_year'] = pd.NA

df.to_csv("combined_clean.csv", index=False)
