import json
import pandas as pd
import os
from tqdm import tqdm


folder = '.\\input_files\\'

for file in tqdm(os.listdir(folder)):
    with open(folder + file, 'r') as f:
        jf = json.load(f)


    cols = jf['Headers']
    data = jf['Data']
    del jf

    df = pd.DataFrame(columns=cols, data=data)

    df.rename(columns={
        'Identifier_Description': 'description',
        'Identifier_Code': 'local_code',
        'Billing_Code': 'code'
    }, inplace=True)


    df.drop('Site', axis=1, inplace=True)


    df['local_code'] = df['local_code'].replace("", pd.NA)
    df['code'] = df['code'].replace("", pd.NA)


    cols = df.columns.tolist()
    id_vars = cols[:3]
    value_vars = cols[3:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')


    df['standard_charge'] = df['standard_charge'].replace('', pd.NA)
    df['standard_charge'] = df['standard_charge'].str.replace(',', '')


    df.dropna(subset='standard_charge', inplace=True)


    mapping = {
        'Charge': 'gross',
        'De-identified Maximum': 'max',
        'De-identified Minimum': 'min',
        'Discounted Cash Price': 'cash',   
    }

    df['payer_category'] = df['payer_name'].map(mapping).fillna('payer')


    df.loc[~df['code'].isna()]


    df.loc[(~df['code'].isna()) & (df['code'].str.contains('APR DRG')), 'apr_drg_temp'] = df['code']
    df.loc[~df['apr_drg_temp'].isna(), 'apr_drg_temp'] = df['apr_drg_temp'].str.replace('APR DRG ', '')
    df.loc[~df['apr_drg_temp'].isna(), 'apr_drg'] = df['apr_drg_temp'].str[:3] + '-' + df['apr_drg_temp'].str[-1]
    df.drop('apr_drg_temp', axis=1, inplace=True)



    df.loc[(~df['code'].isna()) & (df['code'].str.match(r'^[A-Z][0-9]{4}|[0-9]{5}|[0-9]{4}[A-Z]$')), 'hcpcs_cpt'] = df['code']


    ccn = {'11-1667761_South Shore University Hospital_StandardCharges.json': '330043',
    '11-1630914_Huntington Hospital_StandardCharges.json': '330045',
    '11-1562701_North Shore University Hospital_StandardCharges.json': '330106',
    '11-1661359_Peconic Bay Medical Center_StandardCharges.json': '330107',
    '13-1624070_Lenox Hill Hospital_StandardCharges.json': '330119',
    '11-2868878_Staten Island University Hospital_StandardCharges.json': '330160',
    '13-1740118_Northern Westchester Hospital_StandardCharges.json': '330162',
    '11-1633487_Glen Cove Hospital_StandardCharges.json': '330181',
    '11-1639818_Mather Memorial Hospital_StandardCharges.json': '330185',
    '11-2241326_Long Island Jewish Hospital_StandardCharges.json': '330195',
    '13-1725076_Phelps Memorial Hospital Center_StandardCharges.json': '330261',
    '11-3241243_Plainview Hospital_StandardCharges.json': '330331',
    '11-2241326_Long Island Jewish Forest Hills_StandardCharges.json': '330353',
    '11-2241326_Long Island Jewish Valley Stream_StandardCharges.json': '330372',
    '11-1562701_Syosset Hospital_StandardCharges.json': '330398'}


    id = ccn[file]

    df['hospital_id'] = id

    output_name = file.split('_')[0] + '_' + id + '.csv'
    df.to_csv('.\\output_files\\' + output_name, index=False)


