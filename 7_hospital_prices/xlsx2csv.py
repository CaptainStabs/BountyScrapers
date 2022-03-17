import openpyxl
import csv
import pandas as pd
import os


for file in os.listdir("./"):
    if file.endswith('.xlsx'):
        # open workbook by sheet index,
        # optional - sheet_by_index()
        excel = openpyxl.load_workbook(file)

        # writer object is created
        filename = file.replace(".xlsx", "")

        # select the active sheet
        print(dir(excel))
        sheet = excel.active

        # writer object is created
        col = csv.writer(open(f"{filename}.csv",
                              'w',
                              newline=""))

        # writing the data in csv file
        for r in sheet.rows:
            # row by row write
            # operation is perform
            col.writerow([cell.value for cell in r])
