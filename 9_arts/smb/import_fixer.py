import pandas as pd


df = pd.read_csv('smb.csv')
df["accession_number"] = df.apply(lambda x: x["object_number"].split("|")[0] if "." in x["object_number"] else pd.NA, axis=1)
df["object_number"] = df.apply(lambda x: x["source_1"].split("/")[-1], axis=1)
# df = df.dropna(subset="object_number")

df.to_csv("fixed_smb.csv", index=False)
