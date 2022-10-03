import pandas as pd

df1 = pd.read_csv('assessors_data.csv')

df2 = pd.read_csv("parcels.csv")
df2 = df2[["PPI", "Latitude", "Longitude"]]

df =  pd.merge(df1, df2, on="PPI", how='inner')
df.to_csv("combined.csv", index=False)
