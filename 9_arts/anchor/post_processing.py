import pandas as pd

df = pd.read_csv("extracted_data.csv")

df["provenance"] = df["provenance"].apply(lambda x: str(x)[:4000])

df.to_csv("cleaned_extracted_data.csv", index=False)
