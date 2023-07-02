import pandas as pd
import numpy as np
import os
from tqdm import tqdm
# import heartrate; heartrate.trace(browser=True, daemon=True)
folder = '.\\input_files\\'
# file = '135596796_MARY-IMOGENE-BASSETT-HOSPITAL_STANDARDCHARGES.csv'

for file in tqdm(os.listdir(folder)):
    print('\n', file)
    df = pd.read_csv(folder + file, skiprows=3, dtype=str, encoding='ansi')


    df.rename(columns={
        'Payer': 'payer_name',
        'Internal Code': 'local_code',
        'Code': 'code',
        'NDC': 'ndc',
        'Rev Code': 'rev_code',
        'Procedure Description': 'description',
        'Quantity': 'quantity',
        'Plan(s)': 'plan_name',
        'Contract': 'additional_payer_notes',
        'Code Type': 'line_type'
    }, inplace=True)


    df = df.assign(plan_name=df['plan_name'].str.split(',')).explode('plan_name')


    df.reset_index(drop=True, inplace=True)


    df.loc[(~df['rev_code'].isna()), 'rev_code'] = df['rev_code'].str.extract(r'(\d{4})', expand=False)


    df.drop(columns=['IP XR Detail'], inplace=True)


    cols = df.columns.tolist()

    if 'line_type' in cols:
        id_vars = cols[:10]
        val_vars = cols[10:]
    else:
        id_vars = cols[:9]
        val_vars = cols[9:]

    df = pd.melt(df, id_vars=id_vars, value_vars=val_vars, var_name='payer_type', value_name='standard_charge')


    df['payer_type'] = df['payer_type'].str.strip()


    # Set column `setting` to either `inpatient` if col `payer` starts with  'IP' or `outpatient` if col `payer` starts with  'OP'
    df['setting'] = np.where(df['payer_type'].str.startswith('IP '), 'inpatient', np.where(df['payer_type'].str.startswith('OP '), 'outpatient', 1))


    payer_mapping = {
        'IP Price': 'gross',
        'OP Price': 'gross',
        'IP Expected Reimbursement': 'payer',
        'OP Expected Reimbursement': 'payer',
        'Cash Price': 'cash'
    }

    df['payer_category'] = df['payer_type'].map(payer_mapping)


    df.drop(df.loc[(df['payer_name'] == '<Self-pay>') & (df['payer_type'] != 'Cash Price')].index, inplace=True)


    df.loc[df['quantity'] == '1', 'quantity'] = pd.NA
    df['standard_charge'] = df['standard_charge'].str.replace('$', '').str.replace(',', '').str.strip()

    df.loc[df['standard_charge'] == '-', 'standard_charge'] = pd.NA
    df.dropna(subset='standard_charge', inplace=True)


    df.loc[(~df['code'].isna()) & (df['code'].str.match('HCPCS|CPT®')), 'hcpcs_cpt'] = df['code'].str.replace('HCPCS |CPT® ', '', regex=True)
    df['hcpcs_cpt'] = df['hcpcs_cpt'].str.strip()
    df.loc[(df['hcpcs_cpt'].str.len() == 8) | (df['hcpcs_cpt'] == 'CUSTOM') | (df['hcpcs_cpt'].str.len() != 5), 'hcpcs_cpt'] = pd.NA


    df.drop(columns='payer_type', inplace=True)


    hospital_map = {
        '150539039_AURELIA-OSBORN-FOX-MEMORIAL-HOSPITAL_STANDARDCHARGES_0.csv': '330408',
        '135596796_MARY-IMOGENE-BASSETT-HOSPITAL_STANDARDCHARGES.csv': '330136',
        '161540394_OCONNOR-HOSPITAL_STANDARDCHARGES_0.csv': '331305',
        '150533578_LITTLE-FALLS-HOSPITAL_STANDARDCHARGES_0.csv': '331311',
        '141772971_COBLESKILL-REGIONAL-HOSPITAL_STANDARDCHARGES_0.csv': '331320',
        '150539039_AURELIA-OSBORN-FOX-MEMORIAL-HOSPITAL_STANDARDCHARGES_1.csv': '330085'
    }

    hosp_id = hospital_map[file]

    df['hospital_id'] = hosp_id

    df.drop_duplicates(inplace=True)

    df.to_csv('.\\output_files\\' + hosp_id + file.split('_')[1] + '.csv', index=False)


