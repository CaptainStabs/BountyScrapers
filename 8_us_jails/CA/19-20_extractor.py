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
su = pl.read_csv("urls_19.csv", has_header=False)
su.columns = ["file", "url"]
su = dict(zip(su["file"], su["url"]))

su_1 = {
    "2019": "https://www.cdcr.ca.gov/research/monthly-total-population-report-archive-2019/",
    "2020": "https://www.cdcr.ca.gov/research/https-www-cdcr-ca-gov-research-monthly-total-population-report-archive-2020/"
}

in_dir = "./csvs/"

remove_file("extracted_data.csv")
for i, file in tqdm(enumerate(os.listdir(in_dir))):
    # print("\n ", file)

    df = pd.read_csv(os.path.join(in_dir, file))
    df = df[~df['jail'].isin(["Institutions", "Male Institutions", "Male Total", "Female Institutions"])]
    # df["source_url"] = su_1[file[:-4].split()[-1]]
    # df["source_url_2"] = su[file.replace(".csv", "")]
    print(df)
    break
