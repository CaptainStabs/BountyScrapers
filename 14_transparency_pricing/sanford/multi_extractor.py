import pandas as pd
import json
import os
from tqdm import tqdm

folder = '.\\input_files\\'


for file in tqdm(os.listdir(folder)):
    print('\n' + file)
    if '.json' not in file:
        continue
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

    df['code'] = df['code'].str.strip()
    df_payer = df.copy()
    df_payer = df_payer[['payer_name', 'description', 'code', 'standard_charge', 'setting']]
    df_payer['payer_category'] = 'payer'


    df_rates = df.copy()
    try:
        df_rates = df_rates[['description', 'code', 'setting', 'Avg_Gross_Charge', 'Cash_Discount_Price', 'Deidentified_Min_Allowed', 'DeIdentified_Max_Allowed']]
    except KeyError:
        df_rates = df_rates[['description', 'code', 'setting', 'Avg_Gross_Charge', 'Cash_Discount', 'Deidentified_Min_Allowed', 'DeIdentified_Max_Allowed']]


    cols = df_rates.columns.tolist()
    id_vars = cols[:3]
    value_vars = cols[3:]

    df_rates = pd.melt(df_rates, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')


    mapping = {
        'Avg_Gross_Charge': 'gross',
        'Cash_Discount': 'cash',
        'Cash_Discount_Price': 'cash',
        'Deidentified_Min_Allowed': 'min',
        'DeIdentified_Max_Allowed':'max',
        }

    df_rates['payer_category'] = df_rates['payer_name'].map(mapping)


    df = pd.concat([df_payer, df_rates])


    df.reset_index(drop=True, inplace=True)


    df['setting'] = df['setting'].str.lower()


    df.loc[(df['code'].str.match(r'^[A-Z][0-9]{4}|[0-9]{5}|[0-9]{4}[A-Z]$')) & (df['code'].str.len() == 5), 'hcpcs_cpt'] = df['code']
    df.loc[df['code'].str.match(r'^[0-9]{3}$'), 'ms_drg'] = df['code']
    df.loc[df['code'].str.len() == 4, 'apr_drg'] = df['code'][:2] + '-' + df['code'][2:]
    df['apr_drg'] = df['code'].apply(lambda x: x[:3] + '-' + x[-1] if len(str(x)) == 4 else pd.NA)
    df.loc[df['code'].str.len() == 2, 'apr_drg'] = df['code'].str.zfill(3)


    ccns = {
        '460388596_sanford-sheldon-medical-center_standardcharges.json': '161381',
        '460388596_sanford-worthington-medical-center_standardcharges.json': '240022',
        '460388596_sanford-tracy-hospital_standardcharges.json': '241303',
        '460388596_sanford-canby-medical-center_standardcharges.json': '241347',
        # '450409348_sanford-thief-river-falls-medical-center_standardcharges.json': '241381',
        '450409348_sanford-medical-center-mayville_standardcharges.json': '351309',
        '460388596_sanford-aberdeen-medical-center_standardcharges.json': '430097',
        '460388596_sanford-canton-inwood-medical-center_standardcharges.json': '431333',
        '460388596_sanford-vermillion-hospital_standardcharges.json': '431336',
        # '450409348_sanford-thief-river-falls-medical-center_standardcharges.json_': '244018',
        '460388596_sanford-luverne-medical-center_standardcharges.json': '240128',
        '460388596_sanford-westbrook-hospital_standardcharges.json': '241302',
        '450409348_sanford-wheaton_standardcharges.json': '241304',
        '460388596_sanford-jackson-hospital_standardcharges.json': '241315',
        '411266009_sanford-bagley-medical-center_standardcharges.json': '241328',
        '450409348_sanford-medical-center-hillsboro_standardcharges.json': '351329',
        '460388596_sanford-clear-lake-medical-center_standardcharges.json': '431307',
        '460388596_sanford-hospital-webster_standardcharges.json': '431311',
        '460388596_sanford-chamberlain-medical-center_standardcharges.json': '431329'
    }


    if file == '450409348_sanford-thief-river-falls-medical-center_standardcharges.json':
        df1 = df.copy()
        df2 = df.copy()
        df2['hospital_id'] = '241381'
        df1['hospital_id'] = '244018'

        id = '241381'
        df = pd.concat([df1, df2])
    
    else:
        ein = file.split('_')[0]
        id = ccns[file]

        df['hospital_id'] = id

    df['standard_charge'] = pd.to_numeric(df['standard_charge'], errors='coerce')

    df.dropna(subset='standard_charge', inplace=True)

    df.to_csv('.\\output_files\\' + ein + '_' + id + '.csv', index=False)


