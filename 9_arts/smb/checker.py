import pandas as pd

df = pd.read_csv("combined.csv")

print(df.columns)
# print(df['from_location'].equals(df['from_location.1']))

df = df.drop_duplicates(subset=["object_number", "institution_name"])
# df = df.drop("from_location.1", axis=1)
df["dimensions"] = df["dimensions"].apply(lambda x: x[:5000] if not pd.isnull(x) else x)
df["title"] = df["title"].apply(lambda x: x[:1000] if not pd.isnull(x) else x)
df["date_description"] = df["date_description"].apply(lambda x: x[:500] if not pd.isnull(x) else x)
df["object_number"] = df["object_number"].apply(lambda x: x[:50] if not pd.isnull(x) else x)
df["description"] = df["description"].apply(lambda x: x[:10000] if not pd.isnull(x) else x)
df["drop_me"] = df["drop_me"].astype(str)
df["object_number"] = df["object_number"].astype(str)
# df["object_number"] = df[['object_number', 'drop_me']].agg('|'.join, axis=1)
df["object_number"] = df["object_number"].str.replace("<html><body>", "").replace("<\html><\body>", "")
df["object_number"] = df["object_number"].apply(lambda x: x[:50] if not pd.isnull(x) else x)
df["object_number"] = df["object_number"].str.strip()

df2 = df[df["object_number"].isnull()]
print("Duplicate", len(df.duplicated(subset="object_number")))
# df2 = pd.concat([df[df["object_number"].isnull()], df.duplicated(subset="object_number")])
print("Before Drop Dupes:", len(df))
df = df.drop_duplicates(subset=["object_number"])
print("After drop dupe:", len(df))
print("Before drop NA:", len(df))
df = df.dropna(subset=["object_number"])
print("After drop na:", len(df))

df.to_csv("cleaned.csv", index=False)
df2.to_csv("removed.csv", index=False)
