import pandas as pd

df = pd.read_csv('extracted_data.csv')

df = df.drop("drop_me", axis=1)

df["year_start"] = df["year_start"].apply(lambda x: x.split("-")[0] if isinstance(x, str) else x)
df["year_end"] = df["year_end"].apply(lambda x: x.split("-")[0] if isinstance(x, str) else x)

df.to_csv('finished.csv', index=False)
