import pandas as pd
import numpy as np
import os
from tqdm import tqdm


def setting(x):
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
    if pd.isna(x):
        return 'none'
    
    x = str(x)
    prefixes = {
        'HCPCS': 'hcpcs_cpt',
        'CPT®': 'hcpcs_cpt',
        'Custom': 'custom'
    }
    
    # if len(str(x.split()[-1])) == 8:
    #     return 'custom'
    
    if " " in x:
        prefix = x.split(" ")[0]
        try:
            return prefixes[prefix]
        except KeyError:
            # print(x)
            pass
    
    else:
        return 'none'

def zero_pad(code, line_type):
    if line_type == 'drg':
        return str(code).zfill(3)
    else:
        return code


folder = ".\\input_files\\"

# file = '58-0572465_Childrens_Healthcare_of_ATL_at_Scottish_Rite_standardcharges.xlsx'
ccn = {
    '58-0572465': '113301',
    '58-0572412': '113300',
    '20-4144787': '113300',
}


for file in tqdm(os.listdir(folder)):
    print(file)
    ein = file.split("_")[0]
    if '.csv' in file:
        df = pd.read_csv(folder + file, dtype={'Code': str, 'Procedure': str, 'NDC': str, 'Rev Code': str})
        file = file.replace('.csv', '.xlsx')
    else:
        df = pd.read_excel(folder + file, skiprows=1, dtype={'Code': str, 'Procedure': str, 'NDC': str, 'Rev Code': str})
    


    df.rename(columns={
        'Procedure': 'local_code',
        'Code Type': 'line_type',
        'Code': 'code',
        'NDC': 'ndc',
        'Rev Code': 'rev_desc',
        'Procedure Description': 'description',
        'Quantity': 'drug_quantity'
    }, inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:cols.index('Gross Charges')]
    value_vars = cols[cols.index('Gross Charges'):]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_orig', value_name='rate')


    df['setting'] = df['payer_orig'].apply(setting)
    df['payer_category'] = df['payer_orig'].apply(payer_category)


    df['rev_code'] = df['rev_desc'].apply(lambda x: str(x).split(' - ')[0])

    df['line_type'] = df['line_type'].str.replace('Champus DRG - v35', 'drg')
    df['line_type'] = df['line_type'].str.replace('champus drg - v33', 'drg')

    zero_pad_func = np.vectorize(zero_pad)
    df['code'] = zero_pad_func(df['code_orig'], df['line_type'])
    # df['code_prefix'] = df['code'].apply(code_prefix)
    df.loc[df['code'].str.contains('HCPCS'), 'hcpcs_cpt'] = df['code'].str.replace('HCPCS', '')
    df.loc[df['code'].str.contains('CPT®'), 'hcpcs_cpt'] = df['code'].str.replace('CPT®', '')


    df['code'] = df['code'].apply(lambda x: str(x).split()[-1] if ' ' in str(x) else x)
    


    df['local_code'].fillna('na', inplace=True)
    df['code'].fillna('na', inplace=True)
    df['code'] = df['code'].str.replace('nan', 'na')
    df['rev_code'].fillna('na', inplace=True)
    df['rev_code'] = df['rev_code'].str.replace('nan', 'na')
    df['ndc'].fillna('na', inplace=True)
    # df['code_prefix'].fillna('none', inplace=True)

    # is_hcpcs_cpt_and_length_6 = df['code_prefix'] == 'hcpcs_cpt'
    # is_hcpcs_cpt_and_length_6 &= df['code'] != 'na'  # Exclude null cells (doesn't work for some reason)
    # is_hcpcs_cpt_and_length_6 &= df['code'].str.len() != 6
    # df.loc[~is_hcpcs_cpt_and_length_6, 'code_prefix'] = 'custom'

    na_code = df['code'] == 'na'
    # df.loc[na_code, 'code_prefix'] = 'none'
    df[df['code'] == 'na']

    # drg_codes = df['code'] != 'nan'
    # drg_codes &= df['code'].str.len() == 3
    # df.loc[drg_codes, 'code_prefix'] = 'ms-drg'


    df['payer_name'] = df['payer_orig']
    df['line_type'] = df['line_type'].str.lower()

    df['line_type'] = df['line_type'].str.replace('champus drg - v33', 'drg') # Not sure why this has to be down here
    df.loc[df['line_type'].isin(['ed', 'ed ', 'er', 'ct', 'mri', 'ip per diem']), 'line_type'] = None
    # df['filename'] = file
    # df['hospital_ein'] = ein
    df['hospital_id'] = ccn[ein]
    # df['file_last_updated'] = '2023-01-01'
    df['url'] = 'https://choaassets.choa.org/images/files/' + file

    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    
    df.dropna(subset=['rate'], inplace=True)

    df.to_csv('.\\output_files\\' + ein + '.csv', index=False)


