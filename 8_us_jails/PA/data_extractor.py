import os
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)
import pandas as pd
import polars as pl
import numpy as np
import mysql.connector
from tqdm import tqdm; tqdm.pandas()
from pathlib import Path
import sys
p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))

from _common.sql_query import search_and_add
from _common.utils import remove_file

in_dir = "./csvs/"
conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='us_jails')

remove_file("extracted_data")

df = pl.read_csv('input_data.csv', has_header=True, null_values="N/A")
df = df[df.Institution != "In Federal Prisons"]
df = df[df.Institution != "In County Prisons"]

df = df.to_pandas()
# x = df.iloc[0]
# print(df)
df["id"] = df.progress_apply(lambda x: search_and_add(x["Institution"], state="PA", conn=conn, county=x["County"], address=x["Address + Lat/Long"], split=True, verbosity=20), axis=1)
df["snapshot_date"] = df.apply(lambda x: pd.to_datetime(x["Date"], yearfirst=True), axis=1)
df["source_url"] = "https://data.pa.gov/Public-Safety/State-Correction-Population-June-2015-Current-Mont/a8qx-qnix"
# print(df)
df.dropna(subset=["id"], inplace=True)
df["total"] = df["Corrections Population"]
df.drop(["Fiscal Year", "Institution", "Institution Type", "County", "Address + Lat/Long", "Corrections Population", "Date"], axis=1, inplace=True)

df.to_csv("extracted_data.csv", index=False)
