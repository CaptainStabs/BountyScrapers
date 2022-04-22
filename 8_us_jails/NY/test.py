import polars as pl
file = 'Albany County Jail.csv'
df = pl.read_csv(f"./files/{file}")
print(df['type'])
# Drop last column (date range)
df = df.drop(['jail', 'delete'])
# Remove old header
df = df[1:]

df = df.transpose(include_header=True)
df = df.drop("column_1")
# print(df)
# df2 = df.to_pandas()
# print(df2[0])
df.columns = ["snapshot_date", "total_off_site", "total", "convicted_or_sentenced", "civil_offense", "federal_offense", "technical_parole_violators", "state_readies", "detained_or_awaiting_trial"]
print(df[0])
