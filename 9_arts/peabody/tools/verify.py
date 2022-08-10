import pandas as pd


df = pd.read_csv("combined.csv")

print(df["maker_full_name"].equals(df["maker_full_name.1"]))
