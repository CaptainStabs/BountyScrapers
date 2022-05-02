import PyPDF2
import tabula
import pandas as pd
import polars as pl
import os
from tqdm import tqdm

in_dir = "./pdfs/"
out_dir = "./csvs/"
years = []
pages = []
for file in tqdm(os.listdir(in_dir)):
    # print(file)
    f = file.replace(".pdf", ".csv")
    i_f = os.path.join(in_dir, file)
    o_f = os.path.join(out_dir, f)
    p = PyPDF2.PdfFileReader(open(i_f, 'rb'))
    # print(file.split()[-1][:-4])
    # years.append(file.split()[-1][:-4])
    years.append(file)
    pages.append(p.numPages)

df = pd.DataFrame(zip(years, pages))
df.columns = ['years', 'pages']
df = df.drop_duplicates('pages')
df = df.groupby('years')

print(df.apply(print))
