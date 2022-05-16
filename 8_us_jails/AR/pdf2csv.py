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
in_dir = "./pdfs/"
out_dir = "./csvs/"
for file in tqdm(os.listdir(in_dir)):
    f = file.replace(".pdf", ".csv")
    o_f = os.path.join(out_dir, f)
    if not os.path.exists(o_f):
        print("\n ",file)
        # try:
        #     template = templates[file.split()[1][:4]]
        # except KeyError:
        #     template = "./_templates/2021.json"
        template = "./_templates/2021.json"
        df = tabula.io.read_pdf_with_template(
            input_path=os.path.join(in_dir, file),
            template_path=template,
            lattice=False,
            stream=True,
            guess=False)
        print(df)
        is_4 = False
        try:
            df[0].columns = ["jail", "delete", "delete1", "total"]
            is_4 = True
        except ValueError:
            try:
                df[0].columns = ["jail", "delete", "total"]
            except ValueError:
                print("\n [*] Moving file...")
                # Move file to broken_pdfs
                os.rename(os.path.join(in_dir, file), os.path.join("./broken_pdfs/", file))
                continue
        df = df[0]
        if is_4:
            # print(df)
            df = df.drop(["delete", "delete1"], axis=1)
            df.dropna(subset=["jail", "total"], inplace=True)
            df = df[df.total != "Pop."]
        else:
            df = df.drop(["delete"], axis=1)
            df.dropna(subset=["jail", "total"], inplace=True)
            df = df[df.total != "Pop."]
            df[["jail"]] = df[["jail"]].apply(lambda x: x.str.replace(" Med/Min", "").replace(" Med/Max", "").replace("Min", ""))


        print(df)
        df.to_csv(o_f, header=True, index=False)
        # break
