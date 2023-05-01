import pandas as pd
import polars as pl
import os
from tqdm import tqdm


folder = '.\\input_files\\'

for file in tqdm(os.listdir(folder)):

    df = pd.read_csv(folder + file, dtype=str)


    df.rename(columns={
        'Record ID': 'local_code',
        'Description': 'description',
        'CPT/DRG': 'code',
    }, inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:3]
    value_vars = cols[3:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer', value_name='standard_charge')


    df.loc[df['code'].str.len() == 3, 'ms_drg'] = df['code']
    df.loc[df['code'].str.len() == 5, 'hcpcs_cpt'] = df['code']


    df['payer'] = df['payer'].str.strip()


    mapping = {
        'Gross Charge': 'gross',
        'Self Pay': 'cash',
        'Min Payment': 'min',
        'Max Payment': 'max'
    }

    df['payer_category'] = df['payer'].map(mapping).fillna('payer')


    df['standard_charge'] = df['standard_charge'].str.replace('\$|,|\(|\)', '', regex=True)


    df['standard_charge'] = df['standard_charge'].astype(float)


    df['ms_drg'].fillna('', inplace=True)
    df['hcpcs_cpt'].fillna('', inplace=True)
    df['code'].fillna('', inplace=True)
    df['local_code'].fillna('', inplace=True)

    df.loc[df['payer'].str.contains('All Plans'), 'plan'] = 'all plans'
    df['payer'] = df['payer'].str.replace(' (All Plans) Payment', '')
    df['payer'] = df['payer'].str.replace(' Payment', '')
    df['payer'] = df['payer'].str.replace(' (All Plans)', '')
    df['payer'] = df['payer'].str.strip().str.strip()

    df.loc[df['plan'].isna(), 'plan'] = ''

    if 'Bethlehem' in file:
        id = '390049'
    elif 'Lehighton' in file:
        id = '390335'

    else:
        ccn = {
            '844475996': '390162',
            '824432109': '390332',
            '465143606': '390330',
            '454394739': '390326',
            '251550350': '390183',
            # '231352213': '390049',
            # '231352213': '390335',
            '231352203': '390035',
            '221494454': '310060'
        }

        ein = file.split('_')[0]
        id = ccn[ein]
    
    df['hospital_id'] = id

    df.dropna(subset='standard_charge', inplace=True)

    df1 = pl.from_pandas(df)
    df1.write_csv('.\\output_files\\' + file.split('_')[1] + '.csv')


