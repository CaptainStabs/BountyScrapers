from pyxlsb import open_workbook
import pandas as pd
import os


directory = ".\\files\\"
for file in os.listdir(directory):
    print(file)
    filename = os.fsdecode(file)
    print(filename)

    try:
        if filename.endswith(".xls") or filename.endswith(".xlsx"):
            df = pd.read_excel(directory + "\\" + filename, sheet_name=None)
            for key in df.keys():
                df[key].to_csv(f'.\\input_files\\{filename.strip(".xls").strip(".xlsx")}.csv')

    except Exception as e:
        print("ERRPR: ", filename, e)
