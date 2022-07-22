import pandas as pd

df = pd.read_csv("combined.csv")

print(df.columns)
print(df['from_location'].equals(df['from_location.1']))
