import pandas as pd
import os
import traceback as tb
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

sheets = ["Charge Description Master", "Medication", "Supply"]
save_folder = ["\\CDM\\", "\\meds\\", "\\supply\\"]

# def excel2csv()
directory = ".\\input_files\\"
for file in tqdm(os.listdir(directory)):
    # print(file)
    filename = os.fsdecode(file)
    # print(filename)

    try:
        if filename.endswith(".xls") or filename.endswith(".xlsx"):
            for i, sheet in enumerate(sheets):
                # print(file)
                filename = os.fsdecode(file)
                # print(filename)

                try:
                    if filename.endswith(".xls") or filename.endswith(".xlsx"):
                        for i, sheet in enumerate(sheets):
                            df = pd.read_excel(directory + "\\" + filename, sheet_name=sheet, dtype=str)
                            df.to_csv(f'.\\output_files{save_folder[i]}\\{filename[9:].strip(".xls").strip(".xlsx").lstrip("-")}_{sheet.replace(" ", "")}.csv', index = None,header=True)

                except Exception as e:
                    tb.print_exc()
                    print("ERRPR: ", filename, e)
    except Exception as e:
        tb.print_exc()
        print("ERRPR: ", filename, e)
