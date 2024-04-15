import pandas as pd
import os
from tqdm import tqdm
import polars as pl


folder = ".\\input_files\\other_format\\"
for file in tqdm(os.listdir(folder)):

    df = pd.read_excel(folder + file, skiprows=5)


    df_copy = df.copy()


    df.rename(columns={
        'Charge Description Master': 'description',
        'Revenue Code': 'rev_code',
        'CPT/HCPCS': 'code'
    }, inplace=True)

    df['rev_code'] = df['rev_code'].astype(str)

    df['rev_code'] = df['rev_code'].str.split('.').str[0]
    df.loc[df['rev_code'] == 'nan', 'rev_code'] = ''



    cols = df.columns.tolist()
    id_vars = cols[:3]
    value_vars = cols[3:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer', value_name='standard_charge')


    df.loc[df['standard_charge'] == 'NA*', 'standard_charge'] = pd.NA
    df.dropna(subset='standard_charge', inplace=True)


    df['payer'] = df['payer'].str.replace('Negotiated Charge', '')


    df['code'] = df['code'].str.strip()


    df.loc[df['code'].str.len() > 6, 'modifiers'] = df['code'].str[-2:]
    df.loc[df['code'].str.len() > 6, 'hcpcs_cpt'] = df['code'].str[:-2]
    df.loc[df['code'].str.len() == 5, 'hcpcs_cpt'] = df['code']



    mapping = {
        'Discounted Cash Price*': 'cash',
        'De-Identified Minimum Negotiated Charge': 'min',
        'De-Identified Maximum Negotiated Charge': 'max',
        'De-Identified Maximum': 'max',
        'De-Identified Minimum': 'min',
        'Gross Charges': 'gross'
    }

    df['payer'] = df['payer'].str.strip()
    df['payer_category'] = df['payer'].map(mapping).fillna('payer')


    non_null_cols = ['code', 'modifiers', 'hcpcs_cpt', 'rev_code']
    # Have to convert them to string first, which converts nulls to nan
    df[non_null_cols] = df[non_null_cols].astype(str)

    df.loc[df['code'] == 'nan', 'code'] = ''
    df.loc[df['hcpcs_cpt'] == 'nan', 'hcpcs_cpt'] = ''
    df.loc[df['modifiers'] == 'nan','modifiers'] = ''
    df.loc[df['rev_code'] == 'nan','rev_code'] = ''

    df.loc[df['rev_code'].str.len() < 4, 'rev_code'] = df['rev_code'].str.zfill(4)

    df['standard_charge'] = pd.to_numeric(df['standard_charge'], errors='coerce')
    df.dropna(subset='standard_charge', inplace=True)

    ccn = {
        '521369749': '093025',
        '522218584': '090004'
    }

    ein = file.split('_')[0]
    df['hospital_id'] = ccn[ein]

    df = pl.from_pandas(df)
    df.write_csv('.\\output_files\\other_format\\' + ein + '.csv')


