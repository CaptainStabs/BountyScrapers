import pandas as pd
import os
import re
from tqdm import tqdm
import polars as pl

pattern = r"^[A-Z][0-9]{4}|[0-9]{5}|[0-9]{4}[A-Z]$"

def payer_category(x):
    payers = {
        'Charge': 'gross',
        'Self Pay Price': 'cash',
        'Min Negotiated Rate': 'min',
        'Max Negotiated Rate': 'max',
    }

    try:
        return payers[x]
    except KeyError:
        return 'payer'


folder = '.\\input_files\\'

for file in tqdm(os.listdir(folder)):
    df = pd.read_excel(folder + file)


    df.rename(columns={
        'Code': 'code',
        'Desc.': 'description'
    }, inplace=True)


    cols = df.columns.tolist()
    id_vars = ['code', 'description']
    value_vars = cols[3:]
    value_vars.append('Charge')

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer', value_name= 'standard_charge')


    df.dropna(subset=['standard_charge'], inplace=True)


    df.loc[df['code'].str.len() == 5, 'hcpcs_cpt'] = df['code']


    df['payer_category'] = df['payer'].apply(payer_category)


    ccn = {
        '540519577': '490022',
        '134316364': '490140'
    }

    ein = file.split('_')[0]
    df['hospital_id'] = ccn[ein]

    # df['hcpcs_cpt'].fillna('""', inplace=True)
    # df['code'].fillna('""', inplace=True)

    df['hcpcs_cpt'] = df['hcpcs_cpt'].astype(str)
    # df.loc[df['hcpcs_cpt'].str.contains(pattern), 'hcpcs_cpt'] = '""'
    mask = ~df['hcpcs_cpt'].str.contains(pattern)
    df.loc[mask, 'hcpcs_cpt'] = '' # '""'
    df.loc[df['hcpcs_cpt'].str.contains('-'), 'hcpcs_cpt'] = pd.NA # '""'

    df['code'] = df['code'].str.strip()
    df['code'] = df['code'].apply(lambda x: str(x).zfill(3) if len(str(x)) < 3 else x)

    df['apr_drg'] = ''
    df.loc[df['code'].str.contains('-') & ~df['code'].isna(), 'apr_drg'] = df['code']

    df['ms_drg'] = ''
    df.loc[df['code'].str.len() == 3, 'ms_drg'] = df['code']

    df['code'].fillna('', inplace=True)

    # df.loc[df['ms_drg'] == '', 'ms_drg'] = '""'
    # df.loc[df['apr_drg'] == '', 'apr_drg'] = '""'

    # df = df.astype(str)

    # columnsList = ['code', 'hcpcs_cpt', 'apr_drg', 'ms_drg']
    # for col in columnsList:
    #     df[col] =  df[col].apply(lambda x: '"' + str(x) + '"' if x != 'nan' else '""')
    # import csv
    # df.to_csv(file.split('_')[0] + '.csv', index=False, quoting=csv.QUOTE_NONE, escapechar='\\')
    df.to_csv(file.split('_')[0] + '.csv', index=False, na_rep='""')
    # df = pl.from_pandas(df)
    # df.write_csv(file.split('_')[0] + '.csv')


