import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
# import heartrate; heartrate.trace(browser=True, daemon=True)

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

        df = pd.read_csv(f"./files/{file}")
        df = df.iloc[: , :-1]
        # print(df)
        df.columns=["jail", "type", "2021-04-01", "2021-05-01", "2021-06-01", "2021-07-01", "2021-08-01", "2021-09-01", "2021-10-01", "2021-11-01", "2021-12-01", "2022-01-01", "2022-02-01", "2022-03-01", "2022-04-01"]
        df.drop("jail", 1, inplace=True)
        df = df.transpose()
        df = df.drop(df.columns[[0,2]], axis=1)
        # print(df)
        df.columns=["total_off_site", "total", "convicted_or_sentenced", "civil", "federal", "technical_parole_violators", "state_readies", "detained_or_awaiting_trial"]
        df = df.iloc[1:, :]
        # print(df)
        df["other_offense"] = df[["civil", "federal", "state_readies"]].sum(axis=1)
        df = df.drop(df.columns[[3,4,6]], axis=1)
        df.columns=["snapshot_date", "total_off_site", "total", "convicted_or_sentenced", "detained_or_awaiting_trial", "other_offense"]
        df["id"] = file
        print(df['snapshot_date'].to_csv(index=False))


        # o_df = pd.DataFrame(columns=columns)
        # o_df["id"] = file
        # print(o_df)
        break
