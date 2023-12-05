import os
import pandas as pd
from tqdm import tqdm

folder = '.\\input_files\\'

for file in tqdm(os.listdir(folder)):
    df = pd.read_excel(folder + file, dtype=str, skiprows=1, sheet_name='Chargemaster')


    df.columns

    df.drop(columns='Location', inplace=True)


    df.rename(columns={
        'Code Type ': 'line_type',
        'Code Type': 'line_type',
        'Code Type  ': 'line_type',
        'Code': 'code',
        'Code ': 'code',
        'Code   ': 'code',
        'Procedure Code': 'local_code',
        'Description': 'description',
        'NCD Code': 'ndc'

    }, inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:5]
    val_vars = cols[5:]

    df = pd.melt(df, id_vars=id_vars, value_vars=val_vars, var_name='payer_name', value_name='standard_charge')


    df.dropna(subset='standard_charge', inplace=True)


    df.loc[~df['code'].isna() & df['code'].str.match(r'^[A-Z][0-9]{4}$|^[0-9]{5}$|^[0-9]{4}[A-Z]$'), 'hcpcs_cpt'] = df['code']


    df.loc[df['payer_name'].str.contains('Outpatient|outpatient'), 'setting'] = 'outpatient'
    df.loc[df['payer_name'].str.contains('Inpatient|outpatient'), 'setting'] = 'inpatient'


    payer_mapping = {
        'Charge Amount': 'gross',
        'Cash Price': 'cash',
        'Uninsured Discount': 'cash',
        'De-Identified Minimum Negotiated Charge': 'min',
        'De-Identified Maximum Negotiated Charge': 'max'
    }

    df['rate_category'] = df['payer_name'].map(payer_mapping).fillna('negotiated')


    id_mapping = {
    '46-0360899_SpearfishHospital_StandardCharges.xlsx': '430048',
    '46-0319070_RapidCityHospital_StandardCharges.xlsx': '430077',
    '46-0360899_LeadDeadwoodHospital_StandardCharges.xlsx': '431320',
    '46-0360899_SturgisHospital_StandardCharges.xlsx': '431321',
    '46-0360899_CusterHospital_StandardCharges.xlsx': '431323'
    }

    hosp_id = id_mapping[file]

    df['hospital_id'] = hosp_id

    output_folder = '.\\output_files\\'

    df.to_csv(output_folder + hosp_id + '_' + file.split('_')[1] + '.csv', index=False)


