import pandas as pd

df = pd.read_csv('tabula-Tpop1d2201.csv')['name']
df2 = pd.read_csv('address_updated.csv')['facility_name']
df3 = pd.concat([df, df2]).drop_duplicates(keep=False)
print(df3)
