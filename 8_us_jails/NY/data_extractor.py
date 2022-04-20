import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import polars as pl
import pandas as pd
import doltcli as dolt
import mysql.connector


# import heartrate; heartrate.trace(browser=True, daemon=True)
# pl.set_option('display.max_columns', 8)
columns = ["snapshot_date", "total_off_site", "total", "convicted_or_sentenced", "detained_or_awaiting_trial", "other_offense", "id"]
snap_dates = ["2021-04-01", "2021-05-01", "2021-06-01", "2021-07-01", "2021-08-01", "2021-09-01", "2021-10-01", "2021-11-01", "2021-12-01", "2022-02-01", "2022-03-01", "2022-04-01"]
in_col = {
    0:""
}
conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='us_jails')
cursor = conn.cursor()
if os.path.exists("extracted_data.csv"):
    os.remove("extracted_data.csv")
# db = dolt.Dolt("C:\\Users\\adria\\us-jails"\\)
with open("extracted_data.csv", "a") as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=columns)
    for i, file in enumerate(os.listdir("./files/")):
        jail_name = " ".join(file.split()[:2])
        cursor.execute(f"SELECT id from jails where facility_name like '{jail_name}%' and facility_state in ('NY');")

        id = list()
        for r in cursor:
            id.append(r)
        if len(id) > 1 or not int(len(id)):
            print("TOO MANY/NOT ENOUGH IDS:", id, file)
            continue
        else:
            id = id[0][0]
        print(file)
        df = pl.read_csv(f"./files/{file}")
        # Drop last column (date range)
        df = df.drop(['jail', 'delete'])
        # Remove old header
        df = df[1:]

        df = df.transpose(include_header=True)
        # print(df[0])
        df = df.drop("column_1")
        # print(df)
        # df2 = df.to_pandas()
        # print(df2[0])
        df.columns = ["snapshot_date", "total_off_site", "total", "convicted_or_sentenced", "civil_offense", "federal_offense", "technical_parole_violators", "state_readies", "detained_or_awaiting_trial"]
        df = df[1:]
        # print(df)
        df2 = df.to_pandas()
        con_col = ["state_readies", "detained_or_awaiting_trial"]
        # df2[con_col] = pd.to_numeric(df2[con_col].stack(), downcast="integer", errors='coerce').unstack()
        df2["state_readies"] = pd.to_numeric(df2["state_readies"], downcast="integer")
        df2["detained_or_awaiting_trial"] = pd.to_numeric(df2["detained_or_awaiting_trial"], downcast="integer")

        df2["detained_or_awaiting_trial"] = df2[["detained_or_awaiting_trial", "state_readies"]].sum(axis=1)
        # df = pl.from_pandas(df2)
        df = df2
        df = df.drop("state_readies", axis=1)
        # df = df.to_pandas()
        print(id)
        df["id"] = id
        df["source_url"] = "https://www.criminaljustice.ny.gov/crimnet/ojsa/jail_population.pdf"
        # print(df.info())

        if not i:
            df.to_csv("extracted_data.csv", mode="a", index=False)
        else:
            df.to_csv("extracted_data.csv", mode="a", header=False, index=False)
