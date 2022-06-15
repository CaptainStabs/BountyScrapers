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
import tabula
import sys
p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))

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

templates = {
    "December 2019.pdf": "./templates/December 2019.json",
    "April": "./templates/April 2020.json", # One letter leak
    "August": "./templates/April 2020.json",
    "July": "./templates/July 2019.json", # Fix for two letters leak
    "June": "./templates/July 2019.json",
    "March": "./templates/April 2020.json",
    "May": "./templates/July 2019.json",
}

in_dir = "./pdfs/"
out_dir = "./csvs/"
remove_file("extracted_data.csv")
for i, file in tqdm(enumerate(os.listdir(in_dir))):
    f = file.replace(".pdf", ".csv")
    o_f = os.path.join(out_dir, f)
    if not os.path.exists(o_f):
        print("\n ",file)
        try:
            template = templates[file.split()[0]]
        except KeyError:
            template = "./templates/December 2019.json"
        print(template)
        df = tabula.io.read_pdf_with_template(
            input_path=os.path.join(in_dir, file),
            template_path=template,
            lattice=False,
            stream=True,
            guess=False)

        date = df[1].columns[0]
        date = dt.strptime(date, '%B %d, %Y')
        df = df[0]

        try:
            df.columns = ["jail", "total"]
        except ValueError:
            print("\n [*] Moving file...")
            # Move file to broken_pdfs
            os.rename(os.path.join(in_dir, file), os.path.join("./broken_pdfs/", file))
            continue

        df = df[~df['jail'].isin(["Institutions", "Male Institutions", "Male Total", "Female Institutions", "Female Total"])]
        df["id"] = df.apply(lambda x: jail_name_search(x["jail"].strip().strip("'"), "CA", conn, split=False), axis=1)
        df.dropna(subset=["id"], inplace=True)
        df.drop("jail", axis=1, inplace=True)
        df["snapshot_date"] = date.strftime("%Y-%m-%d")
        df["source_url"] = su_1[file[:-4].split()[-1]]
        df["source_url_2"] = su[file[:-4]]
        cols = ["total"]
        df[cols] = df[cols].apply(lambda x: x.str.replace(",", "").astype(float))
        print(len(df))
        df.drop_duplicates(subset=["snapshot_date","id"], inplace=True)
        print(len(df))
        
        if not i:
            df.to_csv("extracted_data.csv", mode="a", index=False)
        else:
            df.to_csv("extracted_data.csv", mode="a", index=False, header=False)
