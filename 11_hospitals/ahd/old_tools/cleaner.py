import pandas as pd

df = pd.read_csv("url_added.csv")
df2  = pd.read_csv("hospitals_state_code.csv")

df3 = pd.merge(df, df2, how="left",on=['name','ccn'])

df3.to_csv("fixed.csv", index=False)
