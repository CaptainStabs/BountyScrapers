import pandas as pd
import json
import os
from tqdm import tqdm

import pandas as pd
import json
import os
from tqdm import tqdm

folder = '.\\input_files\\'
# file = '341883132_bay-park-hospital_standardcharges.json'

for file in tqdm(os.listdir(folder)):
    with open(folder + file, 'r') as f:
        jd = json.load(f)
        jd = jd[0]['item']


    df = pd.DataFrame(jd)


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
    df_rates = df_rates[['description', 'code', 'setting', 'Gross_Charge', 'Cash_Discount', 'Deidentified_Min_Allowed', 'DeIdentified_Max_Allowed']]


    cols = df_rates.columns.tolist()
    id_vars = cols[:3]
    value_vars = cols[3:]

    df_rates = pd.melt(df_rates, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')


    mapping = {
        'Gross_Charge': 'gross',
        'Cash_Discount': 'cash',
        'Deidentified_Min_Allowed': 'min',
        'DeIdentified_Max_Allowed':'max',
        }

    df_rates['payer_category'] = df_rates['payer_name'].map(mapping)


    df = pd.concat([df_payer, df_rates])


    df.reset_index(drop=True, inplace=True)


    df['setting'] = df['setting'].str.lower()

    df['code'] = df['code'].str.strip()


    df.loc[df['code'].str.match(r'^[A-Z][0-9]{4}$|^[0-9]{5}$|^[0-9]{4}[A-Z]$'), 'hcpcs_cpt'] = df['code']
    df.loc[df['code'].str.match(r'^[0-9]{3}$'), 'ms_drg'] = df['code']
    df.loc[df['code'].str.len() == 4, 'rev_code'] = df['code']


    df.loc[df['standard_charge'] == 'N/A', 'standard_charge'] = pd.NA


    df.dropna(subset='standard_charge', inplace=True)


    id_mapping = {
    '344428256_toledo-copy-hospital_standardcharges.json': '360074',
    '341883132_bay-park-hospital_standardcharges.json': '360259',
    '344446484_defiance-regional-hospital_standardcharges.json': '361328',
    '344428256_toledo-hospital_standardcharges.json': '360068',
    '340898745_fostoria-community-hospital_standardcharges.json': '361318',
    '344430849_memorial-hospital_standardcharges.json': '360156',
    '382796005_charles-and-virginia-hickman-hospital_standardcharges.json': '230005',
    '386108110_coldwater-regional-hospital_standardcharges.json': '230022',
    '381984289_monroe-regional-hospital_standardcharges.json': '230099'}

    hosp_id = id_mapping[file]

    df['hospital_id'] = hosp_id

    out_file = hosp_id + file.split('_')[1] + '.csv'

    out_folder = '.\\output_files\\'

    df.to_csv(out_folder + out_file, index=False)