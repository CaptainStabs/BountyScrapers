import tabula
import pandas as pd
import polars as pl
import os
from tqdm import tqdm
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

templates = {
    # "2021": "./_templates/2021_temp.tabula-template.json",
    "2020": "./templates/April 2020.json",
}

su = pl.read_csv("urls_19.csv", has_header=False)
su.columns = ["file", "url"]
su = dict(zip(su["file"], su["url"]))

su_1 = {
    "2019": "https://www.cdcr.ca.gov/research/monthly-total-population-report-archive-2019/",
    "2020": "https://www.cdcr.ca.gov/research/https-www-cdcr-ca-gov-research-monthly-total-population-report-archive-2020/"
}

in_dir = "./pdfs/"
out_dir = "./csvs/"
for file in tqdm(os.listdir(in_dir)):
    f = file.replace(".pdf", ".csv")
    o_f = os.path.join(out_dir, f)
    if not os.path.exists(o_f):
        print("\n ",file)
        try:
            template = templates[file.split()[1][:4]]
        except KeyError:
            template = "./templates/April 2020.json"

        df = tabula.io.read_pdf_with_template(
            input_path=os.path.join(in_dir, file),
            template_path=template,
            lattice=False,
            stream=True,
            guess=False)

        # date = df[1].columns[0]
        # df = df[0]

        try:
            df[0].columns = ["jail", "total"]
        except ValueError:
            print("\n [*] Moving file...")
            # Move file to broken_pdfs
            os.rename(os.path.join(in_dir, file), os.path.join("./broken_pdfs/", file))
            continue

        print(df)
        df.to_csv(o_f, header=True, index=False)
        # break
