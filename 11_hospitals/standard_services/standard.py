import pandas as pd


df = pd.read_csv("possible_indirects.csv")

df = df.dropna(subset=["cdm_indirect_url"])
df = df[df["cdm_indirect_url"].str.contains("standard-services")]
df.to_csv("standard_services.csv", index=False)
