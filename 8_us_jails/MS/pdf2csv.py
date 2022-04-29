import tabula
import pandas as pd
import polars as pl
import os
from tqdm import tqdm
import PyPDF2
# pd.set_option('display.max_columns',50)

in_dir = "./pdfs/"
out_dir = "./csvs/"
for file in tqdm(os.listdir(in_dir)):
    f = file.replace(".pdf", ".csv")
    i_f = os.path.join(in_dir, file)
    o_f = os.path.join(out_dir, f)
    if not os.path.exists(o_f):
        print("\n ",file)

        if file == "April 2014.pdf":
            p = "april"
        else:
            p = PyPDF2.PdfFileReader(open(i_f, 'rb'))
            p = p.numPages

        df_l = tabula.io.read_pdf_with_template(
            input_path=os.path.join(in_dir, file),
            template_path=f"./templates/{p}.json",
            lattice=True,
            stream=False,
            guess=False)

        for i, idf in enumerate(df_l):
            if not i:
                df = [idf]
            else:
                df.append(idf.iloc[: , 1:])

        df = pd.concat(df, axis=1)
        try:
            df.drop("Capacity", axis=1, inplace=True)
        except:
            pass

        # for x in drop_col:
        #     df = df[df.Location != x]
        try:
            df = df.drop("Unnamed: 0", axis=1)
        except Exception as e:
            print(e)

        drop_row = ["County Jails", "COMMUNITY WORK CENTERS", "REGIONAL CORRECTIONAL FACILITIES", "PRIVATE PRISONS", "RESTITUTION CENTERS", "GOVERNOR'S MANSION", "E-CODE", "NaN", "TOTALS"]
        df = df.drop(df[df.Location.isin(drop_row)].index)
        df = df.dropna(subset="Location")

        # cols = df.columns[1:]

        # Instead of blindly grabbing all but first col, select only cols with dtype object
        cols = df.dtypes[df.dtypes == 'object'].index.tolist()[1:   ]
        df[cols] = df[cols].apply(lambda x: x.str.replace(",", ""))
        df[cols] = df[cols].apply(pd.to_numeric)
        df["total"] = df.iloc[:, 1:].mean(axis=1).round(0)

        df = df.drop(list(cols), axis=1)

        df.to_csv(o_f, header=True, index=False)
