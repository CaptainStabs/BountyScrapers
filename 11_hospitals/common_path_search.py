import pandas as pd
from urllib.parse import urlparse


df = pd.read_csv("./paylesshealth-1/most_common_path.csv")

df = df["cdm_indirect_url"]

df = df.apply(lambda x: urlparse(x).path if pd.notna(x) else pd.NA)

df = df.drop_duplicates()
df.to_csv("paths.csv", index=False)


print(df)
