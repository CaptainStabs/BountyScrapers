import pandas as pd
import os
import traceback as tb
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
# import heartrate; heartrate.trace(browser=True, daemon=True)

sheets = ["Charge Description Master", "Medication", "Supply"]
save_folder = ["\\CDM\\", "\\meds\\", "\\supply\\"]

def excel2csv(file, directory):
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


def runner(sheets, save_folder):
    threads = []
    directory = ".\\input_files\\"
    with ProcessPoolExecutor(max_workers=5) as executor:
        for file in tqdm(os.listdir(directory)):
            # print(threads)
            threads.append(executor.submit(excel2csv(file, directory)))

if __name__ == '__main__':
    runner(sheets, save_folder)
