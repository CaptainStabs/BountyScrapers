import openpyxl
import csv
import pandas as pd
import os
import xlrd
from tqdm import tqdm


for file in tqdm(os.listdir("./input_files/csv_3/")):
    if file.endswith('.xlsx'):
        # open workbook by sheet index,
        # optional - sheet_by_index()
        excel = openpyxl.load_workbook("./input_files/csv_3/" + file)

        # writer object is created
        filename = file.replace(".xlsx", "")

        # select the active sheet
        sheet = excel.active

        # writer object is created
        col = csv.writer(open(f"./input_files/converted/{filename}.csv",
                              'w',
                              newline=""))

        # writing the data in csv file
        for r in sheet.rows:
            # row by row write
            # operation is perform
            col.writerow([cell.value for cell in r])
    elif file.endswith(".xls"):
        xls = pd.ExcelFile("./input_files/" + file)
        df = xls.parse(index_col=None, na_values="", dtype=str)
        filename = file.replace(".xls", "")
        df.to_csv("./input_files/converted/" + filename)
