import pandas as pd

df = pd.read_csv("UHC_payers_deduped.csv")

df = df.sort_values(by=["size"])

df.to_csv("UHC_payers_deduped_sorted.csv", index=False)