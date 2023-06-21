import polars as pl
import os
from tqdm import tqdm


folder = '.\\input_excel\\'

for file in tqdm(os.listdir(folder)):
    print('\n', file)
    df = pl.read_excel(folder + file)
    df.write_csv('input_files\\' + file.replace('.xlsx', '.csv'))
