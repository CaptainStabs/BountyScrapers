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
import calendar
import sys
import re
p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))

from _common.sql_query import jail_name_search
from _common.utils import remove_file

# Connection to DB, connecting here so that it doesn't disconnect
conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='us_jails')

# Source URL df for mapping file back to origin
su = pl.read_csv("urls.csv", has_header=False)
su.columns = ["file", "url"]
su = dict(zip(su["file"], su["url"]))

templates = {
    # "2015": "./_templates/2015.json",
    "2016": "./_templates/2016.json",
    "2017C": "./_templates/2017C.json",
    "2018": "./_templates/2018.json",
    # "2019": "./_templates/2019.json",
    "2020": "./_templates/2020.json",

}

months = []
for i in range(1,13):
    months.append((calendar.month_name[i]))
print(months)

def remove_months(cur_string, replace_list):
  for cur_word in replace_list:
    cur_string = cur_string.replace(cur_word, '')
  return cur_string

in_dir = "./pdfs/"
out_dir = "./csvs/"
remove_file("extracted_data.csv")
for i, file in tqdm(enumerate(os.listdir(in_dir))):
    f = file.replace(".pdf", ".csv")
    o_f = os.path.join(out_dir, f)
    if not os.path.exists(o_f):
        print("\n ",file)
        try:
            # template = templates[file[:-4].replace("AdultPopulation", "")]
            template = templates[re.sub('\D', '', file).replace(".", "")]
        except KeyError:
            template = "./_templates/2020.json"
        # print(template)
        df = tabula.io.read_pdf_with_template(
            input_path=os.path.join(in_dir, file),
            template_path=template,
            lattice=False,
            stream=True,
            guess=False)

        date = file.replace("AdultPopulation", "")[:-4].strip("B").strip("C")
        try:
            date = dt.strptime(date, '%B%Y')
        except ValueError:
            date = dt.strptime(date, '%B%d%Y')
        day = calendar.monthrange(date.year, date.month)[1]
        date = "-".join([str(date.year), str(date.month), str(day)])
        date = dt.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")

        df = df[0]
        # print(template)
        try:
            if df.columns[0] == "Adult Corrections:":
                df.columns = ["jail", "male", "female", "delete_total", "male1", "female1", "total"]
                df = df[1:]
            else:
                df.columns = ["jail", "male", "female", "delete_total", "male1", "female1", "total"]
        except:
            print(df)
            continue
            # sys.exit(1)

        # Replace NaN with 0
        df = df.fillna(0)

        df.drop("delete_total", axis=1, inplace=True)

        df = df[~df['jail'].isin(["**Other", "*Community", "Male Total", "Total Adult Population"])]
        df = df[~df.jail.str.contains('\*')]
        df["id"] = df.apply(lambda x: jail_name_search(x["jail"].strip().strip("'"), "SD", conn, split=True), axis=1)

        df.dropna(subset=["id"], inplace=True)
        df.drop("jail", axis=1, inplace=True)
        df["snapshot_date"] = date
        df["source_url"] = su[file]

        # Cannot use pl's from_pandas, using workaround instead
        df.to_csv("temp.csv", index=False)
        df = pl.read_csv("temp.csv")
        remove_file("temp.csv")
        # cols = ["male", "female", "male1", "female1"]
        # df[cols] = df[cols].apply(lambda x: x.str.replace(",", "").astype(float))
        df["federal_offense"] =  df[["male1", "female1"]].sum(axis=1)
        df["male"] = df[["male", "male1"]].sum(axis=1)
        df["female"] = df[["female", "female1"]].sum(axis=1)
        df["total"] = df[["total", "federal_offense"]].sum(axis=1)
        df = df.drop(["male1", "female1"])
        # print(df)
        # print(df)
        # print(len(df))
        df = df.to_pandas()
        df.drop_duplicates(subset=["snapshot_date","id"], inplace=True)
        # print(len(df))

        if not i:
            df.to_csv("extracted_data.csv", mode="a", index=False)
        else:
            df.to_csv("extracted_data.csv", mode="a", index=False, header=False)
