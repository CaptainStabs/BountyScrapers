
import pandas as pd
import numpy as np
import os


def payer_category(x):
    if 'Maximum Fee' in x:
        return 'max'
    elif 'Minimum Fee' in x:
        return'min'
    elif 'Cash Price' in x:
        return 'cash'
    elif 'Gross' in x:
        return 'gross'


folder = '.\\input_files\\'

for file in os.listdir(folder):

    df = pd.read_excel(folder + file, skiprows=3)


    df.rename(columns={
        'Charge Description Master Detail': 'description',
        'REV/CPT/HCPCS': 'code',
        'Payor': 'payer',
        'Plan': 'plan',


    }, inplace=True)


    df.dropna(subset=['payer'], inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:4]
    value_vars = ['Negotiated Fee Inpatient', 'Negotiated Fee Outpatient']
    df_payers = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_temp', value_name='standard_charge')


    df_payers['setting'] = np.where(df_payers['payer_temp'].str.contains('Inpatient'), 'inpatient', np.where(df_payers['payer_temp'].str.contains('Outpatient'), 'outpatient', 1))
    df_payers.drop('payer_temp', axis=1, inplace=True)


    df_payers['payer_category'] = 'payer'


    # Do non-payer columns
    df.drop(['Negotiated Fee Inpatient', 'Negotiated Fee Outpatient', 'payer', 'plan'], axis=1, inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:2]
    value_vars = cols[2:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer', value_name='standard_charge')


    df['payer_category'] = df['payer'].apply(payer_category)
    df['setting'] = np.where(df['payer'].str.contains('Inpatient'), 'inpatient', np.where(df['payer'].str.contains('Outpatient'), 'outpatient', 1))


    df1 = pd.concat([df, df_payers])


    df = df1


    df.reset_index(drop=False, inplace=True)


    df.drop(['level_0', 'index'], axis=1, inplace=True)


    df.loc[df['code'].str.len() == 3, 'rev_code'] = df['code']
    df.loc[df['code'].str.len() == 5, 'hcpcs_cpt'] = df['code']
    df.loc[df['code'].str.len() == 7, 'hcpcs_cpt'] = df['code'].str[:5]
    df.loc[df['code'].str.len() == 7, 'modifiers'] = df['code'].str[-2:]

    df['code'].fillna('""', inplace=True)
    df['plan'].fillna('""', inplace=True)
    df['rev_code'].fillna('""', inplace=True)
    df['hcpcs_cpt'].fillna('""', inplace=True)
    df['modifiers'].fillna('""', inplace=True)

    ccn = {
        '460726303': '210062',
        '520491660': '210034',
        '520591607': '210056',
        '520591685': '210024',
        '520608007': '210015',
        '520619006': '210028',
        '520646893': '210018'
    }

    ein = file.split('_')[0]

    hosp_id = ccn[ein]

    df['hospital_id'] = hosp_id

    df.to_csv('.\\output_files\\' + hosp_id + '.csv', index=False)