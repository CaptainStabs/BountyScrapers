import pandas as pd
import numpy as np

ind_cols = "ccn"
df1 = pd.read_csv("original.csv", index_col=ind_cols)
df1 = df1.sort_index()

df2 = pd.read_csv("updated.csv", index_col=ind_cols)
df2 = df2.sort_index()
df2 = df2.rename({"homepage_url":"updated_url"})

df = df1.merge(df2, how="outer", on=["name", "ccn", "state_code"])


df.to_csv("test.csv", index=False)
