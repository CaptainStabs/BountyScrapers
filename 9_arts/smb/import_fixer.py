import pandas as pd

#
# df = pd.read_csv('smb.csv')
# df["accession_number"] = df.apply(lambda x: x["object_number"].split("|")[0] if "." in x["object_number"] else pd.NA, axis=1)
# df["object_number"] = df.apply(lambda x: x["source_1"].split("/")[-1], axis=1)
# # df = df.dropna(subset="object_number")
#
# df.to_csv("fixed_smb.csv", index=False)

df = pd.read_csv('descriptions_added.csv')
df["accession_number"] = df.apply(lambda x: str(x["object_number"]) if "." in str(x["object_number"]) else pd.NA, axis=1)
df["object_number"] = df.apply(lambda x: x["source_1"].split("/")[-1], axis=1)
df["description"] = df["description"] = df["description"].apply(lambda x: x[:10000] if not pd.isnull(x) else x)
# df = df.dropna(subset="object_number")

df.to_csv("fixed_desc.csv", index=False)
