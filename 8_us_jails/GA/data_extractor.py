import os
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)
import pandas as pd
import polars as pl
import numpy as np
import mysql.connector
from pathlib import Path
from tqdm import tqdm
import sys
p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))

from _common.month_incrementers import file_month_incrementer
from _common.sql_query import jail_name_search
from _common.utils import remove_file

# Connection to DB, connecting here so that it doesn't disconnect
conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='us_jails')

# Source URL df for mapping file back to origin
su = pl.read_csv("urls0.csv", has_header=False)
su.columns = ["file", "url"]
su = dict(zip(su["file"], su["url"]))

in_dir = "./csvs/"

remove_file("extracted_data.csv")
for i, file in tqdm(enumerate(os.listdir(in_dir))):
    print("\n ", file)
    df = pd.read_csv(os.path.join(in_dir, file))

    date = " 01 ".join(file.split("_")[-1][:-4].split("-"))
    df["snapshot_date"] = file_month_incrementer(date, str_format='%b %d %Y')

    df["id"] = df.apply(lambda x: jail_name_search("%".join([x["jail"].strip().strip("'"), "County", "Jail"]), "GA", conn, county=x["jail"].split()[0]), axis=1)
    df["source_url"] = su[file.replace("tabula-", "")]
    df["source_url_2"] = "https://www.dca.ga.gov/node/3811/documents/2086"

    df.dropna(subset=["id"], inplace=True)
    df.drop("jail", axis=1, inplace=True)

    if not i:
        df.to_csv("extracted_data.csv", mode="a", index=False)
    else:
        df.to_csv("extracted_data.csv", mode="a", index=False, header=False)
