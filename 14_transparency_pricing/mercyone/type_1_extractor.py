import pandas as pd
import os
from tqdm import tqdm

folder = '.\\input_files\\'

# file = '420680448_mercyone-des-moines-medical-center_standardcharges.xlsx'

for file in tqdm(os.listdir(folder)):
    print('\n', file)
    if 'other_schema' in file:
        continue
    file_path = folder + file
    
    if file.endswith('.xlsx'):
        df = pd.read_excel(file_path, dtype=str, skiprows=4)

    elif file == '421470935_mercyone-newton-medical-center_standardcharges.csv':
        df = pd.read_csv(file_path, dtype=str, skiprows=3)
    elif file.endswith('.csv'):
        try:
            df = pd.read_csv(file_path, dtype=str, skiprows=4)
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, dtype=str, skiprows=4, encoding='ansi')

    # df.rename(columns=lambda x: x.strip(), inplace=True)
    df.rename(columns={
        'Code': 'code',
        'Description': 'description',
        'Code Type': 'line_type',
        'Revenue Code (RC)': 'rev_code'
    }, inplace=True)


    df.drop(df.tail(9).index, inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:4]
    value_vars = cols[4:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')


    df.loc[df['rev_code'] == 'No RC', 'rev_code'] = pd.NA
    df.loc[(df['standard_charge'] == '*') | (df['standard_charge'] == 'IP') | (df['standard_charge'] == '**') | (df['standard_charge'] == '***'), 'standard_charge'] = pd.NA


    df.dropna(subset='standard_charge', inplace=True)


    mask = (~df['standard_charge'].isna() & df['standard_charge'].str.contains('%'))
    df.loc[mask, 'standard_charge_percent'] = df['standard_charge'].str.split('%').str[0]


    df.loc[~df['standard_charge_percent'].isna(), ['standard_charge', 'contracting_method']] = (pd.NA, 'percent of total billed charge')


    df.loc[df['line_type'].str.match(r'HCPCS|CPT'), 'hcpcs_cpt'] = df['code']
    df.loc[df['line_type'] == 'MS-DRG', 'ms_drg'] = df['code'].str.zfill(3)


    mask = df['line_type'] == 'APR-DRG'
    df.loc[mask & (df['code'].str.len() <= 3), 'apr_drg'] = df['code'].str.zfill(3)

    df.loc[mask & (df['code'].str.len() == 4), 'apr_drg'] = df['code'].str[:3] + '-' + df['code'].str[3:]

    mask = df['ms_drg'].str.len() == 4
    # df.loc[mask, 'apr_drg'] = df['ms_drg']
    df.loc[mask, 'code'] = df['ms_drg']
    df.loc[mask, 'ms_drg'] = df['ms_drg'].str[:3]

    df.loc[df['hcpcs_cpt'].str.len() == 3, 'hcpcs_cpt'] = pd.NA

    mask = df['hcpcs_cpt'].astype(str).str.match(r'^[A-Z][0-9]{4}$|^[0-9]{5}$|^[0-9]{4}[A-Z]$|nan')
    df.loc[~mask, 'hcpcs_cpt'] = pd.NA

    df['standard_charge'] = df['standard_charge'].str.lower()
    mask = (~df['standard_charge'].isna()) & (df['standard_charge'].str.contains(' per diem'))
    df.loc[mask, 'contracting_method'] = 'per diem'
    df.loc[mask, 'standard_charge'] = df['standard_charge'].str.split(' ').str[0]


    df.loc[df['standard_charge'] == '4364140000000', 'standard_charge'] = pd.NA

    df.loc[df['description'] == 'NO ACTIVE CODE DESCRIPTION', 'description'] = pd.NA


    mapping = {
        'Gross Charge': 'gross',
        'Discounted Cash Price': 'cash',
        'De-Identified Minimum Negotiated Charge': 'min',
        'De-Identified Maximum Negotiated Charge': 'max'
    }

    df['payer_category'] = df['payer_name'].map(mapping).fillna('payer')


    df['plan_name'] = pd.NA


    df.loc[df['payer_name'].str.contains('|', regex=False), 'plan_name'] =  df['payer_name'].str.split('| ', regex=False).str[-1]

    df['rev_code'] = df['rev_code'].str.zfill(4)


    mapping = {'421470935_mercyone-newton-medical-center_standardcharges.csv': '160032',
    '420758901_MercyOne Cedar Falls Medical Center_standardcharges.xlsx': '160040',
    '311373080_Mercy Medical Center North Iowa_standardcharges.xlsx': '160064',
    '421264647_MercyOne Waterloo Medical Center_standardcharges.xlsx': '160067',
    '421437483_Mercy Medical Center Dubuque_standardcharges.xlsx': '160069',
    '421336618_Mercy Medical Center Clinton_standardcharges.xlsx': '160080',
    '420680448_mercyone-des-moines-medical-center_standardcharges.xlsx': '160083',
    '311407377_Mercy Medical Center Siouxland_standardcharges.xlsx': '160153',
    '421500277_MercyOne Primghar Medical Center_standardcharges.xlsx': '161300',
    '420818642_MercyOne Elkader Medical Center_standardcharges.xlsx': '161319',
    '421178403_MercyOne Oelwein Medical Center_standardcharges.xlsx': '161338',
    '420680308_mercyone-centerville-medical-center_standardcharges.csv': '161377',
    '202552602_Mercy Medical Center Dyersville_standardcharges.xlsx': '161378'}

    hospital_id = mapping[file]
    df['hospital_id'] = hospital_id


    output_folder = '.\\output_files\\'
    df.to_csv(output_folder + hospital_id + "_" + file.split('_')[1].replace(' ', '_') + '.csv', index=False)


