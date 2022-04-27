import pandas as pd
import polars as pl
import os
from tqdm import tqdm


in_dir = "./manual_csvs/"
out_dir = "./a/"
for f in tqdm(os.listdir(in_dir)):
    o_f = os.path.join(out_dir, f)
    if not os.path.exists(o_f):
        df = pd.read_csv(os.path.join(in_dir, f))
        try:
            df.columns = ["index", "jail", "total", "delete0", "delete1", "convicted_or_sentenced", "delete2", "detained_or_awaiting_trial", "delete3", "convicted", "delete4", "other_offense", "delete5"]
        except ValueError:
            print("\n [*] Moving file...")
            # Move file to broken_pdfs
            os.rename(os.path.join(in_dir, file), os.path.join("./broken_pdfs/", file))
            continue
        df = df.drop([f"delete{x}" for x in range(0,6)], axis=1)

        # df = df.to_pandas()
        df["convicted_or_sentenced"] = df[["convicted_or_sentenced", "convicted"]].sum(axis=1)
        df.drop(["index", "convicted"], inplace=True, axis=1)
        df = df[df["jail"].str.contains("NO JAIL")==False]
        df.to_csv(o_f, header=True, index=False)
