import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import polars as pl
import pandas as pd
# import heartrate; heartrate.trace(browser=True, daemon=True)
# pl.set_option('display.max_columns', 8)
columns = ["snapshot_date", "total_off_site", "total", "convicted_or_sentenced", "detained_or_awaiting_trial", "other_offense", "id"]
snap_dates = ["2021-04-01", "2021-05-01", "2021-06-01", "2021-07-01", "2021-08-01", "2021-09-01", "2021-10-01", "2021-11-01", "2021-12-01", "2022-02-01", "2022-03-01", "2022-04-01"]
in_col = {
    0:""
}
with open("extracted_data.csv", "a") as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=columns)
    for file in os.listdir("./files/"):
        # with open(f"./files/{file}", "r") as f:
        #     line_count = len([line for line in f.readlines()]) - 1
        #     f.seek(0)
        #     # for i, line in tqdm(enumerate(f), total=line_count):
        #     lines = []
        #     for i, line in enumerate(f):
        #         cols = line.split(',')[2:]
        #         lines.append(line)
        #
        #         for j, col in cols:
        #             if col[i].lower() == "census": continue
        #
        #             jail_info = {
        #                 "id": file,
        #                 "snapshot_date": snap_dates[j],
        #
        #             }

        df = pl.read_csv(f"./files/{file}")
        print(df)
        # Drop last column (date range)
        df = df.drop(['jail', 'delete'])
        # Remove old header
        df = df[1:]

        df = df.transpose(include_header=True)
        df = df.drop(["column_0", "column_2"])
        print(df)
        df.columns = ["snapshot_date", "total_off_site", "total", "convicted_or_sentenced", "civil_offense", "federal_offense", "technical_parole_violators", "state_readies", "detained_or_awaiting_trial"]
        df = df[1:]
        print(df)
        df2 = df.to_pandas()
        con_col = ["state_readies", "detained_or_awaiting_trial"]
        # df2[con_col] = pd.to_numeric(df2[con_col].stack(), downcast="integer", errors='coerce').unstack()
        df2["state_readies"] = pd.to_numeric(df2["state_readies"], downcast="integer")
        df2["detained_or_awaiting_trial"] = pd.to_numeric(df2["detained_or_awaiting_trial"], downcast="integer")

        df2["detained_or_awaiting_trial"] = df2[["detained_or_awaiting_trial", "state_readies"]].sum(axis=1)
        df = pl.from_pandas(df2)
        df = df.drop("state_readies")
        df["id"] = file
    
        # df.to_csv("extracted_data", mode="a")
