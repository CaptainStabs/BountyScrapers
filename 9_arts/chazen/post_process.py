import pandas as pd


df = pd.read_csv("extracted_data.csv")

df = df.drop("drop_me", axis=1)

df["title"] = df["title"].apply(lambda x: x[:1000])

df.to_csv("cleaned_data.csv", index=False)
