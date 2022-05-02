import tabula
import pandas as pd
import polars as pl
import os
from tqdm import tqdm
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)
import PyPDF2
# pd.set_option('display.max_columns',50)

custom_templates = {
    "April 2014.pdf": "april",
    "April 2017.pdf": "a2017",
    "April 2009.pdf": "a2009",
    "August 2013.pdf": "a2013",
    "August 2021.pdf": "a2021",
    "December 2014.pdf": "d2014",
    "July 2013.pdf": "j2013",
    "July 2016.pdf": "j2016",
    "June 2013.pdf": "j2013",
    "May 2013.pdf": "j2013",
    "November 2013.pdf": "j2013",
    "November 2018.pdf": "2_l", # No idea why this isn't detected as landascape
    "October 2004.pdf": "o2004",
    "October 2013.pdf": "j2013",
    "September 2013": "j2013",
}

in_dir = "./pdfs/"
out_dir = "./csvs/"
for file in tqdm(os.listdir(in_dir)):
    f = file.replace(".pdf", ".csv")
    i_f = os.path.join(in_dir, file)
    o_f = os.path.join(out_dir, f)

    if not os.path.exists(o_f):
        print("\n ",file)

        try:
            p = custom_templates[file]
        except KeyError:
            pdf = PyPDF2.PdfFileReader(open(i_f, 'rb'))
            p = pdf.numPages
            page = pdf.getPage(0).mediaBox
            # Detect if the page is reaallly w i d e
            if page.getUpperRight_x() - page.getUpperLeft_x() > page.getUpperRight_y() - page.getLowerRight_y():
                print("   [*] Landscape")
                p = str(p) + "_l"

            if "2013" in file:
                p = "j2013"

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
        # df.to_csv("error.csv", header=True, index=False)
        # print(df)
        # print(df.columns)

        df.drop(["Capacity", "Avg Population", "Avg Pop"], axis=1, inplace=True, errors='ignore')

        try:
            # for x in drop_col:
            #     df = df[df.Location != x]
            df = df[df["Location"].str.contains("Note:") == False]
            try:
                df = df.drop("Unnamed: 0", axis=1)
            except Exception as e:
                pass

            drop_row = ["County Jails", "COMMUNITY WORK CENTERS", "REGIONAL CORRECTIONAL FACILITIES", "PRIVATE PRISONS", "RESTITUTION CENTERS", "GOVERNOR'S MANSION", "E-CODE", "NaN", "TOTALS", "Note: Capacity @ MSP does not include 61 beds: 56 at Unit 42 (Hospital) & 5 at Family Vis"]
            df = df.drop(df[df.Location.isin(drop_row)].index)
            df = df.dropna(subset="Location")

            # cols = df.columns[1:]
            # print(df)

            # Instead of blindly grabbing all but first col, select only cols with dtype object
            cols = df.dtypes[df.dtypes == 'object'].index.tolist()[1:   ]
            df[cols] = df[cols].apply(lambda x: x.str.replace(",", "").replace("NR", None))
            df[cols] = df[cols].apply(pd.to_numeric)
            df["total"] = df.iloc[:, 1:].mean(axis=1).round(0)

            # Drop all but last column, to keep the last day of the collection period \
            # to use as snapshot_date
            df = df.drop(list(cols[:-1]), axis=1)

            df.to_csv(o_f, header=True, index=False)
        except Exception as e:
            print(df)
            print(file)
            raise e
