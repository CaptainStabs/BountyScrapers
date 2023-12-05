import os
import pandas as pd
from tqdm import tqdm

folder = '.\\input_files\\'

# file = '431704371_Freeman-Health-System_standardcharges.csv'


for file in tqdm(os.listdir(folder)):
    df = pd.read_csv(folder + file, dtype=str)


    # Find the index of the first entirely blank row
    blank_row_index = df.index[df.isnull().all(axis=1)].min()

    # Slice the DataFrame to keep only the rows before the blank_row_index
    df = df.iloc[:blank_row_index]


    # df.drop(columns='Package/Line_Level', inplace=True)


    df.rename(columns={
        'Code': 'code',
        'Description': 'description',
        'Type': 'setting',
        'Package/Line_Level': 'line_type'
    }, inplace=True)


    cols  = df.columns.tolist()
    id_vars = cols[:4]
    val_vars = cols[4:]

    df = pd.melt(df, id_vars=id_vars, value_vars=val_vars, var_name='payer_name', value_name='standard_charge')


    df.dropna(subset='standard_charge', inplace=True)

    df.loc[df['code'].str.match(r'^[A-Z][0-9]{4}$|^[0-9]{5}$|^[0-9]{4}[A-Z]$'), 'hcpcs_cpt'] = df['code']


    df.loc[df['code'].str.len() <= 3, 'ms_drg'] = df['code'].str.zfill(3)


    df.loc[df['code'].str.match(r'\d{3}X'), 'apr_drg'] = df['code'].str.replace('X', '')


    payer_mapping = {
        'Gross charge': 'gross',
        'Discounted cash price': 'cash',
        'De-identified min contracted rate': 'min',
        'De-identified max contracted rate': 'max'
    }

    df['rate_category'] = df['payer_name'].map(payer_mapping).fillna('negotiated')

    df['setting'] = df['setting'].str.lower()


    id_mapping = {
        '431240629_Freeman-Neosho-Hospital_standardcharges.csv': '261331',
        '431704371_Freeman-Health-System_standardcharges.csv': '260137'
    }

    hosp_id = id_mapping[file]
    df['hospital_id'] = hosp_id

    output_folder = '.\\output_files\\'
    df.to_csv(output_folder + hosp_id + '_' + file.split('_')[1] + '.csv', index=False)


