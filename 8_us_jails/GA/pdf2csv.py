import tabula
import pandas as pd
import polars as pl
import os
from tqdm import tqdm

templates = {
    "2021": "./_templates/2021_temp.tabula-template.json",
    "2020": "./_templates/2020_temp.tabula-template.json",
}
in_dir = "./pdfs/"
out_dir = "./csvs/"
for file in tqdm(os.listdir(in_dir)):
    f = file.replace(".pdf", ".csv")
    o_f = os.path.join(out_dir, f)
    if not os.path.exists(o_f):
        print("\n ",file)
        try:
            template = templates[file.split("-")[1][:4]]
        except KeyError:
            template = "./_templates/template.tabula-template.json"

        df = tabula.io.read_pdf_with_template(
            input_path=os.path.join(in_dir, file),
            template_path=template,
            lattice=True,
            stream=False,
            guess=False)
        # print(df)
        # df = pl.from_pandas(df)

        # df = pl.concat([pl.from_pandas(x) for x in df])
        # print(df)
        df = pd.concat(df)
        # print(df)
        # df = pl.from_pandas(df)
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
        # break
