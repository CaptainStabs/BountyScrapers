import pandas as pd
import numpy as np
import os
from tqdm import tqdm


folder = '.\\input_files\\'
# file = '815427847_AsanteAshlandCommunityHospital_Standardcharges.csv'

for file in tqdm(os.listdir(folder)):
    df = pd.read_csv(folder + file, dtype=str, encoding='ansi')


    df.drop(columns='Location', inplace=True)


    df.rename(columns={
        'Procedure': 'local_code',
        'Code Type': 'line_type', 
        'Code': 'code',
        'NDC': 'ndc',
        'Rev Code': 'rev_code',
        'Procedure Description': 'description',
        'Quantity': 'quantity',
        'Payer': 'payer_name', 
        'Plan(s)': 'plan_name'
    }, inplace=True)


    df['rev_code'] = df['rev_code'].str.split(' -').str[0]


    df.loc[df['quantity'] == "1", 'quantity'] = pd.NA


    cols = df.columns.tolist()
    id_vars = cols[:9]
    value_vars = ['IP Expected Reimbursement', 'OP Expected Reimbursement']

    payer_df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_temp', value_name='standard_charge')


    df.drop(columns=['payer_name', 'plan_name', 'IP Expected Reimbursement', 'OP Expected Reimbursement'], inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:7]
    value_vars = cols[7:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')


    df = pd.concat([df, payer_df])


    df


    df['setting'] = np.where(df['payer_name'].str.startswith('IP'), 'inpatient', np.where(df['payer_name'].str.startswith('OP'), 'outpatient', 1))
    df['setting'] = np.where(df['payer_temp'].str.startswith('IP'), 'inpatient', np.where(df['payer_temp'].str.startswith('OP'), 'outpatient', 1))


    payer_mapping = {
        'IP Price': 'gross',
        'IP De-Identified MIN': 'min',
        'IP De-Identified MAX': 'max',
        'OP Price': 'gross',   
        'OP De-Identified MIN': 'min',
        'OP De-Identified MAX': 'max',
        '<Self-pay>': 'cash'
    }

    df['payer_category'] = df['payer_name'].map(payer_mapping)


    df.loc[df['payer_name'] == '<Self-pay>', 'payer_category'] = 'cash'


    df.loc[~df['payer_temp'].isna(), 'payer_category'] = 'payer'


    df.drop(columns='payer_temp', inplace=True)


    df['code'] = df['code'].str.strip()


    df.reset_index(drop=True, inplace=True)


    df.loc[~df['code'].isna() & df['code'].str.match(r"MS\d{3}"), 'ms_drg'] = df['code'].str.replace('MS', '')


    df['ms_drg'] = df['ms_drg'].astype(str)


    df.reset_index(drop=True, inplace=True)


    df.loc[~df['code'].isna() & df['code'].str.startswith('HCPCS '), 'hcpcs_cpt'] = df['code'].str.replace('HCPCS ', '')
    df.loc[~df['code'].isna() & df['code'].str.startswith('CPT® '), 'hcpcs_cpt'] = df['code'].str.replace('CPT® ', '')


    df.loc[df['hcpcs_cpt'].str.len() == 7, 'hcpcs_cpt'] = pd.NA


    df.loc[~df['plan_name'].isna() & df['plan_name'].str.contains(',')]


    df = df.assign(plan_name=df['plan_name'].str.split(', ')).explode('plan_name')


    df['standard_charge'] = df['standard_charge'].str.replace(',', '')


    df.dropna(subset='standard_charge', inplace=True)


    id_mapping = {
    '571181758_AsanteThreeRiversMedicalCenter_Standardcharges.csv': '380002',
    '815427847_AsanteAshlandCommunityHospital_Standardcharges.csv': '380005',
    '930223960_AsanteRogueRegionalMedicalCenter_Standardcharges.csv': '380018'}

    hosp_id = id_mapping[file]

    df['hospital_id'] = hosp_id

    output_folder = '.\\output_files\\'

    filename = hosp_id + file.split('_')[1] + '.csv'

    df.to_csv(output_folder + filename, index=False)


