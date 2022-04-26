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

def jail_name_fixer(jail_name):
    # Workhouse is closed so idc
    if jail_name == "Bedford":
        jail_name = "Bedford%County Jail"

    if "Bedford" in jail_name and "Workhouse" in jail_name:
        jail_name = "abc"

    if "Dyer" in jail_name and 'Annex' not in jail_name:

        jail_name = "Dyer%County Jail"

    elif "Dyer" in jail_name and "Annex" in jail_name:
        jail_name = "Dyer%County%Correctional Work Center"

    if "Jefferson" in jail_name and "WH" not in jail_name:
        jail_name = "Jefferson%County Justice Center"
    elif "Jefferson" in jail_name:
        jail_name = "Jefferson%County Sheriffs Department Workhouse"

    if jail_name == "Johnson":
        jail_name = "Johnson County"

    if jail_name == "Rutherford":
        jail_name = "Rutherford%County Adult"
    if jail_name == "Rutherford Work Center":
        jail_name = "Rutherford%Work Center"

    if jail_name == "Sullivan":
        jail_name = "Sullivan County Jail"

    if jail_name == "Sullivan Extension":
        jail_name = "Sullivan Sheriffs Office Extension"

    return jail_name

def female_detector(row):
    if "female" in row.lower():
        print("female")
        return True
    print("not female")
    return False

in_dir = "./csvs/"
con_col = ["pre_trial_felony","pre_trial_misd", "TDOC_Backup"]
conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='us_jails')

su = pl.read_csv("defemaled_urls.csv", has_header=False, skiprows=lambda x: female_detector(x))
# su1.columns = ["file", "url"]
# su1 = pd.read_csv("urls.csv", header=None)
# print(su1)
# su = pd.concat((x.query("'female' in url") for x in su1), ignore_index=True)

su.columns = ["file", "url"]
# su = su[su["url"].str.contains("female")]
su = dict(zip(su["file"], su["url"]))
# print(su)


remove_file("extracted_data.csv")
for i, file in tqdm(enumerate(os.listdir(in_dir))):
    print("\n", file)
    df = pl.read_csv(os.path.join(in_dir, file), has_header=False, skip_rows=3)
    df.columns = ["jail","TDOC_Backup","felony1","felony2","federal_offense","misdemeanor","pre_trial_felony","pre_trial_misd","total"]
    # df2 = df.to_pandas()
    # # df2[con_col] = df2[con_col].apply(pd.to_numeric, errors='coerce')
    # for col in con_col:
    #     df2[col] = pd.to_numeric(df2[col], downcast="integer")
    df["detained_or_awaiting_trial"] = df[con_col].sum(axis=1)
    df["felony"] = df[["felony1", "felony2"]].sum(axis=1)
    df = df.drop(con_col)
    df = df.drop(["felony1", "felony2"])
    df = df.to_pandas()
    date = " 01 ".join(file.split("-")[1][:-4].split())

    # Check if file is one of the day-specific snapshots (2000-2019)
    if "July" in date and int(date.split()[-1]) in range(2000,2020):
        # print(date)
        year = date.split()[-1]
        df["snapshot_date"] = str(year) + "-07-31"
    else:
        df["snapshot_date"] = file_month_incrementer(date)



    # df = pl.from_pandas(df)
    # print(df["jail"])
    df["jail"] = df.apply(lambda x: jail_name_fixer(x["jail"]), axis=1)
    df["id"] = df.apply(lambda x: jail_name_search(x["jail"], "TN", conn), axis=1)
    df["source_url"] = su[file[7:-4]]
    df["source_url_2"] = "https://www.tn.gov/correction/statistics-and-information/jail-summary-reports.html"
    df.dropna(subset=["id"], inplace=True)

    df.drop("jail", axis=1, inplace=True)

    # df = pl.from_pandas(df)
    print(len(df))
    df.drop_duplicates(subset=["snapshot_date","id"], inplace=True)
    print(len(df))
    # df = df.to_pandas()

    if not i:
        df.to_csv("extracted_data.csv", mode="a", index=False)
    else:
        df.to_csv("extracted_data.csv", mode="a", header=False, index=False)
