from old_mrfutils import import_csv_to_set, json_mrf_to_csv
import pandas as pd


df = pd.read_csv("first_100.csv"))
# Get first row of df
df = df.iloc[0]

df = df["url"].apply(lambda x: json_mrf_to_csv(loc=x, url=x, npi_filter="quest/npis.csv", code_filter="quest/codes.csv", out_dir="/test/"))