import os
import pandas as pd
from tqdm import tqdm

folder = '.\\other_input_files\\'
for file in tqdm(os.listdir(folder)):
    df = pd.read_csv(folder + file, dtype=str)


    # # Find the index of the first entirely blank row
    # blank_row_index = df.index[df.isnull().all(axis=1)].min()

    # # Slice the DataFrame to keep only the rows before the blank_row_index
    # df = df.iloc[:blank_row_index]


    # # df.drop(columns='Package/Line_Level', inplace=True)


    df.rename(columns={
        'Code': 'code',
        'Description': 'description',
        'Price': 'standard_charge'
    }, inplace=True)

    df['rate_category'] = 'gross'
    df['payer_name'] = 'Price'

    id_mapping = {
        '431240629.csv': '261331',
        '431704371.csv': '260137'
    }

    hosp_id = id_mapping[file]
    df['hospital_id'] = hosp_id

    output_folder = '.\\output_files\\'
    df.to_csv(output_folder + hosp_id + file, index=False)


