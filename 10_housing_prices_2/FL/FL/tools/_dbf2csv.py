import csv
import dbf
import os
from tqdm import tqdm

def dbf_to_csv(table_in, table_out):
    with dbf.Table(table_in) as current_file:
        dbf.export(current_file, filename=table_out)


directory = ".\\DBF\\"

for root, dirs, files in os.walk(directory):
    for file in tqdm(files):
        dir = file.replace(".dbf", "")

        if file.endswith('.dbf'):
            print("\\".join([root, file]))
            dbf_to_csv("\\".join([root, file]), root + "csv\\" + file.replace(".dbf", ".csv"))
