import pandas as pd

df = pd.read_csv("F:\\_Bounty\\LA\\combined.csv")

print(df.columns)
df = df.dropna(subset="sale_price")

df.to_csv("F:\_Bounty\LA\cleaned.csv", index=False)
