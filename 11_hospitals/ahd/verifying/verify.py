import pandas as pd

df1 = pd.read_csv("original.csv")
df1 = df1.sort_index()
df2 = pd.read_csv("updated.csv")
df1 = df1.sort_index()

nulls = df1[df1["homepage_url"].isna()]

print(df1)
print(df2)
print(df1.compare(df2))

diff = df1.compare(df2)

diff.to_csv("diff.csv", index=False)
