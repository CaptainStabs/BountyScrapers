import pandas as pd
import os
import polars as pl
from tqdm import tqdm

folder = '.\\input_files\\'
# file = '231352191_Mercy Catholic Medical Center of Southeastern Pennsylvania_standardcharges .xlsx'


for file in tqdm(os.listdir(folder)):
    df = pd.read_excel(folder + file)


    # Find the index of the row that starts with 'Code'
    code_index = df.index[df.iloc[:, 0] == 'Code'][0]

    # Set the header to the values in the 'Code' row
    df.columns = df.iloc[code_index]

    # Drop the 'Code' row, which is now redundant with the header
    df = df.drop(code_index)

    # Reset the index to start from 0
    df = df.reset_index(drop=True)


    # Drop completely empty rows
    df.dropna(how='all', inplace=True)



    df.rename(columns={
        'Code': 'code',
        'Description': 'description',
        'Type': 'setting',
    }, inplace=True)


    df.drop('Derived contracted rate', axis=1, inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:3]
    value_vars = cols[3:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')


    df.dropna(subset='standard_charge', inplace=True)


    df['payer_name'] = df['payer_name'].str.replace('__Derived Contracted Rate', '')


    mapping = {
        'Gross Charge': 'gross',
        'Discounted Cash Price': 'cash',
        'De-identified min contracted rate': 'min',
        'De-identified max contracted rate': 'max'
    }

    df['payer_category'] = df['payer_name'].map(mapping).fillna('payer')


    df['code'] = df['code'].astype(str)


    df['setting'] = df['setting'].str.lower()

    df['code'] = df['code'].astype(str)


    df.loc[df['code'].str.len() == 1, 'ms_drg'] = df['code'].str.zfill(3)
    df.loc[df['code'].str.len() == 3, 'ms_drg'] = df['code']
    df.loc[df['code'].str.match(r'\d{3}X'), 'ms_drg'] = df['code'].str.strip('X')
    df.loc[df['code'].str.len() == 5, 'hcpcs_cpt'] = df['code']


    ccns = {'38-3176536': '230029',
    '383175878': '230156',
    '383176225': '230069',
    '383176536': '230029',
    '824757260': '230259',
    '383521763': '230002',
    '382589966': '230066',
    '231352191': '390156',
    '510064326': '070002',
    '232794121': '390204',
    '231913910': '390258'}

    ein = file.split('_')[0]

    if ein == '382589966':
        if 'Shelby' in file:
            id = '231320'
        elif 'Muskegon' in file:
            id = '230066'
    else:
        id = ccns[ein]

    df['hospital_id'] = id


    df['description'] = df['description'].str.strip()

    pattern = r'^[A-Z][0-9]{4}|[0-9]{5}|[0-9]{4}[A-Z]$'

    df['hcpcs_cpt'] = df['hcpcs_cpt'].astype(str)
    mask = df['hcpcs_cpt'].str.match(pattern)
    df.loc[~mask, 'hcpcs_cpt'] = pd.NA

    # df['ms_drg'].fillna('', inplace=True)
    # df['hcpcs_cpt'].fillna('', inplace=True)
    # df['code'].fillna('', inplace=True)

    df = pl.from_pandas(df)

    df.write_csv('.\\output_files\\' + ein + '.csv')
