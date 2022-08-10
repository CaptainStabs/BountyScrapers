import pandas as pd

df = pd.read_csv("extracted_data.csv")

df["dimensions"] = df["dimensions"].str.replace("|", ", ")
df["materials"] = df["materials"].str.replace("|", ', ')

df.to_csv("fixed_data.csv", index=False)
