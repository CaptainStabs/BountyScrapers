import csv
import dbf
import os
from tqdm import tqdm

def dbf_to_csv(table_in, table_out):
    with dbf.Table(table_in) as current_file:
        dbf.export(current_file, filename=table_out)


directory = "F:\\___FL\\dbf\\"

for root, dirs, files in os.walk(directory):
        # print(files)
        for file in tqdm(files):
            if file.endswith('.dbf'):
                # print(root + file)
                dbf_to_csv((root + file), root + "csv\\" + file.replace(".dbf", ".csv"))
