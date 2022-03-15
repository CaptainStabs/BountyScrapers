import pandas as pd
import os
import traceback as tb
from tqdm import tqdm

# def excel2csv()
directory = "./input_files/"
for file in tqdm(os.listdir(directory)):
    # print(file)
    filename = os.fsdecode(file)
    # print(filename)

    # if filename.endswith(".xls") or filename.endswith(".xlsx"):
    try:
        print(directory + filename)
        df = pd.read_excel(directory + filename, dtype=str)
        df.to_csv(f'./output_files/{filename.strip(".xls")}.csv', index = None,header=True)

    except Exception as e:
        tb.print_exc()
        print("ERRPR: ", filename, e)
