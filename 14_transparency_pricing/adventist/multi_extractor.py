import pandas as pd
import numpy as np
import polars as pl
import os
from tqdm import tqdm



folder = '.\\input_files\\'

dtypes = {
    'Procedure Code': str, 
    'Revenue Code': str, 
    'Modifier1': str,
    'Modifier2': str,   
    'Rx Unit Multiplier': str 
}

for file in tqdm(os.listdir(folder)):
    df = pd.read_csv(folder + file, dtype=dtypes, skiprows=3)



    df.rename(columns={
        'Procedure Code': 'local_code',
        'Procedure Description': 'description',
        'Price Tier': 'setting',
        'Revenue Code': 'rev_code',
        'CPT HCPCS Code': 'code',
        'NDC Code': 'ndc',
        'Rx Unit Multiplier': 'drug_hcpcs_multiplier'
        
    }, inplace=True)


    df = df[~df['local_code'].isin(['Diagnosis Related Group Code', 'Shoppable Services Code'])]


    cols = df.columns.tolist()
    id_vars = cols[:9]
    value_vars = cols[9:]


    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer', value_name='rate')


    df['ndc'].fillna(pd.NA, inplace=True)


    mapping = {
        'Gross Charge': 'gross',
        'Discounted Cash Price': 'cash',
        'De-identified minimum negotiated charge': 'min',
        'De-identified maximum negotiated charge': 'max'
    }

    df['payer_category'] = df['payer'].map(mapping).fillna('payer')


    df['plan'] = ''
    df['plan'] = np.where(df['payer'].str.contains('ALL_PAYER_-_ALL_OTHER_PLANS'), 'ALL PAYER - ALL OTHER PLANS',
                        np.where(df['payer'].str.contains('ALL_OTHER_PLANS'), 'ALL OTHER PLANS',
                                np.where(df['payer'].str.contains('ALL_PLANS'), 'ALL PLANS', df['plan'])))


    df['payer'] = df['payer'].str.replace('ALL_PAYER_-_ALL_OTHER_PLANS|ALL_PLANS|ALL_OTHER_PLANS', '', regex=True).str.strip('-_')


    df.loc[df['drug_hcpcs_multiplier'] == '0', 'drug_hcpcs_multiplier'] = pd.NA


    df['modifiers'] = df['Modifier1'] + df['Modifier2']
    df.drop(['Modifier1', 'Modifier2'], axis=1, inplace=True)


    cols = ['setting', 'code', 'ndc', 'local_code', 'plan', 'modifiers']
    df[cols] = df[cols].astype(str)
    df.loc[:, cols].fillna('', inplace=True)


    df['setting'].fillna('', inplace=True)


    df['rate'] = df['rate'].astype(float)


    df.loc[df['code'].str.match(r'^\d{3}$'), 'ms_drg'] = df['code']


    df.loc[df['ndc'].isin(['<NA>', 'nan']), 'ndc'] = ''
    df.loc[df['setting'].isin(['<NA>', 'nan']),'setting'] = ''
    df.loc[df['modifiers'].isin(['<NA>', 'nan']),'modifiers'] = ''

    df['ms_drg'].fillna('', inplace=True)
    df['rev_code'].fillna('', inplace=True)

    df['drug_hcpcs_multiplier'].fillna(pd.NA, inplace=True)

    
    ein = file.split('_')[0]

    if file == '812240617_adventist-health---tehachapi-valley_standardcharges.csv':
        df['hospital_id'] = '051301'
    elif file == '812240617_adventist-health-ukiah-valley_standardcharges.csv':
        df['hospital_id'] = '051302'
    elif file == '941279779_adventist-health---st.-helena_standardcharges.csv':
        df1 = df
        df1['hospital_id'] = '054074'
        df['hospital_id'] = '050013'
        df = pd.concat([df, df1])

    else:
        ccn = {
        '941387866': '050133',
        '952294234': '050455',
        '990107330': '120006',
        '680395149': '051317',
        '611823825': '050608',
        '940535360': '050121',
        '680108919': '051310',
        '941044474': '050336',
        '930429015': '380060',
        '453220509': '050192',
        '941415069': '050335',
        '941279779': '054074',
        '812240617': '050301',
        '951816017': '050239',
        '952627981': '051325',
        '956064971': '050236',
        '952282647': '050103',
        '930622075': '381317'
    }
        df['hospital_id'] = ccn[ein]

    if '---' in file:
        output_file = file.split('---')[-1].replace('standardcharges', '')
    else:
        output_file = file.replace('standardcharges', '')

    df = pl.from_pandas(df)
    df.write_csv('.\\output_files\\' + output_file)

