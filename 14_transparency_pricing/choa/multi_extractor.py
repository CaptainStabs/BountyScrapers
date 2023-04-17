import pandas as pd
import numpy as np
import os


def patient_class(x):
    if " IP" in x or "Inpatient" in x:
        return 'inpatient'
    elif " OP" in x or "Outpatient" in x:
        return 'outpatient'
    else:
        return 'both'

def payer_category(x):
    payers = {
        'Gross Charges': 'gross',
        'De-identified Minimum IP Charge': 'min',
        'De-identified Minimum OP Charge': 'min',
        'De-identified Maximum Charge IP': 'max',
        'De-identified Maximum Charge OP': 'max',
        'SELF PAY BEFORE FINANCIAL ASSISTANCE': 'cash'
    }

    try:
        return payers[x]
    except KeyError:
        return 'payer'

def code_prefix(x):
    x = str(x)
    prefixes = {
        'HCPCS': 'hcpcs_cpt',
        'CPT®': 'hcpcs_cpt',
        'Custom': 'custom'
    }

    if " " in x:
        prefix = x.split(" ")[0]
        try:
            return prefixes[prefix]
        except KeyError:
            print(x)
    else:
        return 'none'

def zero_pad(code, code_type):
    if code_type == 'drg':
        return str(code).zfill(3)
    else:
        return code


folder = ".\\input_files\\"

file = '58-0572465_Childrens_Healthcare_of_ATL_at_Scottish_Rite_standardcharges.xlsx'
ein = file.split("_")[0]

ccn = {
    '58-0572465': '113301',
    '58-0572412': '113300',
    '20-4144787': '113300',
}


for file in os.listdir(folder):
        
    df = pd.read_excel(folder + file, skiprows=1, dtype={'Code': str, 'Procedure': str, 'NDC': str, 'Rev Code': str})


    df.rename(columns={
        'Procedure': 'internal_code',
        'Code Type': 'code_type',
        'Code': 'code_orig',
        'NDC': 'ndc',
        'Rev Code': 'rev_desc',
        'Procedure Description': 'description',
    }, inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:cols.index('Gross Charges')]
    value_vars = cols[cols.index('Gross Charges'):]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_orig', value_name='rate')


    df['patient_class'] = df['payer_orig'].apply(patient_class)
    df['payer_category'] = df['payer_orig'].apply(payer_category)


    df['rev_code'] = df['rev_desc'].apply(lambda x: str(x).split(' - ')[0])

    df['code_type'] = df['code_type'].str.replace('Champus DRG - v35', 'drg')

    zero_pad_func = np.vectorize(zero_pad)
    df['code'] = zero_pad_func(df['code_orig'], df['code_type'])
    df['code_prefix'] = df['code'].apply(code_prefix)

    df['code'] = df['code'].apply(lambda x: str(x).split()[-1] if ' ' in str(x) else x)


    df['internal_code'].fillna('na', inplace=True)
    df['code'].fillna('na', inplace=True)
    df['rev_code'].fillna('na', inplace=True)


    df['payer_name'] = df['payer_orig']
    df['code_type'] = df['code_type'].str.lower()

    df['filename'] = file
    df['hospital_ein'] = ein
    df['hospital_ccn'] = ccn[ein]
    df['file_last_updated'] = '2023-01-01'

    df.to_csv(ein + '.csv', index=False)


