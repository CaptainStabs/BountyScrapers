import pandas as pd
import json
import os
from tqdm import tqdm

folder = '.\\input_files\\'


for file in tqdm(os.listdir(folder)):
    file_path = folder + file
    with open(file_path,'r') as f:
        jf = json.load(f)
    jf = jf[0]


    df = pd.DataFrame(jf['item'])


    df = df.assign(Associated_Codes=df['Associated_Codes'].str.split(',')).explode('Associated_Codes')


    df.rename(columns={
        'payer': 'payer_name',
        'Associated_Codes': 'code',
        'iobSelection': 'setting',
        'Payer_Allowed_Amount': 'standard_charge',
    }, inplace=True)


    df_payer = df.copy()
    df_payer = df_payer[['payer_name', 'description', 'code', 'standard_charge', 'setting']]
    df_payer['payer_category'] = 'payer'


    df_rates = df.copy()
    df_rates = df_rates[['description', 'code', 'setting', 'Avg_Gross_Charge', 'Cash_Discount', 'Deidentified_Min_Allowed', 'DeIdentified_Max_Allowed']]


    cols = df_rates.columns.tolist()
    id_vars = cols[:3]
    value_vars = cols[3:]

    df_rates = pd.melt(df_rates, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')


    mapping = {
        'Avg_Gross_Charge': 'gross',
        'Cash_Discount': 'cash',
        'Deidentified_Min_Allowed': 'min',
        'DeIdentified_Max_Allowed':'max',
        }

    df_rates['payer_category'] = df_rates['payer_name'].map(mapping)


    df = pd.concat([df_payer, df_rates])


    df.reset_index(drop=True, inplace=True)


    df['setting'] = df['setting'].str.lower()


    df.loc[df['code'].str.match(r'^[A-Z][0-9]{4}|[0-9]{5}|[0-9]{4}[A-Z]$'), 'hcpcs_cpt'] = df['code']
    df.loc[df['code'].str.match(r'[0-9]{3}'), 'ms_drg'] = df['code']
    df.loc[df['code'].str.len() == 4, 'rev_code'] = df['code']


    ccns = {'340714535': '360002',
    '340827442': '360041',
    '461382538': '360078',
    '341425870': '360098',
    '341260978': '360123',
    '341567805': '363302',
    '340714612': '360145',
    '340816492': '360192',
    '264827222': '360359',
    '340714461': '361307',
    '340714550': '361308',
    '371848577': '360367'}

    ein = file.split('_')[0]
    id = ccns[ein]

    df['hospital_id'] = id


    df.to_csv('.\\output_files\\' + ein + '_' id + '.csv', index=False)


