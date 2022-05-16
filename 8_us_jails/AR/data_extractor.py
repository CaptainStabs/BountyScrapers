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
    df["id"] = df.apply(lambda x: jail_name_search(x["jail"].strip().strip("'"), "AR", conn, split=False, exact=True), axis=1)
    df.drop("jail", inplace=True, axis=1)
    df["snapshot_date"] = f"{file.replace('.csv', '')}-12-31"
    # print()
    # print(df)
    df["source_url"] = su[int(file[:-4])]
    if not i:
        df.to_csv("extracted_data.csv", mode="a", index=False)
    else:
        df.to_csv("extracted_data.csv", mode="a", index=False, header=False)
