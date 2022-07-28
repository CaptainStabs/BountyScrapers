import pandas as pd


df = pd.read_csv('smb.csv')
df["object_number"] = df["object_number"].str.split("|").str[0]
df["object_number"] = df.apply(lambda x: x["source_1"].split("/")[-1] if x["object_number"] == "nan" else x["object_number"], axis=1)
# df = df.dropna(subset="object_number")

df.to_csv("fixed_smb.csv", index=False)
