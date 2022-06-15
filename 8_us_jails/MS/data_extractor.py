import os
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)
import pandas as pd
import polars as pl
import numpy as np
import mysql.connector
from pathlib import Path
from tqdm import tqdm
from datetime import datetime as dt
import sys
p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))

from _common.month_incrementers import file_month_incrementer
from _common.sql_query import jail_name_search
from _common.utils import remove_file

# Connection to DB, connecting here so that it doesn't disconnect
conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='us_jails')

# Source URL df for mapping file back to origin
su = pl.read_csv("urls.csv", has_header=False)
su.columns = ["file", "url"]
su = dict(zip(su["file"], su["url"]))

in_dir = "./csvs/"

remove_file("extracted_data.csv")
for i, file in tqdm(enumerate(os.listdir(in_dir))):
    # print("\n ", file)

    df = pd.read_csv(os.path.join(in_dir, file))
    df.drop("Avg Pop", errors='ignore', inplace=True)
    date = dt.strptime(df.columns[-2], '%d-%b-%y')
    df["snapshot_date"] = date.strftime("%Y-%m-%d")

    df.columns = ["jail", "date", "total", "snapshot_date"]
    df["id"] = df.apply(lambda x: jail_name_search(x["jail"].strip().strip("'"), "MS", conn), axis=1)
    df["source_url"] = su[file.replace(".csv", "")]
    df["source_url_2"] = "https://www.mdoc.ms.gov/Admin-Finance/Pages/Daily-Inmate-Population.aspx"

    df.dropna(subset=["id"], inplace=True)
    df.drop(["jail", "date"], axis=1, inplace=True)
    df.drop_duplicates(subset=["id", "snapshot_date"])

    if not i:
        df.to_csv("extracted_data.csv", mode="a", index=False)
    else:
        df.to_csv("extracted_data.csv", mode="a", index=False, header=False)

df = pd.read_csv("extracted_data.csv")
print(len(df))
df = df.drop_duplicates(subset=["id", "snapshot_date"])
df.to_csv("extracted_data2.csv", index=False)
print(len(df))
